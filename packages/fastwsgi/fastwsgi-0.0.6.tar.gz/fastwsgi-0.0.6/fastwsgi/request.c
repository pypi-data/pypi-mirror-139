#include "server.h"
#include "request.h"
#include "llhttp.h"
#include "constants.h"
#include "start_response.h"

static void reprint(PyObject* obj) {
    PyObject* repr = PyObject_Repr(obj);
    PyObject* str = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
    const char* bytes = PyBytes_AS_STRING(str);

    printf("REPR: %s\n", bytes);

    Py_XDECREF(repr);
    Py_XDECREF(str);
}

static void set_header(PyObject* headers, const char* key, const char* value, size_t length) {
    logger("setting header");
    PyObject* item = PyUnicode_FromStringAndSize(value, length);

    PyObject* existing_item = PyDict_GetItemString(headers, key);
    if (existing_item) {
        PyObject* comma = PyUnicode_FromString(",");
        PyObject* value_list = Py_BuildValue("[SS]", existing_item, item);
        PyObject* updated_item = PyUnicode_Join(comma, value_list);

        PyDict_SetItemString(headers, key, updated_item);
        Py_DECREF(updated_item);
        Py_DECREF(value_list);
        Py_DECREF(comma);
    }
    else {
        PyDict_SetItemString(headers, key, item);
    }
    Py_DECREF(item);
}

int on_message_begin(llhttp_t* parser) {
    logger("on message begin");
    Request* request = (Request*)parser->data;
    request->headers = PyDict_Copy(base_dict);
    request->response_buffer.len = 0;
    return 0;
};

int on_url(llhttp_t* parser, const char* data, size_t length) {
    logger("on url");
    Request* request = (Request*)parser->data;

    char* url = malloc(length + 1);
    strncpy(url, data, length);
    url[length] = 0;

    char* query_string = strchr(url, '?');
    if (query_string) {
        *query_string = 0;
        set_header(request->headers, "QUERY_STRING", query_string + 1, strlen(query_string + 1));
    }
    set_header(request->headers, "PATH_INFO", url, strlen(url));

    free(url);
    return 0;
};

int on_body(llhttp_t* parser, const char* body, size_t length) {
    logger("on body");
    Request* request = (Request*)parser->data;

    PyObject* input = PyDict_GetItem(request->headers, wsgi_input);

    PyObject* write = PyUnicode_FromString("write");
    PyObject* body_content = PyBytes_FromStringAndSize(body, length);
    PyObject* result = PyObject_CallMethodObjArgs(input, write, body_content, NULL);
    Py_DECREF(write);
    Py_XDECREF(result);
    Py_XDECREF(body_content);

    return 0;
};

int on_header_field(llhttp_t* parser, const char* header, size_t length) {
    logger("on header field");

    char* upperHeader = malloc(length + 1);
    for (size_t i = 0; i < length; i++) {
        char current = header[i];
        if (current == '_') {
            current_header = NULL;  // CVE-2015-0219
            return 0;
        }
        if (current == '-') {
            upperHeader[i] = '_';
        }
        else {
            upperHeader[i] = toupper(current);
        }
    }
    upperHeader[length] = 0;
    char* old_header = current_header;

    if ((strcmp(upperHeader, "CONTENT_LENGTH") == 0) || (strcmp(upperHeader, "CONTENT_TYPE") == 0)) {
        current_header = upperHeader;
    }
    else {
        current_header = malloc(strlen(upperHeader) + 5);
        sprintf(current_header, "HTTP_%s", upperHeader);
    }

    if (old_header)
        free(old_header);

    return 0;
};

int on_header_value(llhttp_t* parser, const char* value, size_t length) {
    logger("on header value");
    if (current_header != NULL) {
        Request* request = (Request*)parser->data;
        set_header(request->headers, current_header, value, length);
    }
    return 0;
};

int on_message_complete(llhttp_t* parser) {
    logger("on message complete");
    Request* request = (Request*)parser->data;

    // Sets the input byte stream position back to 0
    PyObject* body = PyDict_GetItem(request->headers, wsgi_input);
    PyObject* seek = PyUnicode_FromString("seek");
    PyObject* res = PyObject_CallMethodObjArgs(body, seek, PyLong_FromLong(0L), NULL);
    Py_DECREF(res);
    Py_DECREF(seek);

    build_wsgi_environ(parser);

    StartResponse* start_response = PyObject_NEW(StartResponse, &StartResponse_Type);
    start_response->called = 0;

    logger("calling wsgi application");
    PyObject* wsgi_response;
    wsgi_response = PyObject_CallFunctionObjArgs(
        wsgi_app, request->headers, start_response, NULL
    );
    logger("called wsgi application");

    if (wsgi_response != NULL)
        build_response(wsgi_response, start_response, parser);

    if (PyErr_Occurred()) {
        request->state.error = 1;
        PyErr_Print();
    }

    Py_CLEAR(start_response->headers);
    Py_CLEAR(start_response->status);
    Py_CLEAR(start_response->exc_info);
    Py_CLEAR(start_response);

    Py_CLEAR(wsgi_response);
    Py_CLEAR(request->headers);
    return 0;
};

void build_response(PyObject* wsgi_response, StartResponse* response, llhttp_t* parser) {
    // This function needs a clean up

    logger("building response");
    Request* request = (Request*)parser->data;

    PyObject* iterator = NULL;
    PyObject* result = NULL;
    PyObject* item = NULL;

    if (PyBytes_Check(wsgi_response))
        result = wsgi_response;
    else {
        iterator = PyObject_GetIter(wsgi_response);
        result = PyBytes_FromString("");
        while ((item = PyIter_Next(iterator))) {
            PyBytes_ConcatAndDel(&result, item);
        }
    }

    int response_has_no_content = 0;

    PyObject* status = PyUnicode_AsUTF8String(response->status);
    char* status_code = PyBytes_AS_STRING(status);
    if (strncmp(status_code, "204", 3) == 0 || strncmp(status_code, "304", 3) == 0) {
        response_has_no_content = 1;
    }

    char* buf = malloc(strlen(status_code) + 10);
    sprintf(buf, "HTTP/1.1 %s", status_code);
    Py_DECREF(status);

    char* connection_header = "\r\nConnection: close";
    if (llhttp_should_keep_alive(parser)) {
        connection_header = "\r\nConnection: Keep-Alive";
        request->state.keep_alive = 1;
    }
    char* old_buf = buf;
    buf = malloc(strlen(old_buf) + strlen(connection_header));
    sprintf(buf, "%s%s", old_buf, connection_header);
    free(old_buf);

    int content_length_header_present = 0;
    for (Py_ssize_t i = 0; i < PyList_GET_SIZE(response->headers); i++) {
        PyObject* tuple = PyList_GET_ITEM(response->headers, i);

        PyObject* field = PyUnicode_AsUTF8String(PyTuple_GET_ITEM(tuple, 0));
        PyObject* value = PyUnicode_AsUTF8String(PyTuple_GET_ITEM(tuple, 1));

        char* header_field = PyBytes_AS_STRING(field);
        char* header_value = PyBytes_AS_STRING(value);

        if (!content_length_header_present)
            if (strcasecmp("Content-Length", header_field) == 0)
                content_length_header_present = 1;

        char* old_buf = buf;
        buf = malloc(strlen(old_buf) + strlen(header_field) + strlen(header_value) + 5);
        sprintf(buf, "%s\r\n%s: %s", old_buf, header_field, header_value);
        free(old_buf);

        Py_DECREF(field);
        Py_DECREF(value);

        logger("added header");
    }

    if (response_has_no_content) {
        char* old_buf = buf;
        buf = malloc(strlen(old_buf) + 26);
        sprintf(buf, "%s\r\nContent-Length: 0\r\n\r\n", old_buf);
        free(old_buf);
    }
    else {
        char* response_body = PyBytes_AS_STRING(result);

        if (content_length_header_present == 0) {
            char* old_buf = buf;
            buf = malloc(strlen(old_buf) + 32);
            sprintf(buf, "%s\r\nContent-Length: %ld", old_buf, strlen(response_body));
            free(old_buf);
        }

        char* old_buf = buf;
        buf = malloc(strlen(old_buf) + strlen(response_body) + 5);
        sprintf(buf, "%s\r\n\r\n%s", old_buf, response_body);
        free(old_buf);
    }

    logger(buf);
    request->response_buffer.base = buf;
    request->response_buffer.len = strlen(buf);

    if (iterator != NULL && PyObject_HasAttrString(iterator, "close")) {
        PyObject* close = PyObject_GetAttrString(iterator, "close");
        if (close != NULL) {
            PyObject* close_result = PyObject_CallObject(close, NULL);
            Py_XDECREF(close_result);
        }
        Py_XDECREF(close);
    }
    Py_XDECREF(iterator);
    Py_XDECREF(result);
    result = NULL;
}


void build_wsgi_environ(llhttp_t* parser) {
    logger("building wsgi environ");
    Request* request = (Request*)parser->data;

    const char* method = llhttp_method_name(parser->method);
    const char* protocol = parser->http_minor == 1 ? "HTTP/1.1" : "HTTP/1.0";
    const char* remote_addr = request->remote_addr;

    set_header(request->headers, "REQUEST_METHOD", method, strlen(method));
    set_header(request->headers, "SERVER_PROTOCOL", protocol, strlen(protocol));
    set_header(request->headers, "REMOTE_ADDR", remote_addr, strlen(remote_addr));
}

void init_request_dict() {
    // Sets up base request dict for new incoming requests
    // https://www.python.org/dev/peps/pep-3333/#specification-details
    PyObject* io = PyImport_ImportModule("io");
    PyObject* BytesIO = PyUnicode_FromString("BytesIO");
    PyObject* io_BytesIO = PyObject_CallMethodObjArgs(io, BytesIO, NULL);

    base_dict = PyDict_New();
    PyDict_SetItem(base_dict, SCRIPT_NAME, empty_string);
    PyDict_SetItem(base_dict, SERVER_NAME, server_host);
    PyDict_SetItem(base_dict, SERVER_PORT, server_port);
    PyDict_SetItem(base_dict, wsgi_input, io_BytesIO);
    PyDict_SetItem(base_dict, wsgi_version, version);
    PyDict_SetItem(base_dict, wsgi_url_scheme, http_scheme);
    PyDict_SetItem(base_dict, wsgi_errors, PySys_GetObject("stderr"));
    PyDict_SetItem(base_dict, wsgi_run_once, Py_False);
    PyDict_SetItem(base_dict, wsgi_multithread, Py_False);
    PyDict_SetItem(base_dict, wsgi_multiprocess, Py_True);
}

void configure_parser_settings() {
    llhttp_settings_init(&parser_settings);
    parser_settings.on_url = on_url;
    parser_settings.on_body = on_body;
    parser_settings.on_header_field = on_header_field;
    parser_settings.on_header_value = on_header_value;
    parser_settings.on_message_begin = on_message_begin;
    parser_settings.on_message_complete = on_message_complete;
}

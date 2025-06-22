
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libcustom_fn.h"
#include "./custom.h"

#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject* unpackb;


static PyObject* custom_fn_add(PyObject* self, PyObject* args) { 
    long a;
    long b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b))
        return NULL;
    long result = Add(a,b);
    return PyLong_FromLong(result);
}

static PyObject* custom_fn_getRequest(PyObject* self, PyObject* args) { 
    char* url;
    if (!PyArg_ParseTuple(args, "s", &url))
        return NULL;
    GoString go_url = {url, (GoInt)strlen(url)};
    char* result = GetRequest(go_url);
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyMethodDef Methods[] = {
    {"add", custom_fn_add, METH_VARARGS, "add"},
    {"getRequest", custom_fn_getRequest, METH_VARARGS, "getRequest"},
    {"custom_function", custom_function, METH_VARARGS, "custom_function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef custom_fn_module = {
    PyModuleDef_HEAD_INIT,
    "custom_fn",
    NULL,
    -1,
    Methods
};
PyMODINIT_FUNC PyInit_custom_fn(void) {
    PyObject* msgpack = PyImport_ImportModule("msgpack");
    if (msgpack == NULL) {
       PyErr_SetString(PyExc_ImportError, "msgpack module not found");
        return NULL;
    }
    unpackb = PyObject_GetAttrString(msgpack, "unpackb");

    return PyModule_Create(&custom_fn_module);
}

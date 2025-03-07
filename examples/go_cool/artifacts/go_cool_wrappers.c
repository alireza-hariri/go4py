
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "../artifacts/build/libgo_cool.h"
#include <string.h>


static PyObject* go_cool_transform(PyObject* self, PyObject* args) { 
    char* s;
    if (!PyArg_ParseTuple(args, "s", &s))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    char* result = Transform(go_s);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}
static PyObject* go_cool_add(PyObject* self, PyObject* args) { 
    long a;
    long b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b))
        return NULL;
    long result = Add(a,b);
    return PyLong_FromLong(result);
}
static PyObject* go_cool_replace(PyObject* self, PyObject* args) { 
    char* s;
    char* old;
    char* new;
    if (!PyArg_ParseTuple(args, "sss", &s, &old, &new))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    GoString go_old = {old, (GoInt)strlen(old)};
    GoString go_new = {new, (GoInt)strlen(new)};
    char* result = Replace(go_s,go_old,go_new);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}
static PyObject* go_cool_randomString(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    char* result = RandomString(n);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}
static PyObject* go_cool_cosine(PyObject* self, PyObject* args) { 
    double x;
    if (!PyArg_ParseTuple(args, "d", &x))
        return NULL;
    double result = Cosine(x);
    return PyFloat_FromDouble(result);
}
static PyObject* go_cool_f2str2(PyObject* self, PyObject* args) { 
    double x;
    if (!PyArg_ParseTuple(args, "d", &x))
        return NULL;
    char* result = F2str2(x);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}
static PyObject* go_cool_str2f(PyObject* self, PyObject* args) { 
    char* s;
    if (!PyArg_ParseTuple(args, "s", &s))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    double result = Str2f(go_s);
    return PyFloat_FromDouble(result);
}
static PyObject* go_cool_http_test(PyObject* self, PyObject* args) { 
    char* url;
    if (!PyArg_ParseTuple(args, "s", &url))
        return NULL;
    GoString go_url = {url, (GoInt)strlen(url)};
    void* result = Http_test(go_url);
    PyObject* py_result = PyBytes_FromString((char*)result);
    free(result);
    return py_result;
}
static PyObject* go_cool_init_go(PyObject* self, PyObject* args) { 
    Init_go();
    return Py_None;
}

static PyMethodDef Methods[] = {
    {"transform", go_cool_transform, METH_VARARGS, "transform"},
    {"add", go_cool_add, METH_VARARGS, "add"},
    {"replace", go_cool_replace, METH_VARARGS, "replace"},
    {"randomString", go_cool_randomString, METH_VARARGS, "randomString"},
    {"cosine", go_cool_cosine, METH_VARARGS, "cosine"},
    {"f2str2", go_cool_f2str2, METH_VARARGS, "f2str2"},
    {"str2f", go_cool_str2f, METH_VARARGS, "str2f"},
    {"http_test", go_cool_http_test, METH_VARARGS, "http_test"},
    {"init_go", go_cool_init_go, METH_VARARGS, "init_go"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef go_cool_module = {
    PyModuleDef_HEAD_INIT,
    "go_cool",
    NULL,
    -1,
    Methods
};
PyMODINIT_FUNC PyInit_go_cool(void) {
    return PyModule_Create(&go_cool_module);
}


#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "../build/libgo_cool.h"
#include <string.h>


// add function
static PyObject* go_cool_add(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    int result = (int)Add(a, b);
    return PyLong_FromLong(result);
}

// replace function replace
static PyObject* go_cool_replace(PyObject* self, PyObject* args) {
    const char *str;
    const char *old;
    const char *new;
    if (!PyArg_ParseTuple(args, "sss", &str, &old, &new))
        return NULL;

    GoString go_str = {str, (GoInt)strlen(str)};
    GoString go_old = {old, (GoInt)strlen(old)};
    GoString go_new = {new, (GoInt)strlen(new)};
    char* result = Replace(go_str, go_old, go_new);
    // return PyUnicode_FromStringAndSize(result.p, result.n);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}


static PyObject* go_cool_random_string(PyObject* self, PyObject* args) {
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    char* result = RandomString(n);
    PyObject* py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}




static PyObject* go_cool_myFunc(PyObject* self, PyObject* args) {
    long a;
    char* s;
    if (!PyArg_ParseTuple(args, "ls", &a, &s))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    long result = myFunc(a,go_s);
    PyObject* py_result = PyLong_FromLong(result);
    return py_result;
}


static PyMethodDef GoCoolMethods[] = {
    {"add", go_cool_add, METH_VARARGS, "Add two numbers"},
    {"replace", go_cool_replace, METH_VARARGS, "Replace"},
    {"random_string", go_cool_random_string, METH_VARARGS, "RandomString"},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef go_cool_module = {
    PyModuleDef_HEAD_INIT,
    "go_cool",
    NULL,
    -1,
    GoCoolMethods
};
PyMODINIT_FUNC PyInit_go_cool(void) {
    return PyModule_Create(&go_cool_module);
}
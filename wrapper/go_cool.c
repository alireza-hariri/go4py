
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "../build/libgo_cool.h"
#include <string.h>

static PyObject* go_cool_add(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    int result = (int)Add((GoInt)a, (GoInt)b);
    return PyLong_FromLong(result);
}

static PyMethodDef GoCoolMethods[] = {
    {"add", go_cool_add, METH_VARARGS, "Add two numbers"},
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
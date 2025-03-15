
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libmemLeakTests.h"

#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}



static PyObject* memLeakTests_func_x(PyObject* self, PyObject* args) { 
    char* result = Func_x();
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* memLeakTests_func_5(PyObject* self, PyObject* args) { 
    struct Func_5_return result = Func_5();
    PyObject* py_result_r0 = result.r0==NULL ? GetPyNone() : PyUnicode_FromString(result.r0);
    free(result.r0);
    PyObject* py_result_r1 = result.r1==NULL ? GetPyNone() : PyUnicode_FromString(result.r1);
    free(result.r1);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}

static PyObject* memLeakTests_func_6(PyObject* self, PyObject* args) { 
    char* a;
    if (!PyArg_ParseTuple(args, "s", &a))
        return NULL;
    GoString go_a = {a, (GoInt)strlen(a)};
    char* result = Func_6(go_a);
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* memLeakTests_func_8(PyObject* self, PyObject* args) { 
    char* a;
    if (!PyArg_ParseTuple(args, "s", &a))
        return NULL;
    Func_8(a);
    RETURN_NONE;
}

static PyObject* memLeakTests_func_10(PyObject* self, PyObject* args) { 
    GoSlice result = Func_10();
    PyObject* py_result = result.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.data, result.len);
    free(result.data);
    return py_result;
}

static PyObject* memLeakTests_func_11(PyObject* self, PyObject* args) { 
    struct Func_11_return result = Func_11();
    PyObject* py_result_r0 = result.r0.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r0.data, result.r0.len);
    free(result.r0.data);
    PyObject* py_result_r1 = result.r1.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r1.data, result.r1.len);
    free(result.r1.data);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}

static PyMethodDef Methods[] = {
    {"func_x", memLeakTests_func_x, METH_VARARGS, "func_x"},
    {"func_5", memLeakTests_func_5, METH_VARARGS, "func_5"},
    {"func_6", memLeakTests_func_6, METH_VARARGS, "func_6"},
    {"func_8", memLeakTests_func_8, METH_VARARGS, "func_8"},
    {"func_10", memLeakTests_func_10, METH_VARARGS, "func_10"},
    {"func_11", memLeakTests_func_11, METH_VARARGS, "func_11"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef memLeakTests_module = {
    PyModuleDef_HEAD_INIT,
    "memLeakTests",
    NULL,
    -1,
    Methods
};
PyMODINIT_FUNC PyInit_memLeakTests(void) {
    return PyModule_Create(&memLeakTests_module);
}

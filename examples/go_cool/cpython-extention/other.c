#include <Python.h>
#include "../artifacts/build/libgo_cool.h"
#include "./other.h"

// slice of ints to go
PyObject* go_cool_someFunc(PyObject* self, PyObject* args) { 
    PyObject* nums;
    if (!PyArg_ParseTuple(args, "O", &nums))
        return NULL;
    if (!PyList_Check(nums)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a list");
        return NULL;
    }
    int len = PyList_Size(nums);
    long* arr = malloc(len * sizeof(long));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(nums, i);
        arr[i] = PyLong_AsLong(item);
    }
    if (PyErr_Occurred()) {
        free(arr);
        return NULL;
    }
    GoSlice go_nums = {arr, (GoInt)len, (GoInt)len};
    SomeFunc(go_nums);
    free(arr);
    Py_INCREF(Py_None);
    return Py_None;
}

// slice of strings to go
PyObject* go_cool_someFunc2(PyObject* self, PyObject* args) {
    PyObject* strs;
    if (!PyArg_ParseTuple(args, "O", &strs))
        return NULL;
    if (!PyList_Check(strs)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a list");
        return NULL;
    }
    int len = PyList_Size(strs);
    GoString* arr = malloc(len * sizeof(GoString));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(strs, i);
        if (!PyUnicode_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be strings");
            free(arr);
            return NULL;
        }
        const char* c_item = PyUnicode_AsUTF8(item);
        arr[i] = (GoString) {c_item, (GoInt)strlen(c_item)};
    }
    if (PyErr_Occurred()) {
        free(arr);
        return NULL;
    }
    GoSlice go_strs = {arr, (GoInt)len, (GoInt)len};
    SomeFunc2(go_strs);
    free(arr);
    Py_INCREF(Py_None);
    return Py_None;
}

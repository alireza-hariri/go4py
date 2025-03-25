
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libmemLeakTests.h"


#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject* unpackb;


static PyObject* memLeakTests_func_1(PyObject* self, PyObject* args) { 
    PyObject* a;
    if (!PyArg_ParseTuple(args, "O", &a))
        return NULL;
    if (!PyList_Check(a)) {
        PyErr_SetString(PyExc_TypeError, "Argument a must be a list");
        return NULL;
    }
    int len_a = PyList_Size(a);
    long* a_CArray = malloc(len_a * sizeof(long));
    for (int i = 0; i < len_a; i++) {
        PyObject* item = PyList_GetItem(a, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyLong");
            free(a_CArray);
            return NULL;
        }
        a_CArray[i] = PyLong_AsLong(item);
    }
    if (PyErr_Occurred()) {
        free(a_CArray);
        return NULL;
    }
    GoSlice go_a = {a_CArray, (GoInt)len_a, (GoInt)len_a};
    Func_1(go_a);
    free(a_CArray);
    RETURN_NONE;
}

static PyObject* memLeakTests_func_2(PyObject* self, PyObject* args) { 
    PyObject* a;
    PyObject* b;
    if (!PyArg_ParseTuple(args, "OO", &a, &b))
        return NULL;
    if (!PyList_Check(a)) {
        PyErr_SetString(PyExc_TypeError, "Argument a must be a list");
        return NULL;
    }
    int len_a = PyList_Size(a);
    GoString* a_CArray = malloc(len_a * sizeof(GoString));
    for (int i = 0; i < len_a; i++) {
        PyObject* item = PyList_GetItem(a, i);
        if (!PyUnicode_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyUnicode");
            free(a_CArray);
            return NULL;
        }
        const char* c_item = PyUnicode_AsUTF8(item);
        a_CArray[i] = (GoString) {c_item, (GoInt)strlen(c_item)};
    }
    if (PyErr_Occurred()) {
        free(a_CArray);
        return NULL;
    }
    GoSlice go_a = {a_CArray, (GoInt)len_a, (GoInt)len_a};
    if (!PyList_Check(b)) {
        PyErr_SetString(PyExc_TypeError, "Argument b must be a list");
        free(a_CArray);
        return NULL;
    }
    int len_b = PyList_Size(b);
    const char** b_CArray = malloc(len_b * sizeof(char*));
    for (int i = 0; i < len_b; i++) {
        PyObject* item = PyList_GetItem(b, i);
        if (!PyUnicode_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyUnicode");
            free(a_CArray);
            free(b_CArray);
            return NULL;
        }
        b_CArray[i] = PyUnicode_AsUTF8(item);
    }
    if (PyErr_Occurred()) {
        free(a_CArray);
        free(b_CArray);
        return NULL;
    }
    GoSlice go_b = {b_CArray, (GoInt)len_b, (GoInt)len_b};
    Func_2(go_a,go_b);
    free(a_CArray);
    free(b_CArray);
    RETURN_NONE;
}

static PyObject* memLeakTests_func_3(PyObject* self, PyObject* args) { 
    GoSlice result = Func_3();
    PyObject* py_result;
    if (result.data == NULL) {
        py_result = GetPyNone();
    } else {
        py_result = PyList_New(result.len);
        for (int i = 0; i < result.len; i++) {
            long item = ((long*)result.data)[i];
            PyList_SetItem(py_result, i, PyLong_FromLong(item));
        }
    }
    free(result.data);
    return py_result;
}

static PyObject* memLeakTests_func_4(PyObject* self, PyObject* args) { 
    GoSlice result = Func_4();
    PyObject* py_result;
    if (result.data == NULL) {
        py_result = GetPyNone();
    } else {
        py_result = PyList_New(result.len);
        for (int i = 0; i < result.len; i++) {
            char* item = ((char**)result.data)[i];
            PyObject* py_item = item==NULL ? GetPyNone() : PyUnicode_FromString(item);
            free(item);
            PyList_SetItem(py_result, i, py_item);
        }
    }
    free(result.data);
    return py_result;
}

static PyObject* memLeakTests_func_5_2(PyObject* self, PyObject* args) { 
    struct Func_5_2_return result = Func_5_2();
    PyObject* py_result_r0;
    if (result.r0.data == NULL) {
        py_result_r0 = GetPyNone();
    } else {
        py_result_r0 = PyList_New(result.r0.len);
        for (int i = 0; i < result.r0.len; i++) {
            GoSlice item = ((GoSlice*)result.r0.data)[i];
            PyObject* py_item = item.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(item.data, item.len);
            free(item.data);
            PyList_SetItem(py_result_r0, i, py_item);
        }
    }
    free(result.r0.data);
    PyObject* py_result_r1;
    if (result.r1.data == NULL) {
        py_result_r1 = GetPyNone();
    } else {
        py_result_r1 = PyList_New(result.r1.len);
        for (int i = 0; i < result.r1.len; i++) {
            char* item = ((char**)result.r1.data)[i];
            PyObject* py_item = item==NULL ? GetPyNone() : PyUnicode_FromString(item);
            free(item);
            PyList_SetItem(py_result_r1, i, py_item);
        }
    }
    free(result.r1.data);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
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

static PyObject* memLeakTests_func_7(PyObject* self, PyObject* args) { 
    char* a;
    unsigned short b;
    char* c;
    double d;
    if (!PyArg_ParseTuple(args, "sHsd", &a, &b, &c, &d))
        return NULL;
    GoString go_a = {a, (GoInt)strlen(a)};
    GoString go_c = {c, (GoInt)strlen(c)};
    int result = Func_7(go_a,b,go_c,d);
    return PyBool_FromLong(result);
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
    {"func_1", memLeakTests_func_1, METH_VARARGS, "func_1"},
    {"func_2", memLeakTests_func_2, METH_VARARGS, "func_2"},
    {"func_3", memLeakTests_func_3, METH_VARARGS, "func_3"},
    {"func_4", memLeakTests_func_4, METH_VARARGS, "func_4"},
    {"func_5_2", memLeakTests_func_5_2, METH_VARARGS, "func_5_2"},
    {"func_x", memLeakTests_func_x, METH_VARARGS, "func_x"},
    {"func_5", memLeakTests_func_5, METH_VARARGS, "func_5"},
    {"func_6", memLeakTests_func_6, METH_VARARGS, "func_6"},
    {"func_7", memLeakTests_func_7, METH_VARARGS, "func_7"},
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
    PyObject* msgpack = PyImport_ImportModule("msgpack");
    if (msgpack == NULL) {
       PyErr_SetString(PyExc_ImportError, "msgpack module not found");
        return NULL;
    }
    unpackb = PyObject_GetAttrString(msgpack, "unpackb");

    return PyModule_Create(&memLeakTests_module);
}

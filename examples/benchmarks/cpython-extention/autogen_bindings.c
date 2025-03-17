
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libbenchmarks.h"


#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject* unpackb;


static PyObject* benchmarks_add(PyObject* self, PyObject* args) { 
    long a;
    if (!PyArg_ParseTuple(args, "l", &a))
        return NULL;
    long result = Add(a);
    return PyLong_FromLong(result);
}

static PyObject* benchmarks_rand(PyObject* self, PyObject* args) { 
    double result = Rand();
    return PyFloat_FromDouble(result);
}

static PyObject* benchmarks_randn(PyObject* self, PyObject* args) { 
    double result = Randn();
    return PyFloat_FromDouble(result);
}

static PyObject* benchmarks_randArray(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    GoSlice result = RandArray(n);
    PyObject* py_result;
    if (result.data == NULL) {
        py_result = GetPyNone();
    } else {
        py_result = PyList_New(result.len);
        for (int i = 0; i < result.len; i++) {
            double item = ((double*)result.data)[i];
            PyList_SetItem(py_result, i, PyFloat_FromDouble(item));
        }
    }
    free(result.data);
    return py_result;
}

static PyObject* benchmarks_getRequest(PyObject* self, PyObject* args) { 
    char* url;
    if (!PyArg_ParseTuple(args, "s", &url))
        return NULL;
    GoString go_url = {url, (GoInt)strlen(url)};
    struct GetRequest_return result = GetRequest(go_url);
    PyObject* py_result_r0 = result.r0.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r0.data, result.r0.len);
    free(result.r0.data);
    PyObject* py_result_r1 = result.r1==NULL ? GetPyNone() : PyUnicode_FromString(result.r1);
    free(result.r1);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}

static PyObject* benchmarks_fibo(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    long result = Fibo(n);
    return PyLong_FromLong(result);
}

static PyObject* benchmarks_findPrimes(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    GoSlice result = FindPrimes(n);
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

static PyObject* benchmarks_solveSudoku(PyObject* self, PyObject* args) { 
    PyObject* board_flat;
    int print;
    if (!PyArg_ParseTuple(args, "Op", &board_flat, &print))
        return NULL;
    if (!PyList_Check(board_flat)) {
        PyErr_SetString(PyExc_TypeError, "Argument board_flat must be a list");
        return NULL;
    }
    int len_board_flat = PyList_Size(board_flat);
    long* board_flat_CArray = malloc(len_board_flat * sizeof(long));
    for (int i = 0; i < len_board_flat; i++) {
        PyObject* item = PyList_GetItem(board_flat, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyLong");
            free(board_flat_CArray);
            return NULL;
        }
        board_flat_CArray[i] = PyLong_AsLong(item);
    }
    if (PyErr_Occurred()) {
        free(board_flat_CArray);
        return NULL;
    }
    GoSlice go_board_flat = {board_flat_CArray, (GoInt)len_board_flat, (GoInt)len_board_flat};
    int result = SolveSudoku(go_board_flat,print);
    free(board_flat_CArray);
    return PyBool_FromLong(result);
}

static PyMethodDef Methods[] = {
    {"add", benchmarks_add, METH_VARARGS, "add"},
    {"rand", benchmarks_rand, METH_VARARGS, "rand"},
    {"randn", benchmarks_randn, METH_VARARGS, "randn"},
    {"randArray", benchmarks_randArray, METH_VARARGS, "randArray"},
    {"getRequest", benchmarks_getRequest, METH_VARARGS, "getRequest"},
    {"fibo", benchmarks_fibo, METH_VARARGS, "fibo"},
    {"findPrimes", benchmarks_findPrimes, METH_VARARGS, "findPrimes"},
    {"solveSudoku", benchmarks_solveSudoku, METH_VARARGS, "solveSudoku"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef benchmarks_module = {
    PyModuleDef_HEAD_INIT,
    "benchmarks",
    NULL,
    -1,
    Methods
};
PyMODINIT_FUNC PyInit_benchmarks(void) {
    PyObject* msgpack = PyImport_ImportModule("msgpack");
    if (msgpack == NULL) {
       PyErr_SetString(PyExc_ImportError, "msgpack module not found");
        return NULL;
    }
    unpackb = PyObject_GetAttrString(msgpack, "unpackb");

    return PyModule_Create(&benchmarks_module);
}

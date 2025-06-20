
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libmsgPack.h"


#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject* unpackb;


static PyObject* msgPack_example_fn1(PyObject* self, PyObject* args) { 
    struct Example_fn1_return result = Example_fn1();
    PyObject* py_result_r0_msgpack;
    if (result.r0.data!=NULL){
        PyObject* py_result_r0 = PyBytes_FromStringAndSize(result.r0.data, result.r0.len);
        py_result_r0_msgpack = PyObject_CallFunctionObjArgs(unpackb, py_result_r0, NULL);
        Py_DECREF(py_result_r0);
    }else{
        py_result_r0_msgpack = GetPyNone();
    }
    free(result.r0.data);
    PyObject* py_result_r1 = result.r1==NULL ? GetPyNone() : PyUnicode_FromString(result.r1);
    free(result.r1);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0_msgpack, py_result_r1);
    Py_DECREF(py_result_r0_msgpack);
    Py_DECREF(py_result_r1);
    return py_result;
}

static PyObject* msgPack_example_fn2(PyObject* self, PyObject* args) { 
    struct Example_fn2_return result = Example_fn2();
    PyObject* py_result_r0 = result.r0.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r0.data, result.r0.len);
    free(result.r0.data);
    PyObject* py_result_r1 = result.r1==NULL ? GetPyNone() : PyUnicode_FromString(result.r1);
    free(result.r1);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}

static PyMethodDef Methods[] = {
    {"example_fn1", msgPack_example_fn1, METH_VARARGS, "example_fn1"},
    {"example_fn2", msgPack_example_fn2, METH_VARARGS, "example_fn2"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef msgPack_module = {
    PyModuleDef_HEAD_INIT,
    "msgPack",
    NULL,
    -1,
    Methods
};
PyMODINIT_FUNC PyInit_msgPack(void) {
    PyObject* msgpack = PyImport_ImportModule("msgpack");
    if (msgpack == NULL) {
       PyErr_SetString(PyExc_ImportError, "msgpack module not found");
        return NULL;
    }
    unpackb = PyObject_GetAttrString(msgpack, "unpackb");

    return PyModule_Create(&msgPack_module);
}

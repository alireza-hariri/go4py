
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/libgo_cool.h"

#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {
    Py_INCREF(Py_None);
    return Py_None;
}



static PyObject* go_cool_transform(PyObject* self, PyObject* args) { 
    char* s;
    if (!PyArg_ParseTuple(args, "s", &s))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    char* result = Transform(go_s);
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
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
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* go_cool_randomString(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    char* result = RandomString(n);
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* go_cool_myFunc(PyObject* self, PyObject* args) { 
    long a;
    char* b;
    if (!PyArg_ParseTuple(args, "ls", &a, &b))
        return NULL;
    GoString go_b = {b, (GoInt)strlen(b)};
    GoSlice result = MyFunc(a,go_b);
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

static PyObject* go_cool_randn2(PyObject* self, PyObject* args) { 
    double result = Randn2();
    return PyFloat_FromDouble(result);
}

static PyObject* go_cool_rands(PyObject* self, PyObject* args) { 
    long n;
    if (!PyArg_ParseTuple(args, "l", &n))
        return NULL;
    GoSlice result = Rands(n);
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
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
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

static PyObject* go_cool_fff(PyObject* self, PyObject* args) { 
    GoSlice result = Fff();
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

static PyObject* go_cool_slice_inp_test(PyObject* self, PyObject* args) { 
    PyObject* nums;
    if (!PyArg_ParseTuple(args, "O", &nums))
        return NULL;
    if (!PyList_Check(nums)) {
        PyErr_SetString(PyExc_TypeError, "Argument nums must be a list");
        return NULL;
    }
    int len = PyList_Size(nums);
    long* nums_CArray = malloc(len * sizeof(long));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(nums, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyLong");
            free(nums_CArray);
            return NULL;
        }
        nums_CArray[i] = PyLong_AsLong(item);
    }
    if (PyErr_Occurred()) {
        free(nums_CArray);
        return NULL;
    }
    GoSlice go_nums = {nums_CArray, (GoInt)len, (GoInt)len};
    Slice_inp_test(go_nums);
    free(nums_CArray);
    RETURN_NONE;
}

static PyObject* go_cool_someFunc(PyObject* self, PyObject* args) { 
    PyObject* nums;
    if (!PyArg_ParseTuple(args, "O", &nums))
        return NULL;
    if (!PyList_Check(nums)) {
        PyErr_SetString(PyExc_TypeError, "Argument nums must be a list");
        return NULL;
    }
    int len = PyList_Size(nums);
    long* nums_CArray = malloc(len * sizeof(long));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(nums, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyLong");
            free(nums_CArray);
            return NULL;
        }
        nums_CArray[i] = PyLong_AsLong(item);
    }
    if (PyErr_Occurred()) {
        free(nums_CArray);
        return NULL;
    }
    GoSlice go_nums = {nums_CArray, (GoInt)len, (GoInt)len};
    SomeFunc(go_nums);
    free(nums_CArray);
    RETURN_NONE;
}

static PyObject* go_cool_someFunc2(PyObject* self, PyObject* args) { 
    PyObject* nums;
    if (!PyArg_ParseTuple(args, "O", &nums))
        return NULL;
    if (!PyList_Check(nums)) {
        PyErr_SetString(PyExc_TypeError, "Argument nums must be a list");
        return NULL;
    }
    int len = PyList_Size(nums);
    GoString* nums_CArray = malloc(len * sizeof(GoString));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(nums, i);
        if (!PyUnicode_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyUnicode");
            free(nums_CArray);
            return NULL;
        }
        char* c_item = PyUnicode_AsUTF8(item);
        nums_CArray[i] = (GoString) {c_item, (GoInt)strlen(c_item)};
    }
    if (PyErr_Occurred()) {
        free(nums_CArray);
        return NULL;
    }
    GoSlice go_nums = {nums_CArray, (GoInt)len, (GoInt)len};
    SomeFunc2(go_nums);
    free(nums_CArray);
    RETURN_NONE;
}

static PyMethodDef Methods[] = {
    {"transform", go_cool_transform, METH_VARARGS, "transform"},
    {"add", go_cool_add, METH_VARARGS, "add"},
    {"replace", go_cool_replace, METH_VARARGS, "replace"},
    {"randomString", go_cool_randomString, METH_VARARGS, "randomString"},
    {"myFunc", go_cool_myFunc, METH_VARARGS, "myFunc"},
    {"randn2", go_cool_randn2, METH_VARARGS, "randn2"},
    {"rands", go_cool_rands, METH_VARARGS, "rands"},
    {"cosine", go_cool_cosine, METH_VARARGS, "cosine"},
    {"f2str2", go_cool_f2str2, METH_VARARGS, "f2str2"},
    {"str2f", go_cool_str2f, METH_VARARGS, "str2f"},
    {"fff", go_cool_fff, METH_VARARGS, "fff"},
    {"slice_inp_test", go_cool_slice_inp_test, METH_VARARGS, "slice_inp_test"},
    {"someFunc", go_cool_someFunc, METH_VARARGS, "someFunc"},
    {"someFunc2", go_cool_someFunc2, METH_VARARGS, "someFunc2"},
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

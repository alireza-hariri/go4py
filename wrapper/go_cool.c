
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



static PyObject* go_cool_f2str(PyObject* self, PyObject* args) {
    double a;
    if (!PyArg_ParseTuple(args, "d", &a))
        return NULL;
    char* result = F2str2(a);
    // GoString result = F2str(a);
    PyObject* py_result = PyUnicode_FromString(result); 
    free(result);
    return py_result;
}

static PyObject* go_cool_Str2f(PyObject* self, PyObject* args) {
    char* s;
    if (!PyArg_ParseTuple(args, "s", &s))
        return NULL;
    GoString go_s = {s, (GoInt)strlen(s)};
    double result = Str2f(go_s);
    PyObject* py_result = PyFloat_FromDouble(result);
    return py_result;
}


static PyObject* go_cool_Fff(PyObject* self, PyObject* args) {

    GoSlice result = Fff();
    // accessing element 0 of the slice
    char *elem0 = result.data;
    // printf("Element 0: %s\n", ((char**)result.data)[0]);
    // free(result.data);
    PyObject* py_result = PyUnicode_FromString(((char**)result.data)[0]);
    for (int i = 0; i < result.len; i++) {
        free(((char**)result.data)[i]);
    }
    free(result.data);

    return py_result;
}

static PyObject* go_cool_Map_test(PyObject* self, PyObject* args) {

    GoSlice result = Map_test();
    PyObject* py_result = PyDict_New();
    for (int i = 0; i < result.len; i++) {
        SS_KVPair kv = ((SS_KVPair*)result.data)[i];
        PyObject* v = PyUnicode_FromString(kv.v);
        PyObject* k = PyUnicode_FromString(kv.k);
        PyDict_SetItem(py_result, k, v);
        free(kv.k);
        free(kv.v);
        Py_DECREF(v);
        Py_DECREF(k);
        // printf("k->ob_refcnt: %ld\n", k->ob_refcnt);
        // printf("v->ob_refcnt: %ld\n", v->ob_refcnt);
    }
    free(result.data);
    // printf("py_result->ob_refcnt: %ld\n", py_result->ob_refcnt);
    return py_result;
}

static PyMethodDef GoCoolMethods[] = {
    {"add", go_cool_add, METH_VARARGS, "Add two numbers"},
    {"replace", go_cool_replace, METH_VARARGS, "Replace"},
    {"random_string", go_cool_random_string, METH_VARARGS, "RandomString"},
    {"f2str", go_cool_f2str, METH_VARARGS, "f2str"},
    {"str2f", go_cool_Str2f, METH_VARARGS, "str2f"},
    {"fff", go_cool_Fff, METH_VARARGS, "fff"},
    {"map_test", go_cool_Map_test, METH_VARARGS, "map_test"},
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
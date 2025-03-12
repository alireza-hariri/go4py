
#include <Python.h>


PyObject* custom_function(PyObject* self, PyObject* args) { 
    char* url;
    if (!PyArg_ParseTuple(args, "s", &url))
        return NULL;
    printf("the string: %s\n", url);
    return Py_None;
}
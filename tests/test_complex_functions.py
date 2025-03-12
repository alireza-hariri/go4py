import pytest
from goopy.code_gen.generate_wrapper import gen_fn
from goopy.types import GoFunction

test_cases = {}

fn = GoFunction(
    name="Func_8",
    arguments=[
        {"name": "a", "type": {"go_type": "[]int"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_8(PyObject* self, PyObject* args) { 
    PyObject* a;
    if (!PyArg_ParseTuple(args, "O", &a))
        return NULL;
    if (!PyList_Check(a)) {
        PyErr_SetString(PyExc_TypeError, "Argument a must be a list");    
        return NULL;
    }
    int len = PyList_Size(a);
    long* a_CArray = malloc(len * sizeof(long));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(strs, i);
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
    GoSlice go_a = {a_CArray, (GoInt)len, (GoInt)len};
    Func_8(go_a);
    free(a_CArray);
    return Py_None;
}"""
test_cases["int_slice_input"] = (fn, fn_res)


fn = GoFunction(
    name="Func_8",
    arguments=[
        {"name": "a", "type": {"go_type": "[]string"}},
        {"name": "b", "type": {"go_type": "[]*C.char"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_8(PyObject* self, PyObject* args) { 
    PyObject* a;
    PyObject* b;
    if (!PyArg_ParseTuple(args, "OO", &a, &b))
        return NULL;
    if (!PyList_Check(a)) {
        PyErr_SetString(PyExc_TypeError, "Argument a must be a list");    
        return NULL;
    }
    int len = PyList_Size(a);
    GoString* a_CArray = malloc(len * sizeof(GoString));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(strs, i);
        if (!PyUnicode_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List items must be PyUnicode");        
            free(a_CArray);
            return NULL;
        }
        char* c_item = PyUnicode_AsUTF8(item);
        a_CArray[i] = (GoString) {c_item, (GoInt)strlen(c_item)};
    }
    if (PyErr_Occurred()) {    
        free(a_CArray);
        return NULL;
    }
    GoSlice go_a = {a_CArray, (GoInt)len, (GoInt)len};
    if (!PyList_Check(b)) {
        PyErr_SetString(PyExc_TypeError, "Argument b must be a list");    
        free(a_CArray);
        return NULL;
    }
    int len = PyList_Size(b);
    char** b_CArray = malloc(len * sizeof(char*));
    for (int i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(strs, i);
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
    GoSlice go_b = {b_CArray, (GoInt)len, (GoInt)len};
    Func_8(go_a,go_b);
    free(a_CArray);
    free(b_CArray);
    return Py_None;
}"""
test_cases["string_slice_inputs"] = (fn, fn_res)


# print(gen_fn(fn, "test"))


@pytest.mark.parametrize("fn,fn_res", test_cases.values(), ids=test_cases.keys())
def test_gen_fn(fn, fn_res):
    assert gen_fn(fn, "test") == fn_res


"""
uv run -m tests.test_complex_functions
"""

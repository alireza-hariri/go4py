import pytest
from go4py.code_gen.generate_wrapper import gen_fn
from go4py.types import GoFunction

test_cases = {}

fn = GoFunction(
    name="Func_1",
    arguments=[
        {"name": "a", "type": {"go_type": "[]int"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_1(PyObject* self, PyObject* args) { 
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
}"""
test_cases["int_slice_input"] = (fn, fn_res)


fn = GoFunction(
    name="Func_2",
    arguments=[
        {"name": "a", "type": {"go_type": "[]string"}},
        {"name": "b", "type": {"go_type": "[]*C.char"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_2(PyObject* self, PyObject* args) { 
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
}"""
test_cases["string_slice_inputs"] = (fn, fn_res)
print(gen_fn(fn, "test"))

#####

fn = GoFunction(
    name="Func_3",
    arguments=[],
    return_type=[{"go_type": "[]int"}],
)
fn_res = """
static PyObject* test_func_3(PyObject* self, PyObject* args) { 
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
}"""
test_cases["return_int_slice"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_4",
    arguments=[],
    return_type=[{"go_type": "[]*C.char"}],
)
fn_res = """
static PyObject* test_func_4(PyObject* self, PyObject* args) { 
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
}"""
test_cases["return_string_slice"] = (fn, fn_res)


fn = GoFunction(
    name="Func_5",
    arguments=[],
    return_type=[{"go_type": "[][]byte"}, {"go_type": "[]*C.char"}],
)
fn_res = """
static PyObject* test_func_5(PyObject* self, PyObject* args) { 
    struct Func_5_return result = Func_5();
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
}"""
test_cases["return_string&byte_slices"] = (fn, fn_res)


@pytest.mark.parametrize("fn,fn_res", test_cases.values(), ids=test_cases.keys())
def test_gen_fn(fn, fn_res):
    assert gen_fn(fn, "test") == fn_res


"""
uv run -m tests.test_complex_functions
"""

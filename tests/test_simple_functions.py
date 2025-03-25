import pytest

from go4py.code_gen.generate_wrapper import gen_fn
from go4py.types import GoFunction


test_cases = {}

fn = GoFunction(
    name="Func_1",
    arguments=[],
    return_type=[{"go_type": "int"}],
)
fn_res = """
static PyObject* test_func_1(PyObject* self, PyObject* args) { 
    long result = Func_1();
    return PyLong_FromLong(result);
}"""
test_cases["simple_int_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_two",
    arguments=[],
    return_type=[{"go_type": "int"}, {"go_type": "float32"}],
)
fn_res = """
static PyObject* test_func_two(PyObject* self, PyObject* args) { 
    struct Func_two_return result = Func_two();
    PyObject* py_result = Py_BuildValue("lf", result.r0, result.r1);
    return py_result;
}"""
test_cases["tuple_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_3",
    arguments=[{"name": "a", "type": {"go_type": "int8"}}],
    return_type=[],
)

fn_res = """
static PyObject* test_func_3(PyObject* self, PyObject* args) { 
    char a;
    if (!PyArg_ParseTuple(args, "b", &a))
        return NULL;
    Func_3(a);
    RETURN_NONE;
}"""
test_cases["int8_arg"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_4",
    arguments=[{"name": "a", "type": {"go_type": "string"}}],
    return_type=[],
)

fn_res = """
static PyObject* test_func_4(PyObject* self, PyObject* args) { 
    char* a;
    if (!PyArg_ParseTuple(args, "s", &a))
        return NULL;
    GoString go_a = {a, (GoInt)strlen(a)};
    Func_4(go_a);
    RETURN_NONE;
}"""
test_cases["string_arg"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_x",
    arguments=[],
    return_type=[{"go_type": "*C.char"}],
)
fn_res = """
static PyObject* test_func_x(PyObject* self, PyObject* args) { 
    char* result = Func_x();
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}"""
test_cases["str_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_4x",
    arguments=[],
    return_type=[{"go_type": "*C.char"}, {"go_type": "[]byte"}],
)
fn_res = """
static PyObject* test_func_4x(PyObject* self, PyObject* args) { 
    struct Func_4x_return result = Func_4x();
    PyObject* py_result_r0 = result.r0==NULL ? GetPyNone() : PyUnicode_FromString(result.r0);
    free(result.r0);
    PyObject* py_result_r1 = result.r1.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r1.data, result.r1.len);
    free(result.r1.data);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}"""
test_cases["str&bytes_tuple_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_5",
    arguments=[],
    return_type=[{"go_type": "*C.char"}, {"go_type": "*C.char"}],
)
fn_res = """
static PyObject* test_func_5(PyObject* self, PyObject* args) { 
    struct Func_5_return result = Func_5();
    PyObject* py_result_r0 = result.r0==NULL ? GetPyNone() : PyUnicode_FromString(result.r0);
    free(result.r0);
    PyObject* py_result_r1 = result.r1==NULL ? GetPyNone() : PyUnicode_FromString(result.r1);
    free(result.r1);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}"""
test_cases["str_tuple_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_6",
    arguments=[{"name": "a", "type": {"go_type": "string"}}],
    return_type=[{"go_type": "*C.char"}],
)
fn_res = """
static PyObject* test_func_6(PyObject* self, PyObject* args) { 
    char* a;
    if (!PyArg_ParseTuple(args, "s", &a))
        return NULL;
    GoString go_a = {a, (GoInt)strlen(a)};
    char* result = Func_6(go_a);
    PyObject* py_result = result==NULL ? GetPyNone() : PyUnicode_FromString(result);
    free(result);
    return py_result;
}"""
test_cases["string_arg_string_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_7",
    arguments=[
        {"name": "a", "type": {"go_type": "string"}},
        {"name": "b", "type": {"go_type": "uint16"}},
        {"name": "c", "type": {"go_type": "string"}},
        {"name": "d", "type": {"go_type": "float64"}},
    ],
    return_type=[{"go_type": "bool"}],
)
fn_res = """
static PyObject* test_func_7(PyObject* self, PyObject* args) { 
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
}"""
test_cases["multi_arg_bool_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_8",
    arguments=[
        {"name": "a", "type": {"go_type": "*C.char"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_8(PyObject* self, PyObject* args) { 
    char* a;
    if (!PyArg_ParseTuple(args, "s", &a))
        return NULL;
    Func_8(a);
    RETURN_NONE;
}"""
test_cases["char_ptr_no_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_9",
    arguments=[
        {"name": "a", "type": {"go_type": "[]byte"}},
    ],
    return_type=[],
)
fn_res = """
static PyObject* test_func_9(PyObject* self, PyObject* args) { 
    PyObject* a;
    if (!PyArg_ParseTuple(args, "O", &a))
        return NULL;
    GoInt len_a = PyBytes_Size(a);
    GoSlice go_a = {PyBytes_AsString(a), len_a, len_a};
    Func_9(go_a);
    RETURN_NONE;
}"""
test_cases["bytes_input"] = (fn, fn_res)

######

fn = GoFunction(
    name="Func_10",
    arguments=[],
    return_type=[{"go_type": "[]byte"}],
)
fn_res = """
static PyObject* test_func_10(PyObject* self, PyObject* args) { 
    GoSlice result = Func_10();
    PyObject* py_result = result.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.data, result.len);
    free(result.data);
    return py_result;
}"""
test_cases["bytes_return"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_11",
    arguments=[],
    return_type=[{"go_type": "[]byte"}, {"go_type": "[]byte"}],
)
fn_res = """
static PyObject* test_func_11(PyObject* self, PyObject* args) { 
    struct Func_11_return result = Func_11();
    PyObject* py_result_r0 = result.r0.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r0.data, result.r0.len);
    free(result.r0.data);
    PyObject* py_result_r1 = result.r1.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.r1.data, result.r1.len);
    free(result.r1.data);
    PyObject* py_result = Py_BuildValue("OO", py_result_r0, py_result_r1);
    Py_DECREF(py_result_r0);
    Py_DECREF(py_result_r1);
    return py_result;
}"""
test_cases["byte_tuple_return"] = (fn, fn_res)


@pytest.mark.parametrize("fn,fn_res", test_cases.values(), ids=test_cases.keys())
def test_gen_fn(fn, fn_res):
    assert gen_fn(fn, "test") == fn_res


"""
uv run -m tests.test_simple_functions
"""

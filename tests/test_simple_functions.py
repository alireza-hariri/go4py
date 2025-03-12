import pytest

from goopy.code_gen.generate_wrapper import gen_fn
from goopy.types import GoFunction


test_cases = {}

fn = GoFunction(
    name="Fn1",
    arguments=[],
    return_type=[{"go_type": "int"}],
)
fn_res = """
static PyObject* test_fn1(PyObject* self, PyObject* args) { 
    long result = Fn1();
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
    return Py_None;
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
    return Py_None;
}"""
test_cases["string_arg"] = (fn, fn_res)

#####

fn = GoFunction(
    name="Func_5",
    arguments=[],
    return_type=[{"go_type": "*C.char"}, {"go_type": "*C.char"}],
)
fn_res = """
static PyObject* test_func_5(PyObject* self, PyObject* args) { 
    struct Func_5_return result = Func_5();
    PyObject* py_result = Py_BuildValue("ss", result.r0, result.r1);
    free(result.r0);
    free(result.r1);
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
    PyObject* py_result = PyUnicode_FromString(result);
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
    char result = Func_7(go_a,b,go_c,d);
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
    return Py_None;
}"""
test_cases["char_ptr_no_return"] = (fn, fn_res)


@pytest.mark.parametrize("fn,fn_res", test_cases.values(), ids=test_cases.keys())
def test_gen_fn(fn, fn_res):
    assert gen_fn(fn, "test") == fn_res


"""
uv run -m tests.test_simple_functions
"""

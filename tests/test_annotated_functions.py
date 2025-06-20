import pytest
from go4py.code_gen.generate_wrapper import gen_fn
from go4py.types import GoFunction

test_cases = {}

fn = GoFunction(
    name="Func_12",
    docs="[go4py] decode-msgpack\n",
    arguments=[],
    return_type=[{"go_type": "[]byte"}, {"go_type": "*C.char"}],
)
fn_res = """
static PyObject* test_func_12(PyObject* self, PyObject* args) { 
    struct Func_12_return result = Func_12();
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
}"""
test_cases["msgpack_decode_return"] = (fn, fn_res)


fn = GoFunction(
    name="Func_13",
    docs="[go4py] skip-binding\n",
    arguments=[],
    return_type=[{"go_type": "[]byte"}, {"go_type": "*C.char"}],
)
fn_res = "\n// function Func_13 is skipped due to 'skip-binding' annotation\n"
test_cases["skip-binding"] = (fn, fn_res)

fn = GoFunction(
    name="Func_14",
    docs="[go4py] no-gil\n",
    arguments=[{"name": "arg0", "type": {"go_type": "int"}}],
    return_type=[{"go_type": "[]byte"}],
)
fn_res = """
static PyObject* test_func_14(PyObject* self, PyObject* args) { 
    long arg0;
    if (!PyArg_ParseTuple(args, "l", &arg0))
        return NULL;
    GoSlice result;
    Py_BEGIN_ALLOW_THREADS
    result = Func_14(arg0);
    Py_END_ALLOW_THREADS
    PyObject* py_result = result.data==NULL ? GetPyNone() : PyBytes_FromStringAndSize(result.data, result.len);
    free(result.data);
    return py_result;
}"""
test_cases["no_gil_function"] = (fn, fn_res)

print(gen_fn(fn, "test"))


@pytest.mark.parametrize("fn,fn_res", test_cases.values(), ids=test_cases.keys())
def test_gen_fn(fn, fn_res):
    assert gen_fn(fn, "test") == fn_res


"""
uv run -m tests.test_annotations
"""

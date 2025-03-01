from goopy.copy_logic import gen_go_copy
from goopy.types import BoolType, FloatType, GoFunction, IntType, StringType, VarType, Variable


go_types_dict = {
    # here we assume 64-bit system
    "int": IntType(bits=64),
    "int8": IntType(bits=8),
    "int16": IntType(bits=16),
    "int32": IntType(bits=32),
    "int64": IntType(bits=64),
    "uint": IntType(bits=64, unsigned=True),
    "uint8": IntType(bits=8, unsigned=True),
    "uint16": IntType(bits=16, unsigned=True),
    "uint32": IntType(bits=32, unsigned=True),
    "uint64": IntType(bits=64, unsigned=True),
    "byte": IntType(bits=8, unsigned=True),
    "rune": IntType(bits=32),
    "float32": FloatType(bits=32),
    "float64": FloatType(bits=64),
    "bool": BoolType(),
    "string": StringType(),
    # "error": ErrorType(),
    # uintptr": None,
}


module_name = "go_cool"

"""
static PyObject* pygoo_sort(PyObject* self, PyObject* args) {
    PyObject* list;
    
    if (!PyArg_ParseTuple(args, "O", &list))
    return NULL;
    
    if (!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "argument must be a list");
        return NULL;
    }
    
    Py_ssize_t length = PyList_Size(list);
    long* vals = (long*)malloc(length * sizeof(long));
    
    for (Py_ssize_t i = 0; i < length; i++) {
        PyObject* item = PyList_GetItem(list, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "list items must be integers");
            return NULL;
        }
        vals[i] = PyLong_AsLong(item);
    }
    
    GoSlice slice = {vals, length, length};
    Sort(slice);
    
    // PyObject* result_list = PyList_New(length);
    // Update the Python list with sorted values
    for (Py_ssize_t i = 0; i < length; i++) {
        PyList_SetItem(list, i, PyLong_FromLong(vals[i]));
    }
    
    free(vals); 
    // return result_list;
    return Py_None;
}
"""


class ArgumentParser:
    arg_decl = []
    format_string = ""
    arg_list = []
    check_logic = ""
    copy_logic = ""

    def addArg(self, var: Variable):
        self.arg_decl.append(f"    {var.type.c_type()} {var.name};")
        if var.type.need_copy:
            self.copy_logic += gen_go_copy(var)
        self.format_string += var.type.fmt_str()
        self.arg_list.append("&" + var.name)

    def gen_ParseTuple(self):
        if len(self.arg_decl) == 0:
            return ""
        args = "\n".join(self.arg_decl)
        return f"""{args}
    if (!PyArg_ParseTuple(args, "{self.format_string}", {", ".join(self.arg_list)}))
        return NULL;"""

    def gen_checks(self):
        return ""

    def gen_copys(self):
        return self.copy_logic

    def gen_code(self):
        result = self.gen_ParseTuple()
        result += self.gen_checks()
        result += self.gen_copys()
        return result


def gen_fn_call(fn: GoFunction):
    args = [("go_" + a.name if a.type.need_copy else a.name) for a in fn.arguments]
    return f"    {fn.return_type.c_type()} result = {fn.name}({','.join(args)});"


class ReturnConverter:
    def __init__(self, t: VarType):
        self.t = t

    def gen_py_result(self):
        return f"    PyObject* py_result = {self.t.converter('result')};"

    def gen_copys(self):
        return ""

    def gen_free_and_refdec(self):
        return "\n    free(result);"

    def gen_code(self):
        result = self.gen_py_result()
        if self.t.need_copy:
            result += self.gen_copys()
            result += self.gen_free_and_refdec()
        return result


def gen_fn(fn: GoFunction):
    arg_parser = ArgumentParser()
    for arg in fn.arguments:
        arg_parser.addArg(arg)
    return_converter = ReturnConverter(fn.return_type)
    return f"""
static PyObject* go_cool_{fn.name}(PyObject* self, PyObject* args) {{
{arg_parser.gen_code()}
{gen_fn_call(fn)}
{return_converter.gen_code()}
    return py_result;
}}
"""


if __name__ == "__main__":
    import pyperclip

    fn = GoFunction(
        name="Map_test",
        return_type=StringType(),
        arguments=[
            # Variable(name="a", type=FloatType()),
            Variable(name="s", type=StringType()),
        ],
    )

    code = gen_fn(fn)
    pyperclip.copy(code)
    print(code)

    jj = fn.model_dump_json()

    fn2 = GoFunction.model_validate_json(jj)

    assert fn == fn2
"""
uv run -m goopy.generate_wrapper
"""

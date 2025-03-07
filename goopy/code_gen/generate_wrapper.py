from goopy.code_gen.copy_logic import gen_go_copy
from goopy.types import (
    BoolType,
    CStringType,
    FloatType,
    GoFunction,
    IntType,
    VarType,
    Variable,
)


module_name = "go_cool"


class ArgumentParser:
    def __init__(self):
        self.arg_decl = []
        self.format_string = ""
        self.arg_list = []
        self.check_logic = ""
        self.copy_logic = ""

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
        return f"""\n{args}
    if (!PyArg_ParseTuple(args, "{self.format_string}", {", ".join(self.arg_list)}))
        return NULL;"""

    def gen_checks(self):
        # TODO
        return ""

    def gen_copys(self):
        return self.copy_logic

    def gen_code(self):
        result = self.gen_ParseTuple()
        result += self.gen_checks()
        result += self.gen_copys()
        return result


def get_return_c_type(fn: GoFunction) -> str:
    if len(fn.return_type) == 0:
        raise Exception("no return type")
    elif len(fn.return_type) == 1:
        return fn.return_type[0].c_type()
    else:
        return f"struct {fn.name}_return"


def gen_fn_call(fn: GoFunction):
    args = [("go_" + a.name if a.type.need_copy else a.name) for a in fn.arguments]
    if len(fn.return_type) == 0:
        return f"    {fn.name}({','.join(args)});"
    else:
        return f"    {get_return_c_type(fn)} result = {fn.name}({','.join(args)});"


class ReturnConverter:
    def __init__(self, t: VarType, var="result"):
        self.t = t
        self.var = var
        self.py_name = "py_" + var.replace(".", "_")
        self.reduceable = type(t) in [IntType, FloatType, BoolType]

    def return_var(self):
        if self.reduceable:
            return self.t.converter(self.var)
        else:
            return self.py_name

    def gen_py_result(self):
        return f"\n    PyObject* {self.py_name} = {self.t.converter(self.var)};"

    def gen_copys(self):
        return ""

    def gen_free_and_refdec(self):
        if self.t.need_copy:
            return f"\n    free({self.var});"
        else:
            return ""

    def gen_code(self):
        if self.reduceable:
            return ""
        result = self.gen_py_result()
        if self.t.need_copy:
            result += self.gen_copys()
            result += self.gen_free_and_refdec()
        return result


def gen_fn(fn: GoFunction, module_name: str):
    arg_parser = ArgumentParser()
    for arg in fn.arguments:
        arg_parser.addArg(arg)
    if len(fn.return_type) == 0:
        return_code = "\n    return Py_None;"
    else:
        if len(fn.return_type) == 1:
            conv = ReturnConverter(fn.return_type[0])
            return_code = conv.gen_code()
            return_code += f"\n    return {conv.return_var()};"
        else:
            return_converters = [
                ReturnConverter(t, f"result.r{i}") for i, t in enumerate(fn.return_type)
            ]
            # return_code = "".join(c.gen_code() for c in return_converters)
            # return_code += (
            #     "\n    PyObject* py_result = PyTuple_New(" + str(len(fn.return_type)) + ");"
            # )
            # for i, c in enumerate(return_converters):
            #     return_code += f"\n    PyTuple_SetItem(py_result, {i}, {c.return_var()});"
            # return_code += "\n    return py_result;"

            code = '\n    PyObject* py_result = Py_BuildValue("'
            for t in fn.return_type:
                code += t.fmt_str()
            code += '"'
            for c in return_converters:
                code += f", {c.var}"
            code += ");"
            return_code = code
            for c in return_converters:
                return_code += c.gen_free_and_refdec()
            return_code += "\n    return py_result;"
    return f"""
static PyObject* {module_name}_{fn.lowercase_name()}(PyObject* self, PyObject* args) {{ {arg_parser.gen_code()}
{gen_fn_call(fn)}{return_code}
}}"""

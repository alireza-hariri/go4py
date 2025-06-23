from go4py.code_gen.copy_logic import gen_go_copy
from go4py.code_gen.slice import indent
from go4py.doc_annotation import DocAnnots, make_doc_annots
from go4py.types import (
    BoolType,
    ByteSliceType,
    CStringType,
    FloatType,
    GoFunction,
    GoStringType,
    IntType,
    SliceType,
    UnknownType,
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
        self.free_logic = ""

    def addArg(self, var: Variable):
        self.arg_decl.append(f"    {var.type.c_type()} {var.name};")
        if var.type.need_copy:
            copy_code, free_logic = gen_go_copy(var, self.free_logic)
            self.copy_logic += copy_code
            self.free_logic = free_logic

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
        return fn.return_type[0].cgo_type()
    else:
        return f"struct {fn.name}_return"


def gen_fn_call(fn: GoFunction, doc_annots: DocAnnots):
    args = [("go_" + a.name if a.type.need_copy else a.name) for a in fn.arguments]

    if len(fn.return_type) == 0:
        if doc_annots.no_gil:
            before = "    Py_BEGIN_ALLOW_THREADS\n"
            after = "\n    Py_END_ALLOW_THREADS"
        else:
            before = after = ""
        # call the function without return value
        return f"{before}    {fn.name}({','.join(args)});{after}"
    else:
        if doc_annots.no_gil:
            return f"""    {get_return_c_type(fn)} result;
    Py_BEGIN_ALLOW_THREADS
    result = {fn.name}({",".join(args)});
    Py_END_ALLOW_THREADS"""
        else:
            # call the function with return value
            return f"    {get_return_c_type(fn)} result = {fn.name}({','.join(args)});"


class ReturnConverter:
    def __init__(self, t: VarType, msgpack_decode: False, var="result"):
        self.t = t
        self.var = var
        self.py_name = "py_" + var.replace(".", "_")
        self.reduceable = type(t) in [IntType, FloatType, BoolType]
        self.is_msgpack = (type(t) is ByteSliceType) and msgpack_decode
        self.msgpack_name = self.py_name + "_msgpack" if self.is_msgpack else None

    def return_var(self):
        if self.reduceable:
            return self.t.converter(self.var)
        elif self.is_msgpack:
            return self.msgpack_name
        else:
            return self.py_name

    def nullable_var(self):
        T = type(self.t)
        if T in [SliceType, ByteSliceType]:
            return f"{self.var}.data"
        if T == GoStringType:
            return f"{self.var}.p"
        if T == CStringType:
            return self.var
        return None

    def gen_py_result(self):
        if type(self.t) is SliceType:
            item_t = self.t.item_type
            item_converter = ReturnConverter(item_t, False, "item")
            return f"""
    PyObject* {self.py_name};
    if ({self.nullable_var()} == NULL) {{
        {self.py_name} = GetPyNone();
    }} else {{
        {self.py_name} = PyList_New({self.var}.len);
        for (int i = 0; i < {self.var}.len; i++) {{
            {item_t.cgo_type()} item = (({item_t.cgo_type()}*){self.var}.data)[i];{indent(item_converter.gen_code(), 8)}
            PyList_SetItem({self.py_name}, i, {item_converter.return_var()});
        }}
    }}"""
        elif self.is_msgpack:
            return f"""
    PyObject* {self.msgpack_name};
    if ({self.var}.data!=NULL){{
        PyObject* {self.py_name} = PyBytes_FromStringAndSize({self.var}.data, {self.var}.len);
        {self.msgpack_name} = PyObject_CallFunctionObjArgs(unpackb, {self.py_name}, NULL);
        Py_DECREF({self.py_name});
    }}else{{
        {self.msgpack_name} = GetPyNone();
    }}"""

        else:
            return f"\n    PyObject* {self.py_name} = {self.nullable_var()}==NULL ? GetPyNone() : {self.t.converter(self.var)};"

    def gen_copys(self):
        return ""

    def gen_free_and_refdec(self):
        if self.t.need_free():
            if type(self.t) in [SliceType, ByteSliceType]:
                return f"\n    free({self.var}.data);"
            else:
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


def gen_return_code(fn: GoFunction, doc_annots: DocAnnots) -> str:
    return_types = fn.return_type

    code = ""


    if len(return_types) == 0:
        code += "\n    RETURN_NONE;"
    else:
        msgpack_decode = doc_annots.msgpack_decode
        if len(return_types) == 1:
            conv = ReturnConverter(return_types[0], msgpack_decode, "result")
            code += conv.gen_code() + f"\n    return {conv.return_var()};"
        else:
            return_converters = [
                ReturnConverter(t, msgpack_decode, f"result.r{i}")
                for i, t in enumerate(return_types)
            ]
            code = ""
            for c in return_converters:
                # breakpoint()
                if not c.reduceable:
                    code += c.gen_code()
            code += '\n    PyObject* py_result = Py_BuildValue("'
            for t in return_types:
                if c.reduceable:
                    code += t.fmt_str()
                else:
                    code += "O"
            code += '"'
            for c in return_converters:
                if c.reduceable:
                    code += f", {c.var}"
                else:
                    code += f", {c.return_var()}"
            code += ");"
            for c in return_converters:
                if not c.reduceable:
                    code += f"\n    Py_DECREF({c.return_var()});"

            code += "\n    return py_result;"
    return code


def gen_fn(fn: GoFunction, module_name: str) -> str:
    doc_annots = fn.doc_annots()

    if doc_annots.skip_binding:
        return f"\n// function {fn.name} is skipped due to 'skip-binding' annotation\n"

    arg_parser = ArgumentParser()
    for arg in fn.arguments:
        arg_parser.addArg(arg)
    return_code = gen_return_code(fn, doc_annots)

    return f"""
static PyObject* {module_name}_{fn.lowercase_name()}(PyObject* self, PyObject* args) {{ {arg_parser.gen_code()}
{gen_fn_call(fn, doc_annots)}{arg_parser.free_logic}{return_code}
}}"""

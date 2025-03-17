from go4py.types import UnknownType, Variable, VarType, GoStringType

need_c_convert = [GoStringType]


def indent(str, indent=4):
    return "\n".join([(indent * " " + line) if line else "" for line in str.split("\n")])


class ItemConverter:
    def __init__(
        self,
        item_type: VarType,
        free_resource_code: str,
        item_name="item",
        # indent = 0,
    ):
        self.t = item_type
        if type(self.t) is UnknownType:
            self.t = self.t.resolve()
        self.name = item_name
        self.free_resource_code = indent(free_resource_code, 8)

    def item_c_type(self):
        c_type = self.t.c_type()
        if c_type == "char*":
            c_type = "const char*"
        return c_type

    def item_cgo_type(self):
        cgo_type = self.t.cgo_type()
        if cgo_type == "char*":
            cgo_type = "const char*"
        return cgo_type

    def check_and_convert(self):
        pytype = self.t.check("").split("_Check")[0]  # TODO: this is hacky fix it
        result = f"""if (!{self.t.check(self.name)}) {{
            PyErr_SetString(PyExc_TypeError, "List items must be {pytype}");{self.free_resource_code}
            return NULL;
        }}"""
        if self.t.need_copy:
            result += f"\n        {self.item_c_type()} c_{self.name} = {self.t.from_py_converter(self.name)};"
        return result

    def final_value(self):
        if self.t.need_copy:
            match self.t:
                case GoStringType():
                    return f"(GoString) {{c_{self.name}, (GoInt)strlen(c_{self.name})}}"
                case _:
                    raise Exception("Not implemented")
        else:
            return self.t.from_py_converter(self.name)


def go_slice_from_py_list(inp_var: Variable, other_free_code=""):
    name = inp_var.name
    free_logic = f"""{other_free_code}
    free({name}_CArray);"""
    item_conv = ItemConverter(inp_var.type.item_type, free_logic, "item")
    copy_logic = f"""
    if (!PyList_Check({name})) {{
        PyErr_SetString(PyExc_TypeError, "Argument {name} must be a list");{indent(other_free_code)}
        return NULL;
    }}
    int len_{name} = PyList_Size({name});
    {item_conv.item_cgo_type()}* {name}_CArray = malloc(len_{name} * sizeof({inp_var.type.item_type.cgo_type()}));
    for (int i = 0; i < len_{name}; i++) {{
        PyObject* item = PyList_GetItem({name}, i);
        {item_conv.check_and_convert()}
        {name}_CArray[i] = {item_conv.final_value()};
    }}
    if (PyErr_Occurred()) {{{indent(free_logic)}
        return NULL;
    }}
    GoSlice go_{name} = {{{name}_CArray, (GoInt)len_{name}, (GoInt)len_{name}}};"""
    return copy_logic, free_logic

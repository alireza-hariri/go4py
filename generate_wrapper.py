from pydantic import BaseModel
from typing import TypeAlias

# we need to know:
module_name = "go_cool"


class IntType(BaseModel):
    bits: int = 64
    unsigned: bool = False

    def fmt_str(self) -> str:
        """Returns the format string for the given integer type."""
        if self.bits == 8:
            return "b" if not self.unsigned else "B"
        elif self.bits == 16:
            return "h" if not self.unsigned else "H"
        elif self.bits == 32:
            return "i" if not self.unsigned else "I"
        elif self.bits == 64:
            return "l" if not self.unsigned else "L"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")

    def c_var(self):
        if self.bits == 8:
            if self.unsigned:
                return "unsigned char"
            else:
                return "char"
        elif self.bits == 16:
            if self.unsigned:
                return "unsigned short"
            else:
                return "short"
        elif self.bits == 32:
            if self.unsigned:
                return "unsigned int"
            else:
                return "int"
        elif self.bits == 64:
            if self.unsigned:
                return "unsigned long"
            else:
                return "long"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")


go_types_dict = {
    # here we assume 64-bit system
    "int": IntType(bits=64, unsigned=False),
    "int8": IntType(bits=8, unsigned=False),
    "int16": IntType(bits=16, unsigned=False),
    "int32": IntType(bits=32, unsigned=False),
    "int64": IntType(bits=64, unsigned=False),
    "uint": IntType(bits=64, unsigned=True),
    "uint8": IntType(bits=8, unsigned=True),
    "uint16": IntType(bits=16, unsigned=True),
    "uint32": IntType(bits=32, unsigned=True),
    "uint64": IntType(bits=64, unsigned=True),
    "uintptr": None,
}


VarType: TypeAlias = IntType | None


class Variable(BaseModel):
    name: str | None
    type: VarType


class GoFunction(BaseModel):
    name: str
    return_type: VarType
    arguments: list[Variable]


module_name = "go_cool"
f = GoFunction(
    name="Add",
    return_type=IntType(),
    arguments=[
        Variable(name="a", type=IntType()),
        Variable(name="b", type=IntType()),
    ],
)
"""
static PyObject* go_cool_add(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    int result = (int)Add((GoInt)a, (GoInt)b);
    return PyLong_FromLong(result);
}
"""


class ArgumentParser:
    format_string = ""
    arg_decl = ""
    arg_list = ""

    def addArg(self, var: Variable):
        self.arg_decl += f"{var.type.c_var()} {var.name};\n"
        self.format_string += var.type.fmt_str()
        self.arg_list += f"&{var.name}, "

    def gen_ParseTuple(self):
        return f"""
        {self.arg_decl}
        
        if (!PyArg_ParseTuple(args, "{self.format_string}", {self.arg_list[:-2]}))
            return NULL;
        """

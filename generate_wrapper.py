from pydantic import BaseModel
from typing import TypeAlias

# we need to know:
module_name = "go_cool"


class IntType(BaseModel):
    name = "int"
    bits: int = 64
    unsigned: bool = False


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

    def addArg(self, var: Variable):
        match var.type:
            case IntType():
                self.format_string += "i"
                self.arg_decl += f"int {var.name};"
            case _:
                raise NotImplementedError(f"type {var.type.name} is not implemented")

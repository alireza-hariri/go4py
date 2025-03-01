from pydantic import BaseModel
from typing import ClassVar, Literal, TypeAlias

from abc import ABC, abstractmethod


class VarType(BaseModel, ABC):
    t: str
    need_copy: ClassVar[bool]

    @abstractmethod
    def c_type(self) -> str: ...

    @abstractmethod
    def fmt_str(self) -> str: ...

    @abstractmethod
    def converter(self, inp: str): ...


class IntType(VarType):
    t: Literal["int"] = "int"
    bits: int = 64
    unsigned: bool = False
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        _sign = "" if not self.unsigned else "unsigned "
        if self.bits == 8:
            return _sign + "char"
        elif self.bits == 16:
            return _sign + "short"
        elif self.bits == 32:
            return _sign + "int"
        elif self.bits == 64:
            return _sign + "long"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")

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

    def converter(self, inp):
        # PyLong_FromLong
        # TODO: fix this for other ints
        return f"PyLong_FromLong({inp})"


class FloatType(VarType):
    t: Literal["float"] = "float"
    bits: int = 64
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        if self.bits == 32:
            return "float"
        elif self.bits == 64:
            return "double"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")

    def fmt_str(self) -> str:
        if self.bits == 32:
            return "f"
        elif self.bits == 64:
            return "d"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")

    def converter(self, inp):
        if self.bits == 32:
            return f"PyFloat_FromFloat({inp})"
        elif self.bits == 64:
            return f"PyFloat_FromDouble({inp})"
        else:
            raise ValueError(f"Unsupported bit size: {self.bits}")


class BoolType(VarType):
    t: Literal["bool"] = "bool"
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        return "char"

    def fmt_str(self) -> str:
        return "d"

    def converter(self, inp):
        return f"PyBool_FromLong({inp})"


class StringType(VarType):
    t: Literal["string"] = "string"
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "char*"

    def fmt_str(self) -> str:
        return "s"

    def converter(self, inp):
        return f"PyUnicode_FromString({inp})"


class SliceType(VarType):
    t: Literal["slice"] = "slice"
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "PyObject*"

    def fmt_str(self) -> str:
        return "O"

    def converter(self, inp):
        return f"PyList_New({inp})"


RealType: TypeAlias = IntType | FloatType | BoolType | StringType


class Variable(BaseModel):
    name: str | None
    type: RealType


class GoFunction(BaseModel):
    name: str
    docs: str | None
    return_type: RealType
    arguments: list[Variable]

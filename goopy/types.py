from pydantic import BaseModel
from typing import ClassVar, Literal, TypeAlias

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


# cusotom exception: cgo limitation
class CgoLimitationError(Exception):
    pass


# go_types_dict = {
#     # here we assume 64-bit system
#     "int": IntType(bits=64),
#     "int8": IntType(bits=8),
#     "int16": IntType(bits=16),
#     "int32": IntType(bits=32),
#     "int64": IntType(bits=64),
#     "uint": IntType(bits=64, unsigned=True),
#     "uint8": IntType(bits=8, unsigned=True),
#     "uint16": IntType(bits=16, unsigned=True),
#     "uint32": IntType(bits=32, unsigned=True),
#     "uint64": IntType(bits=64, unsigned=True),
#     "byte": IntType(bits=8, unsigned=True),
#     "rune": IntType(bits=32),
#     "float32": FloatType(bits=32),
#     "float64": FloatType(bits=64),
#     "bool": BoolType(),
#     "string": StringType(),
#     # "error": ErrorType(),
#     # uintptr": None,
# }


class VarType(BaseModel, ABC):
    go_type: str
    need_copy: ClassVar[bool]

    @abstractmethod
    def c_type(self) -> str: ...

    @abstractmethod
    def fmt_str(self) -> str: ...

    @abstractmethod
    def converter(self, inp: str): ...


class IntType(VarType):
    go_type: Literal["int"] = "int"
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
    go_type: Literal["float64", "float32"] = "float"
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
    go_type: Literal["bool"] = "bool"
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        return "char"

    def fmt_str(self) -> str:
        return "d"

    def converter(self, inp):
        return f"PyBool_FromLong({inp})"


class CStringType(VarType):
    go_type: Literal["*C.char"] = "*C.char"
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "char*"

    def fmt_str(self) -> str:
        return "s"

    def converter(self, inp):
        return f"PyUnicode_FromString({inp})"


class GoStringType(VarType):
    go_type: Literal["string"] = "string"
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "char*"

    def fmt_str(self) -> str:
        return "s"

    def converter(self, inp):
        raise CgoLimitationError("Don't return string from cgo")


class BytesType(VarType):
    go_type: Literal["unsafe.Pointer"] = "unsafe.Pointer"
    need_copy: ClassVar[bool] = True
    size: str | None = None

    def c_type(self) -> str:
        return "void*"

    def fmt_str(self) -> str:
        raise NotImplementedError()

    def converter(self, inp):
        if self.size is None:
            logger.warning(
                "Converting cgo unsafe.Pointer to python bytes without knowing its size!! "
                "(may get trucated on the first zero byte)"
            )
            return f"PyBytes_FromString((char*){inp})"
        else:
            return NotImplementedError()


class NoneType(VarType):
    go_type: Literal[""] = ""
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        return ""

    def fmt_str(self) -> str:
        raise NotImplementedError()

    def converter(self, inp):
        return "Py_None"


# class SliceType(VarType):
#     go_type: Literal["slice"] = "slice"
#     need_copy: ClassVar[bool] = True

#     def c_type(self) -> str:
#         return "PyObject*"

#     def fmt_str(self) -> str:
#         return "O"

#     def converter(self, inp):
#         return f"PyList_New({inp})"


RealType: TypeAlias = IntType | FloatType | BoolType | GoStringType | CStringType | BytesType


class Variable(BaseModel):
    name: str | None
    type: RealType


class GoFunction(BaseModel):
    package: str
    name: str
    docs: str | None
    arguments: list[Variable]
    return_type: list[RealType]

    def model_post_init(self, __context):
        if self.return_type is None:
            self.return_type = NoneType()
        # lowercase fn.name

    def __str__(self) -> str:
        return f"{self.package}.{self.name}"

    def lowercase_name(self) -> str:
        return self.name.lower()[0] + self.name[1:]

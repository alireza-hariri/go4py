from pydantic import BaseModel
from typing import ClassVar, Literal, TypeAlias

from abc import ABC, abstractmethod
import logging

from go4py.doc_annotation import DocAnnots, make_doc_annots

logger = logging.getLogger(__name__)


class go4pyConfig(BaseModel):
    custom_incudes: list[str] = []
    custom_methods: list[str] = []
    output_file: str = "cpython-extention/bindings.c"
    module_name: str = ""


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

    @abstractmethod
    def from_py_converter(self, inp: str): ...

    @abstractmethod
    def check(self, inp): ...

    def need_free(self):
        return False

    def cgo_type(self) -> str:
        return self.c_type()

    @abstractmethod
    def py_type_hint(self): ...

class IntType(VarType):
    go_type: Literal[
        "int",
        "int8",
        "int16",
        "int32",
        "int64",
        "uint",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "byte",
        "rune",
    ] = "int"
    bits: int = 64
    unsigned: bool = False
    need_copy: ClassVar[bool] = False

    def model_post_init(self, __context):
        if self.go_type in ["int", "uint", "int64", "uint64"]:
            self.bits = 64
        elif self.go_type in ["int8", "uint8", "byte"]:
            self.bits = 8
        elif self.go_type in ["int16", "uint16"]:
            self.bits = 16
        elif self.go_type in ["int32", "uint32", "rune"]:
            self.bits = 32
        else:
            raise ValueError(f"Unsupported go type: {self.go_type}")
        if self.go_type in ["uint", "uint8", "uint16", "uint32", "uint64", "byte"]:
            self.unsigned = True
        else:
            self.unsigned = False

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
        if self.unsigned:
            return f"PyLong_FromUnsignedLong({inp})"
        else:
            return f"PyLong_FromLong({inp})"

    def from_py_converter(self, inp):
        if self.bits == 64:
            if self.unsigned:
                return f"PyLong_AsUnsignedLong({inp})"
            else:
                return f"PyLong_AsLong({inp})"
        elif self.bits == 32:
            if self.unsigned:
                raise Exception(
                    "no python function found for conversion to uint32 use int64, uint64 or int32 instead"
                )
            else:
                return f"PyLong_AsInt({inp})"
        else:
            raise Exception(
                f"no python function found for conversion to {self.c_type()} use int64, uint64 or int32 instead"
            )

    def check(self, inp):
        return f"PyLong_Check({inp})"
    
    def py_type_hint(self):
        return "int"

class FloatType(VarType):
    go_type: Literal["float64", "float32"] = "float64"
    bits: int = 64
    need_copy: ClassVar[bool] = False

    def model_post_init(self, __context):
        if self.go_type == "float32":
            self.bits = 32
        elif self.go_type == "float64":
            self.bits = 64
        else:
            raise ValueError(f"Unsupported float type: {self.go_type}")

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

    def from_py_converter(self, inp):
        if self.bits == 64:
            return f"PyFloat_AsDouble({inp})"
        else:
            logger.warning(f"casting double to float in C for {inp} (may overflow silently)")
            return f"(float)PyFloat_AsDouble({inp})"

    def check(self, inp):
        return f"PyFloat_Check({inp})"

    def py_type_hint(self): 
        return "float"

class BoolType(VarType):
    go_type: Literal["bool"] = "bool"
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        return "int"

    def fmt_str(self) -> str:
        return "p"

    def converter(self, inp):
        return f"PyBool_FromLong({inp})"

    def from_py_converter(self, inp):
        return f"PyObject_IsTrue({inp})"

    def check(self, inp):
        return None  # skip checking for bool

    def py_type_hint(self): 
        return "bool"

class CStringType(VarType):
    go_type: Literal["*C.char"] = "*C.char"
    need_copy: ClassVar[bool] = False

    def c_type(self) -> str:
        return "char*"

    def fmt_str(self) -> str:
        return "s"

    def converter(self, inp):
        return f"PyUnicode_FromString({inp})"

    def from_py_converter(self, inp):
        return f"PyUnicode_AsUTF8({inp})"

    def check(self, inp):
        return f"PyUnicode_Check({inp})"

    def need_free(self):
        return True

    def py_type_hint(self): 
        return "str"

class GoStringType(VarType):
    go_type: Literal["string"] = "string"
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "char*"

    def fmt_str(self) -> str:
        return "s"

    def converter(self, inp):
        raise CgoLimitationError("Don't return string from cgo")

    def from_py_converter(self, inp):
        return f"PyUnicode_AsUTF8({inp})"

    def check(self, inp):
        return f"PyUnicode_Check({inp})"

    def need_free(self):
        return True

    def cgo_type(self):
        return "GoString"

    def py_type_hint(self): 
        return "str"

class ByteSliceType(VarType):
    go_type: Literal["[]byte"] = "[]byte"
    need_copy: ClassVar[bool] = True
    size: str | None = None

    def c_type(self) -> str:
        return "PyObject*"

    def fmt_str(self) -> str:
        return "O"

    def converter(self, inp):
        return f"PyBytes_FromStringAndSize({inp}.data, {inp}.len)"

    def from_py_converter(self, inp):
        return NotImplementedError()

    def need_free(self):
        return True

    def check(self, inp):
        return f"PyBytes_Check({inp})"

    def cgo_type(self):
        return "GoSlice"

    def py_type_hint(self): 
        return "bytes"

class UnknownType(VarType):
    go_type: str
    need_copy: bool = True

    def c_type(self):
        raise NotImplementedError()

    def fmt_str(self): ...

    def converter(self, inp): ...

    def from_py_converter(self, inp): ...

    def check(self, inp): ...

    def need_free(self): ...

    def resolve(self):
        """try to convert this type to other types"""
        if self.go_type.startswith("[]"):
            t = self.go_type[2:]
            if t.startswith("(") and t.endswith(")"):
                t = t[1:-1]
            return SliceType(item_type={"go_type": t})
        else:
            raise CgoLimitationError(f"please check if you can use type: {self.go_type}")
    
    def py_type_hint(self): ...

SimpleTypes: TypeAlias = (
    IntType
    | FloatType
    | BoolType
    | GoStringType
    | CStringType
    | ByteSliceType
    | UnknownType  # Complex Types like slice will fall into this but will be resolved later
)


class SliceType(VarType):
    go_type: Literal["Slice"] = "Slice"
    item_type: SimpleTypes
    need_copy: ClassVar[bool] = True

    def c_type(self) -> str:
        return "PyObject*"

    def fmt_str(self) -> str:
        return "O"

    def converter(self, inp):
        raise NotImplementedError()

    def from_py_converter(self, inp):
        return NotImplementedError()

    def check(self, inp):
        return f"PyList_Check({inp})"

    def need_free(self):
        return True

    def cgo_type(self) -> str:
        return "GoSlice"
    
    def py_type_hint(self): 
        return f"list[{self.item_type.py_type_hint()}]"

RealType: TypeAlias = SimpleTypes | SliceType


class Variable(BaseModel):
    name: str | None
    type: RealType


class GoFunction(BaseModel):
    name: str
    arguments: list[Variable]
    return_type: list[RealType]
    package: str = ""
    docs: str = ""

    def __str__(self) -> str:
        return f"{self.package}.{self.name}"

    def lowercase_name(self) -> str:
        return self.name.lower()[0] + self.name[1:]

    def doc_annots(self) -> DocAnnots:
        return make_doc_annots(self.docs)

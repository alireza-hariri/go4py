import pytest

from go4py.types import IntType, CStringType, GoStringType, BoolType, FloatType, Variable


test_cases = {}
v = Variable(name="v", type={"go_type": "string"})
test_cases["string"] = (v, GoStringType)
v = Variable(name="v", type={"go_type": "*C.char"})
test_cases["c_char"] = (v, CStringType)
v = Variable(name="v", type={"go_type": "bool"})
test_cases["bool"] = (v, BoolType)


@pytest.mark.parametrize("var,expected_type", test_cases.values(), ids=test_cases.keys())
def test_other_types(var, expected_type):
    assert type(var.type) is expected_type


int_test_cases = {}

v = Variable(name="v", type={"go_type": "int"})
int_test_cases["int"] = (v, 64, False)
v = Variable(name="v", type={"go_type": "int8"})
int_test_cases["int8"] = (v, 8, False)
v = Variable(name="v", type={"go_type": "uint8"})
int_test_cases["uint8"] = (v, 8, True)
v = Variable(name="v", type={"go_type": "uint16"})
int_test_cases["uint16"] = (v, 16, True)
v = Variable(name="v", type={"go_type": "int32"})
int_test_cases["int32"] = (v, 32, False)
v = Variable(name="v", type={"go_type": "uint32"})
int_test_cases["uint32"] = (v, 32, True)
v = Variable(name="v", type={"go_type": "int64"})
int_test_cases["int64"] = (v, 64, False)
v = Variable(name="v", type={"go_type": "uint64"})
int_test_cases["uint64"] = (v, 64, True)
v = Variable(name="v", type={"go_type": "byte"})
int_test_cases["byte"] = (v, 8, True)
v = Variable(name="v", type={"go_type": "rune"})
int_test_cases["rune"] = (v, 32, False)


@pytest.mark.parametrize("var,bits,unsigned", int_test_cases.values(), ids=int_test_cases.keys())
def test_int_type(var, bits, unsigned):
    assert type(var.type) is IntType
    assert var.type.bits == bits
    assert var.type.unsigned == unsigned


float_test_cases = {}
v = Variable(name="v", type={"go_type": "float32"})
float_test_cases["float32"] = (v, 32)
v = Variable(name="v", type={"go_type": "float64"})
float_test_cases["float64"] = (v, 64)


@pytest.mark.parametrize("var,bits", float_test_cases.values(), ids=float_test_cases.keys())
def test_float_type(var, bits):
    assert type(var.type) is FloatType
    assert var.type.bits == bits

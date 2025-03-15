from goopy.code_gen.slice import go_slice_from_py_list
from goopy.types import ByteSliceType, GoStringType, SliceType, Variable


def gen_go_copy(v: Variable, free_logic: str):
    """
    this function will convert the c type to go type variable
    it will also prefixed the name with `go_`

    """
    match v.type:
        case GoStringType():
            copy_logic = f"""
    GoString go_{v.name} = {{{v.name}, (GoInt)strlen({v.name})}};"""
            return copy_logic, free_logic
        case SliceType():
            return go_slice_from_py_list(v, free_logic)
        case ByteSliceType():
            copy_logic = f"""
    GoInt len = PyBytes_Size({v.name});
    GoSlice go_{v.name} = {{PyBytes_AsString({v.name}), len, len}};"""
            return copy_logic, free_logic
        case _:
            breakpoint()
            raise NotImplementedError()

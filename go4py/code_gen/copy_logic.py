from go4py.code_gen.slice import go_slice_from_py_list
from go4py.types import ByteSliceType, GoStringType, SliceType, UnknownType, Variable


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
            if type(v.type.item_type) is UnknownType:
                raise Exception("Nested types are not supported! (except for [][]byte)")
            return go_slice_from_py_list(v, free_logic)
        case ByteSliceType():
            copy_logic = f"""
    GoInt len_{v.name} = PyBytes_Size({v.name});
    GoSlice go_{v.name} = {{PyBytes_AsString({v.name}), len_{v.name}, len_{v.name}}};"""
            return copy_logic, free_logic
        case _:
            raise NotImplementedError()

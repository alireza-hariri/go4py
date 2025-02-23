from goopy.types import StringType, Variable


def gen_go_copy(v: Variable):
    """
    this function will convert the c type to go type variable (may need a full copy)
    it will also prefixed the name with `go_`

    """
    match v.type:
        case StringType():
            return f"""
    GoString go_{v.name} = {{{v.name}, (GoInt)strlen({v.name})}};"""
        case _:
            return ""

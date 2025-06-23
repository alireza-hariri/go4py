

from pathlib import Path
from go4py.types import GoFunction


def gen_pyi_file(functions: list[GoFunction],dest: Path | str):
    imports = set()
    code  = " \n"
    for fn in functions:
        code += "\n"
        fn_pyi, fn_imports = function_py_interface(fn)
        code += fn_pyi
        imports |= fn_imports

    code = "\n".join(imports) + code
    with open(dest, "w") as f:
        f.write(code)


def function_py_interface(fn:GoFunction):
    imports = set()
    fn_pyi= f"def {fn.name}("
    fn_pyi += ', '.join([arg.name + ":" + arg.type.py_type_hint() for arg in fn.arguments])
    match len(fn.return_type):
        case 0:
            fn_pyi += "): ...\n"
        case 1:
            fn_pyi += f") -> {fn.return_type[0].py_type_hint()}: ...\n"
        case _:
            imports.add("from typing import Tuple")
            fn_pyi += f") -> Tuple[{', '.join([t.py_type_hint() for t in fn.return_type])}]: ...\n"

    return fn_pyi, imports

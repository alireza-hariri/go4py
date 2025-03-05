from pathlib import Path
from goopy.code_gen.generate_wrapper import gen_fn
from goopy.types import CgoLimitationError, GoFunction


def template(module: str, functions_code: list, methods: str):
    return f"""
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "../artifacts/build/lib{module}.h"
#include <string.h>

{functions_code}

static PyMethodDef Methods[] = {{{methods}
    {{NULL, NULL, 0, NULL}}
}};

static struct PyModuleDef {module}_module = {{
    PyModuleDef_HEAD_INIT,
    "{module}",
    NULL,
    -1,
    Methods
}};
PyMODINIT_FUNC PyInit_{module}(void) {{
    return PyModule_Create(&{module}_module);
}}
"""


def gen_binding_file(module: str, functions: list[GoFunction], dest: Path | str):
    functions_code = ""
    res_functions = []
    for fn in functions:
        try:
            functions_code += gen_fn(fn, module)
            res_functions.append(fn)
        except CgoLimitationError as e:
            print("[cgo limitation]", e, "-> skipping function: ", fn.name)
            continue

    methods = ""
    for fn in res_functions:
        fn_name = fn.lowercase_name()
        methods += f'\n    {{"{fn_name}", {module}_{fn_name}, METH_VARARGS, "{fn_name}"}},'
    with open(dest, "w") as f:
        f.write(template(module, functions_code, methods))

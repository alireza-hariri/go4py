import os
from pathlib import Path
from goopy.code_gen.generate_wrapper import gen_fn
from goopy.types import CgoLimitationError, GoFunction, GoopyConfig


def template(config: GoopyConfig, functions_code: list, methods: str):
    custom_incudes = "\n".join(config.custom_incudes)
    custom_methods = "".join(["\n    " + m for m in config.custom_methods])

    return f"""
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/lib{config.module_name}.h"
{custom_incudes}

{functions_code}

static PyMethodDef Methods[] = {{{methods}{custom_methods}
    {{NULL, NULL, 0, NULL}}
}};

static struct PyModuleDef {config.module_name}_module = {{
    PyModuleDef_HEAD_INIT,
    "{config.module_name}",
    NULL,
    -1,
    Methods
}};
PyMODINIT_FUNC PyInit_{config.module_name}(void) {{
    return PyModule_Create(&{config.module_name}_module);
}}
"""


def gen_binding_file(config: GoopyConfig, functions: list[GoFunction], dest: Path | str):
    module = config.module_name
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
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(template(config, functions_code, methods))

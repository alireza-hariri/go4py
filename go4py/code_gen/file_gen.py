import os
from pathlib import Path
from go4py.code_gen.generate_wrapper import gen_fn
from go4py.types import CgoLimitationError, GoFunction, go4pyConfig


def template(config: go4pyConfig, functions_code: list, methods: str):
    custom_incudes = "\n".join(config.custom_incudes)
    custom_methods = "".join(["\n    " + m for m in config.custom_methods])

    return f"""
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>
#include "../artifacts/build/lib{config.module_name}.h"
{custom_incudes}

#define RETURN_NONE Py_INCREF(Py_None) ; return Py_None
PyObject* GetPyNone() {{
    Py_INCREF(Py_None);
    return Py_None;
}}

PyObject* unpackb;
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
    PyObject* msgpack = PyImport_ImportModule("msgpack");
    if (msgpack == NULL) {{
       PyErr_SetString(PyExc_ImportError, "msgpack module not found");
        return NULL;
    }}
    unpackb = PyObject_GetAttrString(msgpack, "unpackb");

    return PyModule_Create(&{config.module_name}_module);
}}
"""


def gen_binding_file(config: go4pyConfig, functions: list[GoFunction], dest: Path | str):
    module = config.module_name
    functions_code = ""
    res_functions: list[GoFunction] = []
    for fn in functions:
        try:
            functions_code += "\n" + gen_fn(fn, module)
            res_functions.append(fn)
        except CgoLimitationError as e:
            print("[cgo limitation]", e, "-> skipping function: ", fn.name)
            continue
        except Exception as e:
            print("[error]", e, "-> skipping function: ", fn.name)
            continue

    methods = ""
    for fn in res_functions:
        if fn.doc_annots().skip_binding:
            continue
        fn_name = fn.lowercase_name()
        methods += f'\n    {{"{fn_name}", {module}_{fn_name}, METH_VARARGS, "{fn_name}"}},'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(template(config, functions_code, methods))

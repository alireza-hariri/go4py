from io import StringIO
import json
import os
import pdb
import subprocess
from pathlib import Path
import logging
from go4py.types import GoFunction, UnknownType
import IPython

logger = logging.getLogger(__name__)


def extract_functions_from_dot_h(file:StringIO):
    content = file.readlines()
    fn_names = set()
    for line in content:
        line = line.strip()
        if line.startswith("extern"):
            if line.endswith(");"):
                fn_names.add(line.split("(")[0].split(" ")[-1])
    return fn_names


def resolve_unknowns(fn:GoFunction):
    for i, t in enumerate(fn.return_type):
        if type(t) is UnknownType:
            fn.return_type[i] = t.resolve()
    for arg in fn.arguments:
        if type(arg.type) is UnknownType:
            arg.type = arg.type.resolve()

def get_go_functions(module_name: str) :
    """list all go exported functions in the go module"""

    # Path to the generated functions.json file
    functions_json_path = Path("artifacts/functions.json")
    header_file = Path(f"artifacts/build/lib{module_name}.h")
    
    with open(header_file, 'r') as file:
        fn_names = extract_functions_from_dot_h(file)

    # Check if the functions.json file was generated
    if not functions_json_path.exists():
        logger.error(f"Error: {functions_json_path} was not generated")
        raise FileNotFoundError(f"{functions_json_path} was not generated")

    # Read the functions.json file
    logger.debug(f"Reading functions from: {functions_json_path.name}")
    with open(functions_json_path, "r") as f:
        functions_data = json.load(f)

    with open(functions_json_path, "r") as f:
        functions_data = json.load(f)

    # Generate GoFunction objects from the JSON data
    go_functions = []
    for func_data in functions_data:
        try:
            go_function = GoFunction.model_validate(func_data)
            if go_function.name not in fn_names:
                logger.warning(f'function skipped: `{go_function.name}` is not in the header file. ({header_file})')
            else:
                resolve_unknowns(go_function)
                go_functions.append(go_function)

            # print(f"Parsed function: {go_function.name}")
        except Exception as e:
            logger.warning(
                f"function skipped: {func_data['name']} (set log-level to DEBUG for more info)"
            )
            logger.debug(e.__traceback__)
            # pdb.post_mortem()



    return go_functions




def convert_functions(go_functions:list[GoFunction]):
    result = {"functions":[]}
    for fn in go_functions:
        result["functions"].append({
            "name":fn.name,
            "arguments": [
                {
                    "name": arg.name,
                    "type": arg.type.py_type_hint()
                }
                for arg in fn.arguments
            ],
            "return_types": [
                t.py_type_hint()
                for t in fn.return_type
            ]
        })
    return result
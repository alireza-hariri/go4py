from pydantic import BaseModel
from go4py.code_gen.file_gen import gen_binding_file
from go4py.code_gen.gen_pyi import gen_pyi_file
from go4py.get_go_functions import get_go_functions
import argparse
import os
import yaml

from go4py.types import go4pyConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Go binding file")
    parser.add_argument("module_path", help="Name (or Path) of the module")
    return parser.parse_args()


def read_config():
    yaml_file = "go4py.yaml"
    if os.path.exists(yaml_file):
        with open(yaml_file, "r") as file:
            go4py_config = yaml.safe_load(file)
            return go4py_config
    return {}


if __name__ == "__main__":
    args = parse_args()
    module_path = args.module_path
    module_name = module_path.split("/")[-1]

    functions = get_go_functions(module_name)
    gen_pyi_file(functions, "__init__.pyi")


    config = go4pyConfig.model_validate(read_config())
    config.module_name = module_name

    gen_binding_file(config, functions, "cpython-extention/autogen_bindings.c")

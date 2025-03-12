from pydantic import BaseModel
from goopy.code_gen.file_gen import gen_binding_file
from goopy.get_go_functions import get_go_functions
import argparse
import os
import yaml

from goopy.types import GoopyConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Go binding file")
    parser.add_argument("module_path", help="Name (or Path) of the module")
    return parser.parse_args()


def read_config():
    yaml_file = "goopy.yaml"
    if os.path.exists(yaml_file):
        with open(yaml_file, "r") as file:
            goopy_config = yaml.safe_load(file)
            return goopy_config
    return {}


if __name__ == "__main__":
    args = parse_args()
    module_path = args.module_path
    functions = get_go_functions(module_path)
    module_name = module_path.split("/")[-1]

    config = GoopyConfig.model_validate(read_config())
    config.module_name = module_name

    gen_binding_file(config, functions, "cpython-extention/autogen_bindings.c")

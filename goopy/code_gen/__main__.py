from goopy.code_gen.file_gen import gen_binding_file
from goopy.get_go_functions import get_go_functions
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Go binding file")
    parser.add_argument("module_name", help="Name of the module")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    module_name = args.module_name
    functions = get_go_functions(module_name)
    gen_binding_file(module_name, functions, f"artifacts/{module_name}.c")

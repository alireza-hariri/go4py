from goopy.code_gen.file_gen import gen_binding_file
from goopy.go_functions import get_go_functions


if __name__ == "__main__":
    functions = get_go_functions()
    gen_binding_file("go_cool", functions, "wrapper/go_cool.c")

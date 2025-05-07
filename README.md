<div style="text-align: center;">
<img src="docs/img/go4py.png" width="290" style=""/>
<h2> go4py: ⚡ Supercharge your Python with Go ⚡ </h2>
</div>


<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/alireza-hariri/go4py"> <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alireza-hariri/go4py"> <img alt="GitHub repo Licence" src="https://img.shields.io/pypi/l/go4py">

[![Latest version](https://img.shields.io/pypi/v/go4py)](https://pypi.python.org/pypi/go4py) [![Supported python versions](https://img.shields.io/pypi/pyversions/go4py)](https://pypi.python.org/pypi/go4py) [![Downloads](https://static.pepy.tech/badge/go4py)](https://pepy.tech/projects/go4py) [![Downloads](https://static.pepy.tech/badge/go4py/month)](https://pepy.tech/project/go4py)
  


Do you ever wish Python were faster? `go4py` is here to help!
Enjoy the speed and simplicity of Go within Python! You just need to write bottlenecks of your Python code as some CGo functions. `go4py` will automatically generate the Python module for you!

Check the performance boost in our [benchmarks](docs/benchmark.md) and get a sense of how much faster it can be compared to basic Python! 🚀


## Installation
#### Linux
 1. Install Go
 2. `pip install go4py`
#### Windows
 1. Install Go
 2. Install [MSYS2](https://www.msys2.org/) and then install [mingw-toolchain](https://packages.msys2.org/groups/mingw-w64-x86_64-toolchain) inside it.
 3. Install `go4py` in a python vitrual exnvironment.
 4. Open a mingw shell and activate the venv inside it (e.g. `source venv/Scripts/activate`)
 5. Add Go to your PATH in the mingw shell (e.g., `export PATH=$PATH:"/c/Program Files/Go/bin/"`)


## Usage
 To create a Go package inside your Python project:
```shell
 go4py init <module_name>
```
 This will create a directory with the name `<module_name>` and add `go.mod` to your project.
 You can go to `<module_name>/src` directory and add your Go functions there.

 To build the Go package and generate bindings code for the Python module:
```shell
 go4py build <module_name>
```

You can now import the functions as methods of a python module:
```python
from <module_name> import <function_name>
```
Please note that we convert the function names' first character to lower case.

## How it works
There is a Makefile in the created directory with four major steps:
1. Parsing the Go code and extracting the signatures of the functions (the `functions.json` file).
2. Building an object file from Go code (`.a` and `.h` files).
3. Making a C wrapper for the Go functions as a Python native C extension.
4. Building a shared library from the generated C code (`__init__.so` file or `__init__.pyd` file).

The Makefile is actually quite readable, and you can modify it to your needs `go4py` will just run it 

## Documentation
Currently, we don't have good documentation, but you can check the [examples](examples) directory for some examples. And better than that, you can take a look at the [tests](tests) directory and see the codes that `go4py` generates.

### TODO
 - [x] Windows support
 - [x] no-GIL mode
 - [x] custom user bindings code
 - [x] make a helper function in go for passing Go slices to C
 - [ ] Warn the user if it uses string or other dynamically allocated types as a result.
 - [ ] Warn the user for an unexported function or wrong export with space (`// export`).
 - [ ] Generate type definitions file (`.pyi` file).
 - [ ] Can we make async Python functions or not?


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=alireza-hariri/go4py&type=Date)](https://www.star-history.com/#alireza-hariri/go4py&Date)
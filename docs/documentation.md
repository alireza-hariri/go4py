# Documentation

This library is a small code generator that creates a Python C-extension from a Go package with some exported functions. The generated code will create a wrapper for each exported function to work as a method of the final Python C-extension. The Go package should be a cgo package and functions should be marked as `//export`.

### Why a Library

Yes, you can write this generated code yourself specially if the number of functions is limited.  
But this library simplifies the process significantly and keeps maximum flexibility in the hands of the user.  
More importantly, you are dealing with C code, and both Python and Go objects are memory-unsafe. It's good idea to generate unsafe codes insted of writing it by hand.

## Getting Started

### 1. Installation

Follow the instructions on the [README page](/README.md),  
and make sure the following commands are available in your shell:

1. `gcc` & `make`  
2. `go4py`  
3. `go`

### 2. The `go4py init` Command

The `go4py init <module_path>` command creates a directory at `<module_path>` and also generates a `go.mod` file in the current directory with `go mod init` command (if one doesn't already exist).  
If you don't want a `go.mod` file in your current directory, run this command from somewhere else.

The full logic of this command can be found in the [cli.py](/go4py/cli.py#L40) file.

### 3. The `go4py build` Command

The `go4py build [module_path]` command looks for a `Makefile` in `[module_path]` and runs it (the default target).  
If no `Makefile` is found, it checks for `Makefile`s in the subdirectories of `[module_path]` (non-recursively) and runs them all. if `module_path` is not provided it will do the same thing for current directory.  
After running the Makefile, you can import the created Python module and use its functions.

The full logic of this command can be found in the [cli.py](/go4py/cli.py) file.

## Types

There are some limitations with Go types. Most of these come from the fact that you can't return normal pointers from cgo functions to outside of the Go runtime. Similarly, you can't return types containing Go pointers.  

However, there are workarounds (using unsafe pointers), and `go4py` provides utilities for this, which we will explain later.

Some solutions for Python-Go interoperability try to get too clever, hiding these limitations behind complex tricks. for example tracking all pointers in a map and passing keys instead of actual pointers.  
We don't do that here! This simplifies the library, removes a layer of abstraction, and makes the generated code is much more readable.  
You can always handle that yourself if needed.

| Go type                          | Intermediate C type | Python type | Notes |
|----------------------------------|----------------------|--------------|-------|
| `bool`                           | `int`                | `bool`       | -     |
| `int8`, `int16`, `int32` (`rune`), `int64` (`int`) | `char`, `short`, `int`, `long` | `int` | - |
| `float32`, `float64`             | `float`, `double`    | `float`      | -     |
| `string`                         | `char*`              | `str`        | Don't use this as a return type; see *note-1* |
| `*C.char`                        | `char*`              | `str`        | Use this instead of `string` for returning strings to Python |
| `[]byte`                         | `PyObject*`          | `bytes`      | See *note-1* |
| Slice (e.g. `[]int`)             | `PyObject*`          | `list`       | Works only for basic types; see *note-1* |

#### **Note-1**

These Go types contain internal pointers, so they cannot be returned by cgo functions to the outside world. (You can use them as function inputs without issue.)

- For `string`, the best solution is to use `C.CString` from Go's internal C package. This converts a Go string into a `*C.char`.
- For `slice`, use the helper function `go4py.CopySlice()` to create a copy of the slice with the pointer replaced by an unsafe pointer.  
  Make sure to use this only when returning the slice. If you call this function and forget to return the resulting slice, it will cause a memory leak.
### error

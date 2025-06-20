# Go4py Documentation

This library is a small code generator that creates a Python C-extension from a Go package with some exported functions. The generated code will create a wrapper for each exported function to work as a method of the final Python C-extension. The Go package should be a cgo package and functions should be marked as `//export`.

### Why a Library

Yes, you can write this generated code yourself specially if the number of functions is limited.  
But this library simplifies the process significantly and keeps maximum flexibility in the hands of the user.  
More importantly, you are dealing with C code, and both Python and Go objects are memory-unsafe. It's good idea to generate unsafe codes instead of writing it by hand.

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

# Types

There are some limitations with input and output variable types. Most of these limitations come from the fact that you can't return normal pointers from cgo functions to outside of the Go runtime. You can't also return types containing Go pointers.  

However, there are workarounds here (using unsafe pointers), and `go4py` is providing some utilities for this, which we will explain here.

Some solutions for Python-Go interoperability try to get too clever, hiding these limitations behind complex tricks. for example tracking all pointers in a map and passing keys instead of actual pointers.  
We don't do that here! This decesion will simplify the library, removes a layer of abstraction, and makes the generated code much more readable. You can always impelement these tricks youreslf if you  realy need them.

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
These Go types contain an internal go pointer, so they should not be returned by cgo functions to outside of the go runtime. 
But you can use them as function inputs without an issue.

- For `string`, the best solution is to use `C.CString` from Go's internal C package. This converts a Go string type into a `*C.char` type.  Make sure to use this only when returning the string. If you call this function and forget to return the result, it will cause a memory leak. 
example:
```go
import "C"
//export Example
func Example() *C.char {
    numbers := "hello C!"
    C.CString(numbers)
}
```
- For `slice`, use the helper function `go4py.CopySlice()` to create a copy of the slice with the pointer replaced by an unsafe pointer.  
**important:** Make sure to use this only when returning the slice. If you call this function and forget to return the resulting slice, it will cause a memory leak.  
example:
```go
import "C"
import "github.com/alireza-hariri/go4py/go_pkg/go4py"
//export Example_fn
func Example_fn() []int {
    numbers := []int{1, 2, 3}
    go4py.CopySlice(numbers)
}
```
### Errors
Go Error type is not a supported by go4py. (because they also have a go pointer inside them) but you can use other types to indecate an error.

We generally recommend to implement most of the error handling logic in the Go side but
you can easily extract the string value of the err object and pass it to python 

```go
import "C"
//export Example_fn2
func Example_fn2() (int, *C.char) {
    result, err := some_logic()
    if err != nil {
        return nil, C.CString(err.Error())
    }
    return result, nil
}
```
In this example None value in the second return variable means no-error happened

### Serialized types

To deal with the limitation of cgo for more complex return types we recommend to serialize these types inside the go runtime to some standard data transfer format and pass the Serialized data and there is some utilities provided by go4py to automatically deserialize these. This method have some overhead but its still very fast. (for example much faster than having a seprate service and passing network packets)
for example you can use `json` to pass any arbitrary type from go to python but for performance reasons we chose the `msgpack` witch is mush faster. 

To achieve this we use an special go4py [function annotation](#function-annotations) called `decode-msgpack`.
When a function is decorated with `decode-msgpack` the generated code will automatically decode all the the output variables of the `[]byte` type.

```go
package main
import "C"
import (
  	"github.com/vmihailenco/msgpack/v5"
    "github.com/alireza-hariri/go4py/go_pkg/go4py"
)

// [go4py] decode-msgpack
//export Example_fn1
func Example_fn1() ([]byte, *C.char) {
    some_map := map[string]string{"hello": "world", "example-key": "example-val"}
    b, err := msgpack.Marshal(some_map)
    if err != nil{
        return nil, C.CString(err.Error())
    }
    return go4py.CopySlice(b), nil
}

// [go4py] decode-msgpack
//export Example_fn2
func Example_fn2() ([]byte, *C.char) {
    type Item struct {
        Foo string
    }
    b, err := msgpack.Marshal(&Item{Foo: "bar"})
    if err != nil{
        return nil, C.CString(err.Error())
    }
    return go4py.CopySlice(b), nil
}

func main() {}
```
# Function-annotations

As you have seen in the last section all the go4py function annotations should start with a `//[go4py]` and then the name of annotation. some of of them also have arguments.


| Annotation              | Description |
|-------------------------|---------------------------------------|
| no-gil          |  Relese the GIL before calling this function. (using the `Py_BEGIN_ALLOW_THREADS` macro) | 
| decode-msgpack  |  Decode all the the output variables of type `[]byte` automaticly as a msgpack. |
| skip-binding    |  Skip auto-generating the wrapper code for this function in the c-extention. | 

usage:
```go
// [go4py] <annotation>
//export Some_fn
func Some_fn() {
    // ...
}
```

# Custom code
 If you need to impelement some custom code in the C side there is a way for this in go4py.
 for example when you need to implement a custom wrapper for a function and don't want the generated code.
 1. create a `go4py.yaml` file in the module directory beside the MakeFile with this content.
```yaml
 custom_incudes:
  - '#include "./custom.h"'
custom_methods:
  - '{"custom_function", custom_function, METH_VARARGS, "custom_function"},'
```
The lines in the `custom_incudes` will be added directly to the final generated c-extention in the header section. and similary the lines in the `custom_methods` will be added to the methods of the c-extention.
2. make a `custom.h` and `custom.c` file inside the `cpython-extention` directory.  
For example the header file will be something like this:
```c
#include <Python.h>
PyObject* custom_function(PyObject*, PyObject*) ;
```
3. Use `skip-binding` [function annotation](#function-annotations)
This annotion can be usefull here becuse you can prevent the auto-generated wapper method for any function if you want to impelement it yourself.  
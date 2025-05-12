
# Documentation
This lib is a small code generator that make a python c-extention form a Go pakage with a some exported functions. The genereted code will make a wrapper for each exported function in to work as a method of the final python c-extention. the go pakage should be a cgo specificly and function's should be marked as `//exported`.

### Why a library
oh yes you can write this generated code yourself. specialy if the number of functions is limited. 
But this library will simplify the process a lot and keeps the maximum flexibility in hand of user.
more importantly you are dealing with C code and we are memory unsafe on objecs of both side. both on python objects and go objects.

## Getting stated 

### 1. Installation
 Follow the instructions on the [readme page](/README.md).  
 and make soure to have these command availabe in your shell:
 1. gcc & make
 2. go4py
 3. go
### 2. The `go4py init` command
The `go4py init <module_path>` command will create a directory in the `<module_path>` and it also create a `go.mod` file in the current directory (if it don't have any).
so if you dont like the created `go.mod` in your root directory run this command from somewhere else.

The full logic of this command can be found in the [cli.py](/go4py/cli.py#l40) file.

### 2. The `go4py build` command
The `go4py build [module_path]` command will look at the `[module_path]` for a `makefile` and run it (runs the default target). if there is not any makefile it will check the directories of the `[module_path]` (not recursive) for makefiles and run them all. the default value of `module_path` is current directory.
after runing this makefile you are can import the ceated python module and use it's functions.

The full logic of this command can be found in the [cli.py](/go4py/cli.py) file.

## Types
There is some limitation with some go types. Most of these limitations is come from the fact that you are not allowed to simply return a normal pointer in cgo to the world outside of the go runtime. Similary you can't return types with normal go pointers inside them. but there is some workarownd (using unsafe pointers) and the go4py have some utils for this workarounds that we will explain later. 

Some of solutions for python-go interoperability gets too smart and hide these limitations behind some complex tricks like tracking all the pointers in a map and passing the key insted of pointer to the outside of the go runtime. 
We don't do that here! This simplify the liberary a lot, removes a layer of abstraction and makes the generated code much more readable. 
you can simply do these kind of thing yourself. no need to complicate and hide things here.

| Go type  | intermediate C type | Python type | notes|
|----------|-------------|-------------|---------|
| bool     | int         | bool        |-|
| int8, int16, int32(rune), int64(int) | char, short, int, long| int|-|
| float32, float64 | float, double | float|-|
| string | char* | str | don't use this for return value see *note-1 |
| *C.char | char* | str | use this type insted of `string` for returning strings to python|
| []byte | PyObject* | bytes | see *note-1   |
| slice (eg. []int)  |  PyObject* | list |will only worke for the above types, see *note-1 |
#### **note-1** 
These go types have a pointer inside them. so it can't be returned by a cgo functions to the outside of go runtime. (you use them as the function input without any problem)

for the `strings` the best solution is to use the `C.CString` from the go internal C pakage. That will convert your string to `*C.char`

for the `slice` type we have a helper function `go4py.copySlice()` that makes a copy of your slice but repaces the pointer inside with an unsafe pointer. make sure to use this function only when you are about to return the slice. if you use this function and forget to return the resulting slice then you will have a memory-leake for sure.

#### **note-2** 

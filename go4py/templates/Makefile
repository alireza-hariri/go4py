.PHONY: clean cpython-extention


# --- Platform-specific ---
# The file extention of a c-extention pakage is ".so" in linux and ".pyd" in windows
ifeq (,$(findstring NT,$(OS))) 
    # on Linux
    SHARED_LIB_EXT := .so
else
    # on Windows
    SHARED_LIB_EXT := .pyd 
endif


# -- Variables ---
MODULE_NAME := {{ module_name }}
BUILD_DIR := ./artifacts/build
PYTHON_INCLUDE=$(shell go4py py-include-path)
PYTHON3_LIB=$(shell go4py py-lib-path)
GO_FILES := $(shell find . -name "*.go")


# --- Targets ---
ARTIFACTS_DIR := ./artifacts
PARSER_TARGET := ${ARTIFACTS_DIR}/functions.json
GO_TARGET := ${BUILD_DIR}/lib${MODULE_NAME}.a
FINAL_TARGET := __init__${SHARED_LIB_EXT} # eg. __init__.so


# --- Build Flags ---
CFLAGS := -shared -fPIC -I${PYTHON_INCLUDE}
LDFLAGS := -L${BUILD_DIR} -l${MODULE_NAME} -L${PYTHON3_LIB} -lpython3


# --- Rules ---
all:  ${FINAL_TARGET}

${ARTIFACTS_DIR}:
	mkdir -p ${ARTIFACTS_DIR}

# 1. Parsing Go codes
${PARSER_TARGET}: ${GO_FILES} ${ARTIFACTS_DIR}
	@go4py textbox Step-1: "Parsing Go code"
	go4py parse ./src

# 2. Build Go files
${GO_TARGET}: ${PARSER_TARGET}
	@go4py textbox Step-2: "Building Go code"
	go build -buildmode=c-archive -o ${GO_TARGET} ./src

# 3. Generate Python wrapper code
cpython-extention: ${PARSER_TARGET} ${GO_TARGET}
	@go4py textbox Step-3: "Generating CPython wrapper code"
	python -m go4py.code_gen ${MODULE_NAME}

# 4. Build final shared library
${FINAL_TARGET}: cpython-extention
	@go4py textbox Step-4: "Building final shared library"
	gcc ${CFLAGS} -o ${FINAL_TARGET} $(wildcard cpython-extention/*.c) ${LDFLAGS}
	@go4py textbox Done!

# Clean build artifacts
clean:
	rm -rf ${BUILD_DIR} ./*${SHARED_LIB_EXT}

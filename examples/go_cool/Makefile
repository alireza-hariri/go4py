# This makefile have 4 steps:
#
# 1. Parsing Go code (extracting function signatures)
# 2. Building Go code into c-archive (.a file)
# 3. Generating Python wrapper code ()
# 4. Compiling everything into a shared library


.PHONY: clean go4py-wrapper c-build

# Configuration variables
MODULE_NAME := go_cool
BUILD_DIR := ./artifacts/build
ARTIFACTS_DIR := ./artifacts

GO_TARGET := ${BUILD_DIR}/lib${MODULE_NAME}.a
PARSER_TARGET := ${ARTIFACTS_DIR}/functions.json
OUTPUT_FILE := __init__.so

PYTHON_INCLUDE=/usr/include/python3.13
export PYTHONPATH=..

CFLAGS := -shared -fPIC
LDFLAGS := -L${BUILD_DIR} -l${MODULE_NAME}
GO_FILES := $(shell find . -name "*.go")

# Default target
all:  c-build


${ARTIFACTS_DIR}:
	@mkdir -p ${ARTIFACTS_DIR}

# 1. Parsing Go codes
${PARSER_TARGET}: ${GO_FILES} ${ARTIFACTS_DIR}
	@go4py textbox Step-1: "Parsing Go code"
	go4py parse ./src

# 2. Build Go files
${GO_TARGET}: ${GO_FILES} ${PARSER_TARGET}
	@go4py textbox Step-2: "Building Go code"
	go build -buildmode=c-archive -o ${BUILD_DIR}/lib${MODULE_NAME}.a ./src

# 3. Generate Python wrapper code
go4py-wrapper: ${PARSER_TARGET} ${GO_TARGET}
	@go4py textbox Step-3: "Generating CPython binding code"
	python -m go4py.code_gen ${MODULE_NAME}

# 4. Build final shared library
c-build: ${GO_TARGET} go4py-wrapper
	@go4py textbox Step-4: "Building final shared library"
	gcc ${CFLAGS} -o ${OUTPUT_FILE} $(wildcard cpython-extention/*.c) ${LDFLAGS} -I${PYTHON_INCLUDE}
	@go4py textbox Done!

# Clean build artifacts
clean:
	rm -rf ${BUILD_DIR} ./*.so

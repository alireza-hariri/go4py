# This makefile have 4 steps:
#
# 1. Parsing Go code (extracting function signatures)
# 2. Building Go code into c-archive (.a file)
# 3. Generating Python wrapper code ()
# 4. Compiling everything into a shared library


.PHONY: clean go4py-wrapper c-build

# Configuration variables
MODULE_NAME := custom_fn
BUILD_DIR := ./artifacts/build
ARTIFACTS_DIR := ./artifacts

GO_TARGET := ${BUILD_DIR}/lib${MODULE_NAME}.a
PARSER_TARGET := ${ARTIFACTS_DIR}/functions.json
OUTPUT_FILE := __init__.so

PYTHON_INCLUDE=/usr/include/python3.13
export PYTHONPATH=..

CFLAGS := -shared -fPIC
LDFLAGS := -L${BUILD_DIR} -l${MODULE_NAME}

# Default target
all: c-build

GO_FILES := $(wildcard *.go)

${ARTIFACTS_DIR}:
	mkdir -p ${ARTIFACTS_DIR}

# 1. Parsing Go codes
${PARSER_TARGET}: ${GO_FILES} ${ARTIFACTS_DIR}
	go4py parse .

# 2. Build Go files
${GO_TARGET}: ${GO_FILES}
	go build -buildmode=c-archive -o ${BUILD_DIR}/lib${MODULE_NAME}.a .

# 3. Generate Python wrapper code
go4py-wrapper: ${PARSER_TARGET}
	python -m go4py.code_gen ${MODULE_NAME}

# 4. Build final shared library
c-build: ${GO_TARGET} go4py-wrapper
	gcc ${CFLAGS} -o ${OUTPUT_FILE} $(wildcard cpython-extention/*.c) ${LDFLAGS} -I${PYTHON_INCLUDE}
	@echo "Build complete: ${OUTPUT_FILE}"

# Clean build artifacts
clean:
	rm -rf ${BUILD_DIR}/* ./*.so

# This makefile handles the process of:
# 1. Parsing Go code (extracting function signatures)
# 2. Building Go code into c-archive (.a file)
# 3. Generating Python wrapper code ()
# 4. Compiling everything into a shared library

.PHONY: clean goopy-wrapper c-build

# Configuration variables
MODULE_NAME := go_cool
BUILD_DIR := ./artifacts/build
ARTIFACTS_DIR := ./artifacts

GO_TARGET := ${BUILD_DIR}/lib${MODULE_NAME}.a
PARSER_TARGET := ${ARTIFACTS_DIR}/functions.json
OUTPUT_FILE := __init__.so

PYTHON_INCLUDE := /usr/include/python3.13
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
	go run ../goopy/parsing.go .

# 2. Build Go
${GO_TARGET}: ${GO_FILES}
	go build -buildmode=c-archive -o ${BUILD_DIR}/lib${MODULE_NAME}.a .

# Generate Python wrapper code
goopy-wrapper: ${PARSER_TARGET}
	python -m goopy.code_gen ${MODULE_NAME}

# Build final shared library
c-build: ${GO_TARGET} goopy-wrapper
	gcc ${CFLAGS} -o ${OUTPUT_FILE} ${ARTIFACTS_DIR}/${MODULE_NAME}_wrappers.c ${LDFLAGS} -I${PYTHON_INCLUDE}
	@echo "Build complete: ${OUTPUT_FILE}"

# Clean build artifacts
clean:
	rm -rf ${BUILD_DIR}/* ./*.so

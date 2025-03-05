# This makefile handles the process of:
# 1. Parsing Go code
# 2. Building Go code into a C archive
# 3. Generating Python wrapper code
# 4. Compiling everything into a shared library

.PHONY: clean

# Configuration variables
MODULE_NAME := {{module_name}}
BUILD_DIR := ./artifacts/build
ARTIFACTS_DIR := ./artifacts
OUTPUT_FILE := __init__.so

# Python configuration - detect version or use default
PYTHON_VERSION ?= $(shell python --version 2>&1 | sed 's/Python \([0-9]\+\.[0-9]\+\).*/\1/')
PYTHON_INCLUDE ?= /usr/include/python${PYTHON_VERSION}
export PYTHONPATH=..

# Compiler flags
CFLAGS := -shared -fPIC
LDFLAGS := -L${BUILD_DIR} -l${MODULE_NAME}

# Default target
all: c-build


${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}

# 1. Parsing Go codes
${ARTIFACTS_DIR}/functions.json: ${BUILD_DIR}
	go run ../goopy/parsing.go .

# 2. Build Go
${BUILD_DIR}/lib${MODULE_NAME}.a:
	go build -buildmode=c-archive -o ${BUILD_DIR}/lib${MODULE_NAME}.a .

# Generate Python wrapper code
goopy-wrapper: ${ARTIFACTS_DIR}/functions.json
	python -m goopy.code_gen ${MODULE_NAME}

# Build final shared library
c-build: goopy-wrapper go-build
	@echo "Building shared library..."
	@if [ ! -f "${ARTIFACTS_DIR}/${MODULE_NAME}.c" ]; then \
		echo "Error: ${ARTIFACTS_DIR}/${MODULE_NAME}.c not found"; \
		exit 1; \
	fi
	gcc ${CFLAGS} -o ${OUTPUT_FILE} ${ARTIFACTS_DIR}/${MODULE_NAME}.c ${LDFLAGS} -I${PYTHON_INCLUDE}
	@echo "Build complete: ${OUTPUT_FILE}"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf ${BUILD_DIR}/* ./*.so
	@echo "Clean complete"
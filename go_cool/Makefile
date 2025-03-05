.PHONY: go-build python-script c-build

export MODULE_NAME=go_cool
export PYTHON_INCLUDE=/usr/include/python3.13
export PYTHONPATH=..
all: c-build


parser: 
	go run ../goopy/parsing.go .

go-build: 
	go build -buildmode=c-archive -o ./artifacts/build/lib${MODULE_NAME}.a .

goopy-wrapper: parser
	python -m goopy.code_gen ${MODULE_NAME}

c-build: goopy-wrapper go-build
	gcc -shared -o ${MODULE_NAME}.so -fPIC artifacts/${MODULE_NAME}.c -L./artifacts/build -l${MODULE_NAME} -I${PYTHON_INCLUDE}

clean:
	rm -rf ./build/* ./*.so 
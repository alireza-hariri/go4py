.PHONY: go-build python-script c-build

export MODULE_NAME=go_cool
export PYTHON_INCLUDE=/usr/include/python3.13

all: c-build

go-build: 
	go build -buildmode=c-shared -o ./build/lib${MODULE_NAME}.so ./lib


generate-wrapper: go-build
	python generate_wrapper.py ${MODULE_NAME}


c-build: go-build
	gcc -shared -o ${MODULE_NAME}.so -fPIC wrapper/${MODULE_NAME}.c -L./build -l${MODULE_NAME} -I${PYTHON_INCLUDE}

clean:
	rm -rf ./build/* ./*.so 
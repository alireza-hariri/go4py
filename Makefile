.PHONY: go-build python-script c-build

export MODULE_NAME=go_cool
export PYTHON_INCLUDE=/usr/include/python3.13

all: c-build


parser: 
	go build  -o ./artifacts/build goopy/parsing.go


go-build: 
	go build -buildmode=c-archive -o ./artifacts/build/lib${MODULE_NAME}.a ./lib


goopy-wrapper: parser
	python -m goopy ${MODULE_NAME}


c-build: goopy-wrapper go-build
	gcc -shared -o ${MODULE_NAME}.so -fPIC artifacts/${MODULE_NAME}.c -L./artifacts/build -l${MODULE_NAME} -I${PYTHON_INCLUDE}

clean:
	rm -rf ./build/* ./*.so 
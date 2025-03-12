package main

import "C"

import (
	"io"
	"net/http"
)

//export Add
func Add(a int, b int) int {
	return a + b
}

//export GetRequest
func GetRequest(url string) *C.char {
	resp, err := http.Get(url)
	if err != nil {
		return C.CString(err.Error())
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString(string(body))
}

func main() {}

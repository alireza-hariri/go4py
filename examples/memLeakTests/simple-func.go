package main

import "C"
import (
	"fmt"
	"math/rand"

	"github.com/alireza-hariri/goopy/go_pkg/goopy"
)

//export Func_x
func Func_x() *C.char {
	// randomly return string or nil
	if rand.Intn(2) == 0 {
		return C.CString("Hello, World!")
	}
	return nil
}

//export Func_5
func Func_5() (*C.char, *C.char) {
	options := []string{"Hello", "Bonjour", "Hola", "Ciao", "Konnichiwa"}
	str1 := options[rand.Intn(len(options))]
	str2 := options[rand.Intn(len(options))]

	return C.CString(str1), C.CString(str2)
}

//export Func_6
func Func_6(a string) *C.char {
	if rand.Intn(2) == 0 {
		return C.CString(fmt.Sprintf("Processed: %s", a))
	}
	return nil
}

//export Func_8
func Func_8(a *C.char) {
	// randomly return string or nil
	a_str := C.GoString(a)
	if rand.Intn(10) == 0 {
		fmt.Println(a_str)
	}
}

//export Func_10
func Func_10() []byte {
	// Generate random byte slice
	length := 200
	data := make([]byte, length)
	for i := range data {
		data[i] = byte(rand.Intn(256))
	}
	if rand.Intn(2) == 0 {
		return nil
	}
	return goopy.CopySlice(data)
}

//export Func_11
func Func_11() ([]byte, []byte) {
	// Generate first random byte slice
	length1 := 200
	data1 := make([]byte, length1)
	for i := range data1 {
		data1[i] = byte(rand.Intn(256))
	}
	// Generate second random byte slice
	length2 := 200
	data2 := make([]byte, length2)
	for i := range data2 {
		data2[i] = byte(rand.Intn(256))
	}

	if rand.Intn(2) == 0 {
		return nil, goopy.CopySlice(data2)
	}
	if rand.Intn(2) == 0 {
		return goopy.CopySlice(data1), nil
	}
	return goopy.CopySlice(data1), goopy.CopySlice(data2)
}

func main() {}

package main

import "C"

import (
	"fmt"
	"math/rand"

	"github.com/alireza-hariri/go4py/go_pkg/go4py"
)

//export Func_1
func Func_1(a []int) {
	// Process the integer slice
	if len(a) > 0 {
		fmt.Println("First element of slice:", a[0])
	}
}

//export Func_2
func Func_2(a []string, b []*C.char) {
	// Process the string slice and C.char slice
	if len(a) > 0 {
		fmt.Println("First string:", a[0])
	}
	if len(b) > 0 && b[0] != nil {
		fmt.Println("First C string:", C.GoString(b[0]))
	}
}

//export Func_3
func Func_3() []int {
	// Generate random integer slice
	length := rand.Intn(10) + 1
	result := make([]int, length)
	for i := range result {
		result[i] = rand.Intn(100)
	}

	// Randomly return nil or the slice
	if rand.Intn(2) == 0 {
		return nil
	}
	return go4py.CopySlice(result)
}

//export Func_4
func Func_4() []*C.char {
	// Generate random string slice
	options := []string{"Hello", "World", "Go", "Python", "Integration"}
	result := make([]*C.char, 5)

	if rand.Intn(4) == 0 {
		return nil
	}

	for i := range result {
		// Randomly include nil values
		if rand.Intn(2) == 0 {
			result[i] = nil
		} else {
			result[i] = C.CString(options[rand.Intn(len(options))])
		}
	}
	return go4py.CopySlice(result)
}

//export Func_5_2
func Func_5_2() ([][]byte, []*C.char) {
	if rand.Intn(3) == 0 {
		return nil, nil
	}
	// Generate random byte slices
	byteSlices := go4py.MakeSlice[[]byte](10)

	for i := range byteSlices {
		if rand.Intn(2) == 0 {
			byteSlices[i] = nil
		} else {
			byteSlices[i] = go4py.MakeSlice[byte](20)
			for j := range byteSlices[i] {
				byteSlices[i][j] = byte(rand.Intn(256))
			}
		}
	}

	if rand.Intn(3) == 0 {
		return byteSlices, nil
	}
	// Generate random string slice
	options := []string{"Data", "Bytes", "Binary", "Content", "Information"}
	strSlice := make([]*C.char, 5)

	for i := range strSlice {
		// Randomly include nil values
		if rand.Intn(2) == 0 {
			strSlice[i] = nil
		} else {
			strSlice[i] = C.CString(options[rand.Intn(len(options))])
		}
	}

	return byteSlices, go4py.CopySlice(strSlice)
}

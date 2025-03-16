package main

import "C"

import (
	"math/rand"
	"strings"
	"sync"
	// "fmt"
)

var count int
var mtx sync.Mutex

type KV struct {
	Key   string
	Value string
}

const letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

//export Transform
func Transform(s string) *C.char {
	parts := strings.Split(s, "\n")
	res := strings.Join(parts, ":")
	return C.CString(res)
}

//export Add
func Add(a, b int) int {
	return a + b
}

//export Replace
func Replace(s string, old string, new string) *C.char {
	// fmt.Println(s)
	res := strings.Replace(s, old, new, -1)
	return C.CString(res)
	// return "alaki"
}

//export RandomString
func RandomString(n int) *C.char {
	res := make([]byte, n)
	for i := range res {
		res[i] = letters[rand.Intn(len(letters))]
	}
	return C.CString(string(res))
}

// [go4py] skip-binding
//
//export MyFunc
func MyFunc(a int, b string) [](int) {
	return []int{1, 2, 3, 4, 5}
}

//export Randn2
func Randn2() float64 {
	return rand.NormFloat64()
}

//export Rands
func Rands(n int) []float64 {
	res := make([]float64, n)
	for i := range res {
		res[i] = rand.Float64()
	}
	return res
}

// ggygnnmmm
func main() {

}

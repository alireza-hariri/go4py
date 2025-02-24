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

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"



//export Add
func Add(a, b int) int {
    return a + b
}


//export Replace
func Replace(s string, old string, new string ) *C.char {
    // fmt.Println(s)
    res:= strings.Replace(s, old, new, -1)
    return C.CString(res)
    // return "alaki"
}


//export RandomString
func RandomString(n int) *C.char  {
    res := make([]byte, n)
    for i := range res {
        res[i] = letterBytes[rand.Intn(len(letterBytes))]
    }
    return C.CString(string(res))
}

//export MyFunc
func MyFunc(a int, b string) *C.char {
    // fmt.Println(a)
    return C.CString(b)
}

// ggygygyg
func main() {

}


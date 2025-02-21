package main

import "C"

import (
	"sync"
)

var count int
var mtx sync.Mutex

// kmkk
//export Add
func Add(a, b int) int {
        return a + b
}


// jjjjjjj
//export somethingelse
func somethingelse(a, b int) (int,[]string) {
        return a + b, []string{"a","b"}
}

// ggygygyg
func main() {

}


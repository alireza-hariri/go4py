package main

/*
typedef struct {
    char* k;
    char* v;
} SS_KVPair;
*/
import "C"

import (
	"fmt"
	"math"
	"strconv"
	"unsafe"
)

//export Cosine
func Cosine(x float64) float64 {
	return math.Cos(x)
}

//export F2str
func F2str(x float64) string {
	return fmt.Sprintln(x)
}

//export F2str2
func F2str2(x float64) *C.char {
	return C.CString(fmt.Sprintln(x))
}

//export Str2f
func Str2f(s string) float64 {
	if s, err := strconv.ParseFloat(s, 64); err == nil {
		return s
	} else {
		return 0.0
	}
}

func allocSlice[T any](len int) []T {
	elemSize := int(unsafe.Sizeof(*new(T)))
	ptr := C.malloc(C.size_t(len * elemSize))
	sliceHeader := struct {
		p   unsafe.Pointer
		len int
		cap int
	}{p: ptr, len: len, cap: len}
	slice := *(*[]T)(unsafe.Pointer(&sliceHeader))
	return slice
}

//export Fff
func Fff() []*C.char {
	goStrings := []string{"hello", "world", "example"}
	cStrings := allocSlice[*C.char](len(goStrings))
	for i, s := range goStrings {
		cStrings[i] = C.CString(s)
	}
	return cStrings
}

//export Map_test
func Map_test() []C.SS_KVPair {
	_map := map[string]string{"hello": "world", "example": "example"}
	var c_map []C.SS_KVPair = allocSlice[C.SS_KVPair](len(_map))

	i := 0
	for k, v := range _map {
		c_map[i].k = C.CString(k)
		c_map[i].v = C.CString(v)
		i++
	}
	return c_map

}

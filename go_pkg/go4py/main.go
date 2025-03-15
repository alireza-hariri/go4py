package go4py

import "C"
import "unsafe"

// make a new go slice with unsafe pointer so it can be passable to C
func MakeSlice[T any](len int) []T {
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

// make a copy of go slice with unsafe pointer so it can be passable to C
func CopySlice[T any](a []T) []T {
	ptr := C.malloc(C.size_t(len(a) * int(unsafe.Sizeof(*new(T)))))
	sliceHeader := struct {
		p   unsafe.Pointer
		len int
		cap int
	}{p: ptr, len: len(a), cap: len(a)}
	slice := *(*[]T)(unsafe.Pointer(&sliceHeader))
	copy(slice, a)
	return slice
}

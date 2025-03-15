package main

import "C"

import (
	"fmt"
	"io"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"
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

func alaki() (*C.char, int) {

	return C.CString("hello"), 5
}

// //export Map_test2
// func Map_test2() (unsafe.Pointer, int) {
// 	_map := map[string]string{"hello": "world", "example": "example"}

// 	b, err := msgpack.Marshal(_map)

// 	if err != nil {
// 		fmt.Println(err)
// 		return nil, 0
// 	}
// 	// fmt.Println(b)
// 	return C.CBytes(b), len(b)
// }

//export Slice_inp_test
func Slice_inp_test(nums []int) {

}

func Tesing(native_map map[string]string) map[int][]int {
	fmt.Println(native_map)
	m := map[int]([]int){}
	m[1] = []int{1, 2, 3}
	m[2] = []int{4, 5, 6}
	return m
}

//export Http_test
func Http_test(url string) unsafe.Pointer {

	resp, err := http.Get(url)
	if err != nil {
		log.Print(err) // Changed from log.Fatal to log.Print to allow function to return
		return C.CBytes([]byte("err"))
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		return nil
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	return C.CBytes(body)
}

var httpClient *http.Client

func init() {
	httpClient = &http.Client{
		Transport: &http.Transport{
			MaxIdleConns:        100,              // Total max idle connections
			MaxIdleConnsPerHost: 100,              // Max idle connections per host
			IdleConnTimeout:     90 * time.Second, // Keep-alive duration
			DisableKeepAlives:   true,             // Enable keep-alive
			TLSHandshakeTimeout: 10 * time.Second, // TLS handshake timeout
			// Other Transport settings as needed (e.g., Proxy, TLSClientConfig)
		},
		Timeout: 30 * time.Second, // Overall request timeout
	}
}

func callback_inp(f func() int) {
	fmt.Println(f())
}

//export SomeFunc
func SomeFunc(nums []int) {
	fmt.Println(nums)
}

//export SomeFunc2
func SomeFunc2(nums []string) {
	fmt.Println(nums)
}

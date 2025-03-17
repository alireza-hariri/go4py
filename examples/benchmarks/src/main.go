package main

import "C"

import (
	"io"
	"math/rand/v2"
	"net/http"

	"github.com/alireza-hariri/go4py/go_pkg/go4py"
)

//export Add
func Add(a int) int {
	return a + 10000
}

//export Rand
func Rand() float64 {
	return rand.Float64()
}

//export Randn
func Randn() float64 {
	return rand.NormFloat64()
}

//export RandArray
func RandArray(n int) []float64 {
	slice := go4py.MakeSlice[float64](n)
	for i := range n {
		slice[i] = rand.Float64()
	}
	return slice
}

//export GetRequest
func GetRequest(url string) ([]byte, *C.char) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, C.CString(err.Error())
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, C.CString(err.Error())
	}
	return go4py.CopySlice(body), nil
}

//export Fibo
func Fibo(n int) int {
	if n <= 1 {
		return n
	}
	a, b := 0, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}

//export FindPrimes
func FindPrimes(n int) []int {
	primes := []int{}
	for i := 2; i < n; i++ {
		isPrime := true
		for j := 2; j < i; j++ {
			if i%j == 0 {
				isPrime = false
				break
			}
		}
		if isPrime {
			primes = append(primes, i)
		}
	}
	return go4py.CopySlice(primes)
}

func main() {}

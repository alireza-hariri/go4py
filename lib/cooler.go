


package main

import "C"

import (
        "math"
)
//export Cosine
func Cosine(x float64) float64 {
        return math.Cos(x)
}




package main

import "math"

const (
	ISO_FORMAT               = "2006-01-02"
	Float64EqualityThreshold = 1e-9
)

// AlmostEqual compares two float64 numbers
func AlmostEqual(a, b float64) bool {
	return math.Abs(a-b) <= Float64EqualityThreshold
}

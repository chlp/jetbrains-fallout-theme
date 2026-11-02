package main

import "fmt"

const threshold = 50

func scan(signal int) string {
	switch {
	case signal > threshold:
		return "strong"
	case signal > threshold/2:
		return "medium"
	}
	return "weak"
}

func main() {
	fmt.Println(scan(42))
}

package main

import "fmt"

func scan(signal int) string {
	if signal > 50 {
		return "strong"
	}
	return "weak"
}

func main() {
	fmt.Println(scan(42))
	fmt.Println("radio offline")
}

package main

import (
	"fmt"
	"strings"
)

// Terminal is a wasteland terminal.
// TODO: add hacking mini-game
type Terminal struct {
	Name    string `json:"name"`
	Locked  bool
	retries int
}

const maxRetries = 4

func (t *Terminal) Login(password string) error {
	if t.retries >= maxRetries {
		return fmt.Errorf("terminal %q locked: %d attempts", t.Name, t.retries)
	}
	t.retries++
	if strings.ToUpper(password) != "OVERSEER" {
		return undefinedErr
	}
	t.Locked = false
	return nil
}

func main() {
	term := &Terminal{Name: "WASTELAND TERMINAL", Locked: true}
	unused := 42
	if err := term.Login("overseer"); err != nil {
		fmt.Println("ERROR:", err)
	}
	fmt.Printf("%s: %v\n", term.Name, len([]int{1, 2, 3}))
}

package main

import "core:fmt"
import "core:os"
import "core:strconv"
import "core:strings"

is_safe :: proc(xs: []int) -> bool {
	safe, inc := true, xs[1] > xs[0]
	for i := 1; i < len(xs) && safe; i += 1 {
		d := xs[i] - xs[i - 1]
		safe = abs(d) >= 1 && abs(d) <= 3 && (inc && d >= 0 || !inc && d <= 0)
	}
	return safe
}

main :: proc() {
	data, _ := os.read_entire_file("input")
	lines := string(data)
	defer delete(data)

	xs, ys := make([dynamic]int), make([dynamic]int)
	defer delete(xs)
	defer delete(ys)

	res1, res2 := 0, 0
	for line in strings.split_lines_iterator(&lines) {
		clear(&xs)
		for num in strings.split(line, " ") {
			if x, ok := strconv.parse_int(num); ok do append(&xs, x)
		}
		safe := is_safe(xs[:])
		res1 += int(safe)
		if !safe {
			for i := 0; i < len(xs); i += 1 {
				clear(&ys)
				append(&ys, ..xs[:i])
				append(&ys, ..xs[i + 1:])
				if is_safe(ys[:]) {
					res2 += 1
					break
				}
			}
		}
	}

	fmt.printf("Part 1: %d\n", res1)
	fmt.printf("Part 2: %d\n", res1 + res2)
}

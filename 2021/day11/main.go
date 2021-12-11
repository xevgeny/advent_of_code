package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

const N = 10

type Octopus struct {
	level   int
	falshed bool
}

type Field = [N][N]*Octopus

type Game struct {
	field          Field
	flashes        int
	flashesPerStep int
	step           int
}

func (g *Game) flashNeighbours(n, m int) {
	for i := -1; i <= 1; i++ {
		for j := -1; j <= 1; j++ {
			if n+i >= 0 && n+i < N && m+j >= 0 && m+j < N {
				if !(i == 0 && j == 0) {
					g.mutateOctopus(n+i, m+j)
				}
			}
		}
	}
}

func (g *Game) mutateOctopus(n, m int) {
	octopus := g.field[n][m]
	octopus.level += 1
	if !octopus.falshed && octopus.level > 9 {
		g.flashesPerStep += 1
		octopus.falshed = true
		g.flashNeighbours(n, m)
	}
}

func (g *Game) NextState() {
	g.step += 1
	g.flashesPerStep = 0
	for n := 0; n < N; n++ {
		for m := 0; m < N; m++ {
			g.mutateOctopus(n, m)
		}
	}
	// reset energy level and flashed flag
	for n := 0; n < N; n++ {
		for m := 0; m < N; m++ {
			octopus := g.field[n][m]
			if octopus.level > 9 {
				octopus.level = 0
			}
			octopus.falshed = false
		}
	}
	g.flashes += g.flashesPerStep
	if g.flashesPerStep == N*N {
		fmt.Printf("Answer 2: %d\n", g.step)
		os.Exit(0)
	}
}

func (g *Game) MutateState(steps int) {
	for i := 0; i < steps; i++ {
		g.NextState()
	}
}

func (g Game) String() string {
	var sb strings.Builder
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			sb.WriteString(fmt.Sprintf("%v", g.field[i][j].level))
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

func loadNewGame(fname string) (*Game, error) {
	var field Field
	bytes, err := ioutil.ReadFile(fname)
	if err != nil {
		return nil, err
	}
	split := strings.Split(string(bytes), "\n")
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			level, err := strconv.Atoi(string(split[i][j]))
			if err != nil {
				return nil, err
			}
			field[i][j] = &Octopus{level, false}
		}
	}
	return &Game{field, 0, 0, 0}, nil
}

func main() {
	game, err := loadNewGame("./input")
	if err != nil {
		panic(err)
	}
	game.MutateState(100)
	fmt.Printf("Answer 1: %d\n", game.flashes)
	game.MutateState(200) // find answer 2
}

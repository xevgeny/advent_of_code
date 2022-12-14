N = 1000
S = (500, 0)


def draw_line(grid, x0, y0, x1, y1):
    if x0 == x1:  # vertical line
        for y in range(min(y0, y1), max(y0, y1) + 1): 
            grid[y][x0] = "#"
    else:  # horizontal line
        for x in range(min(x0, x1), max(x0, x1) + 1):
            grid[y0][x] = "#"


def draw_sand(grid, max_y):
    x, y = S
    while y <= max_y:
        if grid[y + 1][x] == "." or grid[y + 1][x - 1] == "." or grid[y + 1][x + 1] == ".":
            y += 1
            if grid[y][x] != ".":
                x += -1 if grid[y][x - 1] == "." else 1
        else:
            if grid[y][x] == "o":  # source is blocked
                return False
            else:
                grid[y][x] = "o"
                return True
    return False


if __name__ == "__main__":
    max_y = 0
    input = open("input", "r").read().splitlines()
    grid = [["." for x in range(N)] for y in range(N)]
    for line in input:
        vecs = [[int(c) for c in vec.split(",")] for vec in line.split(" -> ")]
        x, y = vecs[0]
        max_y = max(max_y, y)
        for i in range(1, len(vecs)):
            nx, ny = vecs[i]
            draw_line(grid, x, y, nx, ny)
            x, y = nx, ny
            max_y = max(max_y, y)

    grid1 = [row[:] for row in grid]
    it = 0
    while draw_sand(grid1, max_y): 
        it += 1
    print(f"Part 1: {it}")

    max_y += 2
    grid2 = [row[:] for row in grid]
    grid2[max_y] = ["#" for _ in range(N)]
    it = 0
    while draw_sand(grid2, max_y): 
        it += 1
    print(f"Part 2: {it}")

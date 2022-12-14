def add_sand(obs, max_y):  # obs - set of obstacles, sand or rocks
    x, y = (500, 0)
    while y <= max_y:
        if (x, y+1) not in obs:
            y += 1
        elif (x-1, y+1) not in obs:
            x -= 1
            y += 1
        elif (x+1, y+1) not in obs:
            x += 1
            y += 1
        else:
            if (x, y) in obs:  # source is blocked
                return False
            else:
                obs.add((x, y))
                return True
    return False


if __name__ == "__main__":
    max_y = 0
    rocks = set()
    input = open("input", "r").read().splitlines()
    for line in input:
        segments = [[int(c) for c in vec.split(",")] for vec in line.split(" -> ")]
        x, y = segments[0]
        max_y = max(max_y, y)
        for i in range(1, len(segments)):
            nx, ny = segments[i]
            if x == nx:  # vertical line
                for yy in range(min(y, ny), max(y, ny) + 1): 
                    rocks.add((x, yy))
            else:  # horizontal line
                for xx in range(min(x, nx), max(x, nx) + 1):
                    rocks.add((xx, y))
            x, y = nx, ny
            max_y = max(max_y, y)

    obs1 = rocks.copy()
    it = 0
    while add_sand(obs1, max_y): 
        it += 1
    print(f"Part 1: {it}")

    max_y += 2
    obs2 = rocks.copy()
    [obs2.add((x, max_y)) for x in range(1000)]
    it = 0
    while add_sand(obs2, max_y): 
        it += 1
    print(f"Part 2: {it}")

def possible_id(line):
    id, game = line.split(":")
    for round in game.split(";"):
        r, g, b = 0, 0, 0
        for cube in round.split(","):
            match cube.split():
                case [i, "red"]:
                    r += int(i)
                case [i, "green"]:
                    g += int(i)
                case [i, "blue"]:
                    b += int(i)
        if r > 12 or g > 13 or b > 14:
            return 0
    return int(id.split(" ")[1])


def power(line):
    _, game = line.split(":")
    R, G, B = 0, 0, 0
    for round in game.split(";"):
        r, g, b = 0, 0, 0
        for cube in round.split(","):
            match cube.split():
                case [i, "red"]:
                    r += int(i)
                case [i, "green"]:
                    g += int(i)
                case [i, "blue"]:
                    b += int(i)
        R, G, B = max(R, r), max(G, g), max(B, b)
    return R * G * B


with open("input", "r") as f:
    lines = f.read().splitlines()

    part1 = sum([possible_id(line) for line in lines])
    print(f"Answer 1: {part1}")

    part2 = sum([power(line) for line in lines])
    print(f"Answer 2: {part2}")

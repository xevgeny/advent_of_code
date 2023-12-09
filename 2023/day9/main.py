def find(row, fwd):
    q = [row]
    while not all(x == q[-1][0] for x in q[-1]):
        xs = []
        for i in range(len(q[-1]) - 1):
            xs.append(q[-1][i + 1] - q[-1][i])
        q.append(xs)
    next = 0
    for xs in q[::-1]:
        next = next + xs[-1] if fwd else xs[0] - next
    return next


with open("input", "r") as f:
    rows = [[int(x) for x in xs.split()] for xs in f.read().splitlines()]

    part1 = sum([find(row, True) for row in rows])
    print(f"Part 1: {part1}")

    part2 = sum([find(row, False) for row in rows])
    print(f"Part 2: {part2}")

with open("input", "r") as f:
    pairs = [[int(x) for x in line.split()] for line in f.readlines()]
    lhs, rhs = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
    print(f"Part 1: {sum([abs(pair[1] - pair[0]) for pair in zip(sorted(lhs), sorted(rhs))])}")
    print(f"Part 2: {sum([x * rhs.count(x) for x in lhs])}")

import math


def parse(mapping):
    return [[int(x) for x in xs.split()] for xs in mapping]


def find(x, mapping):
    for dst, src, rng in mapping:
        if src <= x < src + rng:
            return x - src + dst
    return x


def find_ranges(ranges, mapping):
    res = []
    for dst, src, rng in mapping:
        b0, b1 = src, src + rng
        for a0, a1 in ranges:
            # find if A overlaps with B
            if min(a1, b1) > max(a0, b0):
                res.append((max(a0, b0) - src + dst, min(a1, b1) - src + dst))
    return res


with open("input", "r") as f:
    seeds, *mappings = f.read().split("\n\n")
    seeds = [int(x) for x in seeds.split(":")[1].split()]
    mappings = [parse(mapping.split("\n")[1:]) for mapping in mappings]

    min_x = math.inf
    for seed in seeds:
        x = seed
        for mapping in mappings:
            x = find(x, mapping)
        min_x = min(x, min_x)
    print(f"Part 1: {min_x}")

    min_x = math.inf
    seed_pairs = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for seed, seed_rng in seed_pairs:
        ranges = [(seed, seed + seed_rng)]
        for mapping in mappings:
            ranges = find_ranges(ranges, mapping)
        min_x = min(min_x, min([x for x, _ in ranges]))
    print(f"Part 2: {min_x}")

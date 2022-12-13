from functools import cmp_to_key


def compare(l, r):
    if type(l) == list and type(r) == list:
        if len(l) > 0 and len(r) > 0:
            res = compare(l[0], r[0])
            return compare(l[1:], r[1:]) if res is None else res
        if len(l) == len(r) == 0:  # both lists are empty
            return None
        return len(l) == 0  # left side ran out of items

    if type(l) == list and type(r) != list:
        return compare(l, [r])

    if type(l) != list and type(r) == list:
        return compare([l], r)

    return None if l == r else l < r


if __name__ == "__main__":
    input = open("input", "r").read()

    pairs = [pair.split("\n") for pair in input.split("\n\n")]
    n = sum([i for i, (l, r) in enumerate(pairs, 1) if compare(eval(l), eval(r))])
    print(f"Part 1: {n}")

    sep1 = [[2]]
    sep2 = [[6]]
    all = [eval(packet) for packet in input.splitlines() if packet != ""] + [sep1, sep2]
    all.sort(key=cmp_to_key(lambda l, r: -1 if compare(l, r) else 1))
    pos1 = all.index(sep1) + 1
    pos2 = all.index(sep2) + 1
    print(f"Part 2: {pos1 * pos2}")

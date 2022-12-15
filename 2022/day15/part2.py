import re


def find_intersection_y(Y, Sx, Sy, Bx, By, xs):
    sb = abs(Sx - Bx) + abs(Sy - By)  # sensor to beacon distance
    if Sy - sb <= Y <= Sy + sb:
        sr = abs(Sy - Y)  # sensor to row projection
        delta = sb - sr
        x0, x1 = min(Sx - delta, Sx + delta), max(Sx - delta, Sx + delta)
        xs.add((x0, x1))


def merge(xs):
    for i, (a0, a1) in enumerate(xs):
        for j, (b0, b1) in enumerate(xs):
            if i == j:
                continue
            if a0 <= b0 <= a1 or b0 <= a0 <= b1:
                xs.remove((a0, a1))
                xs.remove((b0, b1))
                xs.add((min(a0, b0), max(a1, b1)))
                return merge(xs)


if __name__ == "__main__":
    N = 4000000
    lines = open("input", "r").read().splitlines()
    input = [[int(n) for n in re.findall(r"-?\d+", line)] for line in lines]

    for y in range(N + 1):
        if y % 100000 == 0:
            print(f"row: {y}")

        xs = set()
        for (Sx, Sy, Bx, By) in input:
            find_intersection_y(y, Sx, Sy, Bx, By, xs)

        merge(xs)

        n = 0
        for x0, x1 in xs:
            if 0 <= x0 <= x1 <= N:
                n += x1 - x0
            elif x0 <= 0 <= x1 <= N:
                n += x1
            elif 0 <= x0 <= N <= x1:
                n += N - x0
            elif x0 <= 0 <= N <= x1:
                n += N

        if n != N:  # only single row has this property
            x = sorted(xs)[0][1] + 1  # is this always the case?
            print(f"Part 2: {x*N + y}")
            break

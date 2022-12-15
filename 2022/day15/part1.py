import re


def find_intersection_y(Y, Sx, Sy, Bx, By, xs):
    sb = abs(Sx - Bx) + abs(Sy - By)  # sensor to beacon distance
    if Sy - sb <= Y <= Sy + sb:
        sr = abs(Sy - Y)  # sensor to row projection
        delta = sb - sr
        x0, x1 = min(Sx - delta, Sx + delta), max(Sx - delta, Sx + delta)
        for x in range(x0, x1 + 1):
            xs.add(x)


if __name__ == "__main__":
    Y = 2000000
    xs = set()
    beacons = set()

    lines = open("input", "r").read().splitlines()
    for line in lines:
        Sx, Sy, Bx, By = map(int, re.findall(r"-?\d+", line))
        print(f"Sx: {Sx}, Sy: {Sy}, Bx: {Bx}, By: {By}")
        find_intersection_y(Y, Sx, Sy, Bx, By, xs)
        beacons.add((Bx, By))

    for Bx, By in beacons:
        if By == Y and Bx in xs:
            xs.remove(Bx)

    print(f"Part 1: {len(xs)}")

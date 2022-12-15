import re

N = 2000000
row = set()


def update_row(Sx, Sy, Bx, By):
    dist = abs(Sx - Bx) + abs(Sy - By)
    for x in range(Sx - dist, Sx + dist + 1):
        for y in range(Sy - dist, Sy + dist + 1):
            if y == N and abs(Sx - x) + abs(Sy - y) <= dist:
                row.add((x, y))


if __name__ == "__main__":
    lines = open("input", "r").read().splitlines()
    beacons = set()
    for line in lines:
        Sx, Sy, Bx, By = map(int, re.findall(r"\d+", line))
        print(f"Sx: {Sx}, Sy: {Sy}, Bx: {Bx}, By: {By}")
        beacons.add((Bx, By))
        update_row(Sx, Sy, Bx, By)
    row = [pos for pos in row if pos not in beacons]
    print(f"Part 1: {len(row)}")

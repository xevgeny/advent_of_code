from collections import defaultdict


def solve(arr):
    res1, res2 = 0, 0
    gears = defaultdict(list)
    N, M = len(arr), len(arr[0])
    num, has_symbol, gear = "", False, None
    for i in range(N + 1):
        for j in range(M):
            if i < N and arr[i][j].isdigit():
                num += arr[i][j]
                for ii in [-1, 0, 1]:
                    for jj in [-1, 0, 1]:
                        if 0 <= i + ii < N and 0 <= j + jj < M:
                            cc = arr[i + ii][j + jj]
                            if not cc.isdigit() and cc != ".":
                                has_symbol = True
                            if cc == "*":
                                gear = (i + ii, j + jj)
            else:
                if num != "" and has_symbol:
                    res1 += int(num)
                if num != "" and gear:
                    gears[gear].append(int(num))
                    if len(gears[gear]) == 2:
                        res2 += gears[gear][0] * gears[gear][1]
                num, has_symbol, gear = "", False, None
    return res1, res2


with open("input", "r") as f:
    lines = f.read().splitlines()
    print(f"Answer 1 & 2: {solve(lines)}")

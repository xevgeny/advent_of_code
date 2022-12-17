shapes = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def play(moves, N):
    Y, X = N * 3, 7
    board = [[False for _ in range(X)] for _ in range(Y)]
    n, m, ymax = 0, 0, 0
    while n < N:
        y, x = ymax + 3, 2
        shape = shapes[n % len(shapes)]
        while True:
            dx = 1 if moves[m % len(moves)] == ">" else -1
            ok = True
            for sy, sx in shape:
                if not (0 <= y+sy < Y and 0 <= x+sx+dx < X and not board[y+sy][x+sx+dx]):
                    ok = False
                    break
            if ok:
                x += dx
            m += 1
            ok = True
            for sy, sx in shape:
                if not (0 <= y+sy-1 < Y and 0 <= x+sx < X and not board[y+sy-1][x+sx]):
                    ok = False
                    break
            if not ok:
                for sy, sx in shape:
                    board[y+sy][x+sx] = True
                    ymax = max(ymax, y+sy+1)
                break
            y -= 1
        n += 1
    return ymax


moves = open("input", "r").read()
print(f"Part 1: {play(moves, 2022)}")

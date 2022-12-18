shapes = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def play(moves, N):
    Y, YY, X = 10_000, 256, 7  # Y - sliding window, YY - history, X - width of the board
    board = [[False for _ in range(X)] for _ in range(Y+YY)]
    n, m, ymax, ysum = 0, 0, 0, 0
    D = len(moves) * len(shapes)
    stats, _stats = [], []  # keep track of all delta ymax
    while n < N:
        y, x = ymax + 3, 2
        shape = shapes[n % len(shapes)]
        while True:
            dx = 1 if moves[m % len(moves)] == ">" else -1
            ok = True
            for sy, sx in shape:
                if not (0 <= y+sy < Y+YY and 0 <= x+sx+dx < X and not board[y+sy][x+sx+dx]):
                    ok = False
                    break
            if ok:
                x += dx
            m += 1
            ok = True
            for sy, sx in shape:
                if not (0 <= y+sy-1 < Y+YY and 0 <= x+sx < X and not board[y+sy-1][x+sx]):
                    ok = False
                    break
            if not ok:
                yt = ymax
                for sy, sx in shape:
                    board[y+sy][x+sx] = True
                    ymax = max(ymax, y+sy+1)
                _stats.append(ymax-yt)
                if ymax >= Y:  # trim the board
                    nb = [[False for _ in range(X)] for _ in range(Y+YY)]
                    nb[:YY] = board[ymax-YY:ymax]
                    board = nb
                    ysum += ymax - YY
                    ymax = YY
                break
            y -= 1
        n += 1
        # track all delta ymax every D iterations
        if n % D == 0:
            stats.append(_stats)
            _stats = []
    return stats


def dedect_cycle(dstats, nmin, nmax):
    def find(dstats, n):
        for i in range(len(dstats)-n):
            if dstats[i:i+n] == dstats[i+n:i+2*n]:
                return i, i+n
        return None

    for n in range(nmin, nmax):
        pos = find(dstats, n)
        if pos:
            print(f"Found a repeating cycle of length {n} starting at {pos}")
            return (n, pos)

    return None


def solve(cycle):
    n, pos = cycle
    y = sum(dstats[:pos[0]])
    yc = sum(dstats[pos[0]:pos[1]])  # full height of the cycle
    rc = n*D  # number of rocks in the cycle
    nc = (rocks - pos[0]*D) // rc  # number of full cycles
    r = rocks - pos[0]*D - nc*rc  # remaining rocks
    y += nc * yc
    for c in stats[pos[0]:pos[1]]:
        for cc in c:
            r -= 1
            y += cc
            if r == 0:
                return y


rocks = 1_000_000_000_000
moves = open("input", "r").read()
stats = play(moves, 50_000_000)
D = len(moves) * len(shapes)
dstats = [sum(s) for s in stats]
cycle = dedect_cycle(dstats, nmin=5, nmax=500)
# We should be able to find a repeating cycle of length n
# Now let's calculate the final result
if cycle:
    print(f"Part 2: {solve(cycle)}")

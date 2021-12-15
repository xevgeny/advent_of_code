from queue import PriorityQueue


def readinput(input):
    arr = []
    for line in open(input).read().split('\n'):
        t = []
        for c in line:
            t.append(int(c))
        arr.append(t)
    return arr


def lowestrisk(arr):
    N = len(arr)
    dists = [[None for _ in range(N)] for _ in range(N)]
    q = PriorityQueue()
    q.put((0, 0, 0))
    while not q.empty():
        # print(q.qsize())
        dist, y, x = q.get()
        newdist = dist + arr[y][x]
        if dists[y][x] is None or newdist < dists[y][x]:
            dists[y][x] = newdist  # update min distance to (0,0)
        else:
            continue
        for yy, xx in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if 0 <= y+yy < N and 0 <= x+xx < N and dists[y+yy][x+xx] is None:
                q.put((dists[y][x], y+yy, x+xx))
    return dists[N-1][N-1]-arr[0][0]


def expand(arr):
    N = len(arr)
    for i in range(4):  # expand south
        for n in range(N):
            arr.append([x+1 if x+1 <= 9 else 1 for x in arr[N*i+n]])
    for y in range(len(arr)):  # expand east
        for i in range(4):
            arr[y].extend([x+1 if x+1 <= 9 else 1 for x in arr[y][N*i:N*i+N]])


arr = readinput('./input')
print('Answer 1:', lowestrisk(arr))
expand(arr)
print('Answer 2:', lowestrisk(arr))

import heapq


def count_steps(arr):
    N = len(arr)
    M = len(arr[0])
    distances = [[float("inf") for _ in range(M)] for _ in range(N)]
    Sy, Sx = [(y, x) for y in range(N) for x in range(M) if arr[y][x] == "S"][0]
    Ey, Ex = [(y, x) for y in range(N) for x in range(M) if arr[y][x] == "E"][0]
    arr[Sy][Sx] = "a"
    arr[Ey][Ex] = "z"
    min_distance = float("inf")
    for Sy, Sx in [(y, x) for y in range(N) for x in range(M) if arr[y][x] == "a"]:
        q = [(0, Sy, Sx)]
        while q:
            d, y, x = heapq.heappop(q)
            if distances[y][x] <= d:
                continue
            distances[y][x] = d
            if y == Ey and x == Ex:
                min_distance = min(min_distance, d)
            for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < N and 0 <= nx < M and ord(arr[y][x]) - ord(arr[ny][nx]) >= -1:
                    heapq.heappush(q, (d + 1, ny, nx))
    return min_distance


if __name__ == "__main__":
    lines = open("input", "r").read().splitlines()
    arr = [list(line) for line in lines]
    print(f"Part 2: {count_steps(arr)}")

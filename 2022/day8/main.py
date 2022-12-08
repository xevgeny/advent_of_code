# number of visible trees
def part1(trees):
    n = 0
    N = len(trees)
    M = len(trees[0])
    for y in range(N):
        for x in range(M):
            if y == 0 or x == 0 or y == N - 1 or x == M - 1:
                n += 1
            else:
                left = len([i for i in range(0, x) if trees[y][i] >= trees[y][x]]) == 0
                right = len([i for i in range(x + 1, M) if trees[y][i] >= trees[y][x]]) == 0
                top = len([i for i in range(0, y) if trees[i][x] >= trees[y][x]]) == 0
                bottom = len([i for i in range(y + 1, N) if trees[i][x] >= trees[y][x]]) == 0
                if left or right or top or bottom:
                    n += 1
    return n


# highest scenic score, common sense doesn't apply here :/
def part2(trees):
    score = 0
    N = len(trees)
    M = len(trees[0])
    for y in range(N):
        for x in range(M):
            n_left, n_right, n_top, n_bottom = (0, 0, 0, 0)

            for i in reversed(range(0, x)):
                n_left += 1
                if trees[y][i] >= trees[y][x]:
                    break

            for i in range(x + 1, M):
                n_right += 1
                if trees[y][i] >= trees[y][x]:
                    break
            
            for i in reversed(range(0, y)): 
                n_top += 1
                if trees[i][x] >= trees[y][x]:
                    break

            for i in range(y + 1, N):
                n_bottom += 1
                if trees[i][x] >= trees[y][x]:
                    break

            score = max(score, n_left * n_right * n_top * n_bottom)

    return score


if __name__ == "__main__":
    with open("input", "r") as f:
        text = f.read()
        trees = [[int(x) for x in line] for line in text.splitlines()]
        print("Part 1 : {}".format(part1(trees)))
        print("Part 2 : {}".format(part2(trees)))

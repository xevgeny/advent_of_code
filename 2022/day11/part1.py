monkeys = [
    [71, 86],
    [66, 50, 90, 53, 88, 85],
    [97, 54, 89, 62, 84, 80, 63],
    [82, 97, 56, 92],
    [50, 99, 67, 61, 86],
    [61, 66, 72, 55, 64, 53, 72, 63],
    [59, 79, 63],
    [55],
]

monkey_business = [0] * len(monkeys)


def inspect(monkey, fn, div, m1, m2):
    for it in monkeys[monkey]:
        n = fn(it) // 3
        if n % div == 0:
            monkeys[m1].append(n)
        else:
            monkeys[m2].append(n)
    monkey_business[monkey] += len(monkeys[monkey])
    monkeys[monkey] = []


def play_round():
    inspect(0, lambda x: x * 13, 19, 6, 7)
    inspect(1, lambda x: x + 3, 2, 5, 4)
    inspect(2, lambda x: x + 6, 13, 4, 1)
    inspect(3, lambda x: x + 2, 5, 6, 0)
    inspect(4, lambda x: x * x, 7, 5, 3)
    inspect(5, lambda x: x + 4, 11, 3, 0)
    inspect(6, lambda x: x * 7, 17, 2, 7)
    inspect(7, lambda x: x + 7, 3, 2, 1)


if __name__ == "__main__":
    for i in range(20):
        play_round()
    monkey_business.sort(reverse=True)
    print(f"Part 1: {monkey_business[0] * monkey_business[1]}")

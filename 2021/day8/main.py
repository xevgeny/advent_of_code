def split_row(row):
    return [x.strip().split(' ') for x in row.split('|')]


def read_input(input):
    rows = open(input, 'r').read().split('\n')
    return [split_row(row) for row in rows]


def count_1478(rows):
    count = 0
    for row in rows:
        for digit in row[1]:
            if len(digit) in [2, 3, 4, 7]:
                count += 1
    return count


def sum_all(rows):
    sum = 0
    for row in rows:
        input  = [set(sorted(x)) for x in row[0]]
        output = [set(sorted(x)) for x in row[1]]
        digits = [None] * 10
        digits[1] = next(x for x in input if len(x) == 2)
        digits[4] = next(x for x in input if len(x) == 4)
        digits[7] = next(x for x in input if len(x) == 3)
        digits[8] = next(x for x in input if len(x) == 7)
        digits[3] = next(x for x in input if len(x) == 5 and digits[1].issubset(x))
        digits[5] = next(x for x in input if len(x) == 5 and digits[4].difference(set.union(digits[1], digits[7])).issubset(x))
        digits[2] = next(x for x in input if len(x) == 5 and x != digits[3] and x != digits[5])
        digits[9] = next(x for x in input if len(x) == 6 and x.difference(digits[5]).issubset(digits[4]))
        digits[6] = next(x for x in input if len(x) == 6 and x != digits[9] and len(x.difference(digits[5])) == 1)
        digits[0] = next(x for x in input if len(x) == 6 and x != digits[6] and x != digits[9])
        num = ''.join(map(lambda x: str(digits.index(x)), output))
        sum += int(num)
    return sum


rows = read_input('./input')
print('Answer 1: {}'.format(count_1478(rows)))
print('Answer 2: {}'.format(sum_all(rows)))

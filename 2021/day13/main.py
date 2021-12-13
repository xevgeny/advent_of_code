import re


def load_instructions(input):
    [dot_input, fold_input] = open(input).read().split('\n\n')
    dots = []
    for line in dot_input.split('\n'):
        [x, y] = line.split(',')
        dots.append((int(x), int(y)))
    folds = []
    for fold in fold_input.split('\n'):
        pos = int(re.findall(r'\d+', fold)[0])
        if 'x' in fold:
            folds.append(('x', pos))
        else:
            folds.append(('y', pos))
    return (dots, folds)



def foldall(dots, folds):
    t0 = set(dots)
    for i, (axis, pos) in enumerate(folds):
        t1 = set()
        for (x, y) in t0:
            if axis == 'x':
                t1.add((pos - (x - pos), y)) if x > pos else t1.add((x, y))
            else:
                t1.add((x, pos - (y - pos))) if y > pos else t1.add((x, y))
        t0 = t1
        if i == 0:
            print('Answer 1: {}'.format(len(t0)))
    return t0

(dots, folds) = load_instructions('./input')
code = foldall(dots, folds)

xmax = max(map(lambda t: t[0], code))
ymax = max(map(lambda t: t[1], code))
arr = [['.' for x in range(xmax + 1)] for y in range(ymax + 1)]
for (x, y) in code:
    arr[y][x] = '#'

print('Answer 2:')
for row in arr:
    print(' '.join(row))
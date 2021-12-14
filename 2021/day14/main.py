from collections import Counter, defaultdict


def read_input(input):
    template, rules_input = open(input).read().split('\n\n')
    rules = []
    for rule in rules_input.split('\n'):
        a, b = rule.split(' -> ')
        rules.append((a, b))
    return template, rules


def getpairsdict(template):
    pd = defaultdict(lambda: 0)
    lst = list(template)
    z = zip(lst[:-1], lst[1:])
    for pair in [a+b for a, b in z]:
        pd[pair] += 1
    return pd


def score(template, rules, steps):
    pd = getpairsdict(template)
    last = list(pd.keys())[-1]

    for step in range(steps):
        tmp = pd.copy()
        for a, b in rules:
            for pair in pd:
                if pair == a:
                    tmp[pair] -= pd[pair]
                    tmp[pair[0]+b] += pd[pair]
                    tmp[b+pair[1]] += pd[pair]
                    if pair == last:
                        last = b + pair[1]
        pd = tmp

    cd = defaultdict(lambda: 0)
    for pair in pd:
        cd[pair[0]] += pd[pair]
    cd[last[1]] += 1
    counts = sorted(list(cd.values()))
    return counts[-1] - counts[0]


template, rules = read_input('./input')
print('Answer 1: {}'.format(score(template, rules, 10)))
print('Answer 1: {}'.format(score(template, rules, 40)))

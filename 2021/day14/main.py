from collections import defaultdict


def read_input(input):
    template, rules_input = open(input).read().split('\n\n')
    rules = dict()
    for rule in rules_input.split('\n'):
        k, v = rule.split(' -> ')
        rules[k] = v
    return template, rules


def score(template, rules, steps):
    last = template[-1]
    pd = defaultdict(int)  # pairs dict
    for i in range(len(template)-1):
        pd[template[i]+template[i+1]] += 1

    for step in range(steps):
        tmp = defaultdict(int)
        for pair in pd:
            tmp[pair[0]+rules[pair]] += pd[pair]
            tmp[rules[pair]+pair[1]] += pd[pair]
        pd = tmp

    cd = defaultdict(int)  # chars dict
    for pair in pd:
        cd[pair[0]] += pd[pair]
    cd[last] += 1
    return max(cd.values()) - min(cd.values())


template, rules = read_input('./input')
print('Answer 1: {}'.format(score(template, rules, 10)))
print('Answer 2: {}'.format(score(template, rules, 40)))

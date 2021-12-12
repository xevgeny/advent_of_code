from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def npath(self, u, visited, can_visit_twice):
        n = 0
        for v in self.graph[u]:
            if v == 'end':
                n += 1
            elif v.isupper():
                n += self.npath(v, visited, can_visit_twice)
            elif v not in visited:
                n += self.npath(v, visited | {v}, can_visit_twice)
            elif v != 'start' and can_visit_twice:
                n += self.npath(v, visited, False)
        return n


def load_graph(input):
    g = Graph()
    input = open(input).read().split('\n')
    for i in input:
        [u, v] = i.split('-')
        g.add_edge(u, v)
    return g


g = load_graph('./input')

print(g.npath('start', {'start'}, False))
print(g.npath('start', {'start'}, True))

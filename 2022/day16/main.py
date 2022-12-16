import re
from bitsets import bitset


def best_flow1(G, F, V):
    states = set([(0, "AA", V())])  # total flow, current position, bitset of open valves
    for t in range(30):
        next_states = set()
        print(f"searching at t={t}, nstates={len(states)}")
        for total_flow, valve, open_valves in sorted(states, reverse=True)[:100000]:
            total_flow += sum([F[ov] for ov in open_valves])
            if F[valve] > 0 and valve not in open_valves:
                next_states.add((total_flow, valve, open_valves.union(V([valve]))))
            for next_valve in G[valve]:
                next_states.add((total_flow, next_valve, open_valves))
        states = next_states
    best_flow = 0
    for s, _, _ in states:
        best_flow = max(best_flow, s)
    return best_flow


def best_flow2(G, F, V):
    states = set([(0, V(["AA", "AA"]), V())])  # total flow, bitset of current positions, bitset of open valves
    for t in range(26):
        next_states = set()
        print(f"searching at t={t}, nstates={len(states)}")
        for total_flow, valves, open_valves in sorted(states, reverse=True)[:100000]:
            total_flow += sum([F[ov] for ov in open_valves])
            vs = valves.members()
            v1, v2 = (vs[0], vs[1]) if len(vs) == 2 else (vs[0], vs[0])
            o1, o2 = F[v1] > 0 and v1 not in open_valves, F[v2] > 0 and v2 not in open_valves
            if o1 and o2:
                next_states.add((total_flow, V([v1, v2]), open_valves.union(V([v1, v2]))))
            if o1:
                for nv in G[v2]:
                    next_states.add((total_flow, V([v1, nv]), open_valves.union(V([v1]))))
            if o2:
                for nv in G[v1]:
                    next_states.add((total_flow, V([nv, v2]), open_valves.union(V([v2]))))
            for nv1 in G[v1]:
                for nv2 in G[v2]:
                    next_states.add((total_flow, V([nv1, nv2]), open_valves))
        states = next_states
    best_flow = 0
    for s, _, _ in states:
        best_flow = max(best_flow, s)
    return best_flow


G = {}  # graph of valves
F = {}  # flow rates
lines = open("input", "r").read().splitlines()
for line in lines:
    valves = re.findall(r"[A-Z]{2}", line)
    G[valves[0]] = valves[1:]
    flow_rate = int(re.findall(r"\d+", line)[0])
    F[valves[0]] = flow_rate
V = bitset("V", tuple([v for v in G]))
print(f"Part 1: {best_flow1(G, F, V)}")
print(f"Part 2: {best_flow2(G, F, V)}")

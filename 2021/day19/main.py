import numpy as np
import math


def readinput(input):
    res = []
    scanners = open(input).read().split('\n\n')
    for scanner in scanners:
        points = []
        for point in scanner.split('\n')[1:]:
            x, y, z = [int(x) for x in point.split(',')]
            points.append((x, y, z))
        res.append(points)
    return res


def genrotations():
    def Rx(t):
        return np.array([
            [1, 0, 0],
            [0, math.cos(t), -math.sin(t)],
            [0, math.sin(t), math.cos(t)],
        ])

    def Ry(t):
        return np.array([
            [math.cos(t), 0, math.sin(t)],
            [0, 1, 0],
            [-math.sin(t), 0, math.cos(t)],
        ])

    def Rz(t):
        return np.array([
            [math.cos(t), -math.sin(t), 0],
            [math.sin(t), math.cos(t), 0],
            [0, 0, 1]
        ])

    # Bruteforce 24 unique rotation matrices because why not
    # https://en.wikipedia.org/wiki/Rotation_matrix
    rotations = []
    for i in [0, 1/2, 1, 3/2]:
        for j in [0, 1/2, 1, 3/2]:
            for k in [0, 1/2, 1, 3/2]:
                rx = Rx(-i*math.pi)
                ry = Ry(-j*math.pi)
                rz = Rz(-k*math.pi)
                rot = np.rint(rx.dot(ry).dot(rz)).astype(int)
                if not any(np.array_equal(x, rot) for x in rotations):
                    rotations.append(rot)
    return rotations


def noverlaps(beacons, scanner, rot, delta):
    n = 0
    for p in scanner:
        rotp = rot.dot(p) + delta
        if (rotp[0], rotp[1], rotp[2]) in beacons:
            n += 1
    return n


def mapscanner(beacons, scanner):
    for refp in beacons:
        for p in scanner:
            for rot in rotations:
                rotp = rot.dot(p)
                delta = np.array([
                    refp[0]-rotp[0],
                    refp[1]-rotp[1],
                    refp[2]-rotp[2],
                ])
                # the desired transformation was found, map all beacons
                if noverlaps(beacons, scanner, rot, delta) >= 12:
                    xs = []
                    for pp in scanner:
                        rotpp = rot.dot(pp) + delta
                        xs.append((rotpp[0], rotpp[1], rotpp[2]))
                    return (xs, delta)
    return None


def mapall():
    beacons = set(scanners[0])
    pos = [None] * len(scanners)
    pos[0] = np.array([0, 0, 0])
    mapped = [0]
    while len(mapped) < len(scanners):
        for i in range(len(scanners)):
            if i not in mapped:
                res = mapscanner(beacons, scanners[i])
                if res:
                    xs, delta = res
                    print('Found mapping for scanner #{} {}'.format(i, delta))
                    pos[i] = delta
                    mapped.append(i)
                    beacons |= set(xs)
    return beacons, pos


def L1(p, q):
    return np.sum(np.abs(p-q))


def maxdistance(pos):
    res = 0
    for p in pos:
        for q in pos:
            n = L1(p, q)
            if n > res:
                res = n
    return res


rotations = genrotations()
scanners = readinput('./input')
beacons, pos = mapall()

print('Answer 1:', len(beacons))
print('Answer 2:', maxdistance(pos))

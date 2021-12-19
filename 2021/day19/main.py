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


def noverlaps(refscanner, scanner, rot, delta):
    n = 0
    for p in scanner:
        rotp = rot.dot(p) + delta
        if (rotp[0], rotp[1], rotp[2]) in refscanner:
            n += 1
    return n


def mapscanner(refscanner, scanner):
    res = []
    for refp in refscanner:
        for p in scanner:
            for rot in rotations:
                rotp = rot.dot(p)
                delta = np.array([
                    refp[0]-rotp[0],
                    refp[1]-rotp[1],
                    refp[2]-rotp[2],
                ])
                # the desired transformation was found, map all beacons
                if noverlaps(refscanner, scanner, rot, delta) >= 12:
                    for pp in scanner:
                        rotpp = rot.dot(pp) + delta
                        res.append((rotpp[0], rotpp[1], rotpp[2]))
                    return res
    return []


def mapall():
    beacons = set(scanners[0])
    mapped = [0]
    while len(mapped) < len(scanners):
        for i in range(len(scanners)):
            if i not in mapped:
                res = mapscanner(beacons, scanners[i])
                if len(res) > 0:
                    print('Found mapping for scanner #{}'.format(i))
                    mapped.append(i)
                    beacons |= set(res)
    return beacons


def L1(p, q):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return np.sum(np.abs(p-q))


rotations = genrotations()
scanners = readinput('./input')


print('Answer 1:', mapall())

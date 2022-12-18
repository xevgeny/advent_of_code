lines = open("input", "r").read().splitlines()
cubes = set([tuple(map(int, line.split(","))) for line in lines])
dxyz = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def surface_area(cubes):
    n = 0
    for x, y, z in cubes:
        for dx, dy, dz in dxyz:
            if (x + dx, y + dy, z + dz) not in cubes:
                n += 1
    return n


def exterior_surface_area(cubes):
    xmin, xmax = min(x for x, y, z in cubes) - 1, max(x for x, y, z in cubes) + 1
    ymin, ymax = min(y for x, y, z in cubes) - 1, max(y for x, y, z in cubes) + 1
    zmin, zmax = min(z for x, y, z in cubes) - 1, max(z for x, y, z in cubes) + 1

    # find all air blocks within the bounding box
    air = set()
    q = [(xmin, ymin, zmin)]
    while q:
        x, y, z = q.pop(0)
        if (x, y, z) in air:
            continue
        if (x, y, z) not in cubes:
            air.add((x, y, z))
            for dx, dy, dz in dxyz:
                nx, nd, nz = x + dx, y + dy, z + dz
                if xmin <= nx <= xmax and ymin <= nd <= ymax and zmin <= nz <= zmax:
                    q.append((nx, nd, nz))

    # count the number of cubes that touch air 
    n = 0
    for x, y, z in cubes:
        for dx, dy, dz in dxyz:
            if (x + dx, y + dy, z + dz) in air:
                n += 1
    return n


print(f"Part 1: {surface_area(cubes)}")
print(f"Part 2: {exterior_surface_area(cubes)}")

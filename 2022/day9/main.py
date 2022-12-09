class RopeState:
    def __init__(self, size: int):
        self.xs, self.ys = [0] * size, [0] * size
        self.pos = {(0, 0)}

    def _update(self, Dx, Dy, n):
        for _ in range(n):
            self.xs[0] += Dx
            self.ys[0] += Dy
            for i in range(1, len(self.xs)):
                Cx, Cy = self.xs[i - 1] - self.xs[i], self.ys[i - 1] - self.ys[i]
                if abs(Cx) > 1 or abs(Cy) > 1:
                    self.xs[i] += 0 if Cx == 0 else 1 if Cx > 0 else -1
                    self.ys[i] += 0 if Cy == 0 else 1 if Cy > 0 else -1
            self.pos.add((self.xs[-1], self.ys[-1]))

    def move(self, command):
        match command.split(" "):
            case ["U", n]:
                self._update(0, 1, int(n))
            case ["D", n]:
                self._update(0, -1, int(n))
            case ["L", n]:
                self._update(-1, 0, int(n))
            case ["R", n]:
                self._update(1, 0, int(n))


if __name__ == "__main__":
    commands = open("input", "r").read().splitlines()
    rs2, rs10 = RopeState(size=2), RopeState(size=10)
    for command in commands:
        rs2.move(command)
        rs10.move(command)
    print(f"Part 1: {len(rs2.pos)}")
    print(f"Part 2: {len(rs10.pos)}")

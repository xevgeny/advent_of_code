class Program:
    def __init__(self):
        self.x = 1
        self.cycle = 0
        self.addx = [1]
        self.strength = 0
        self.screen = [["." for _ in range(40)] for _ in range(6)]

    def check(self):
        if self.cycle in [20, 60, 100, 140, 180, 220]:
            self.strength += self.cycle * sum(self.addx)
        c = self.cycle - 1
        if abs(self.x - (c % 40)) < 2:
            self.screen[c // 40][c % 40] = "#"

    def run(self, instructions: list[str]):
        ip = 0
        while True:
            match instructions[ip % len(instructions)].split(" "):
                case ["addx", x]:
                    self.cycle += 1
                    self.check()
                    if self.cycle == 240:
                        break
                    self.cycle += 1
                    self.check()
                    if self.cycle == 240:
                        break
                    self.x += int(x)
                    self.addx.append(int(x))
                case ["noop"]:
                    self.cycle += 1
                    self.check()
                    if self.cycle == 240:
                        break
            ip += 1


if __name__ == "__main__":
    instructions = open("input", "r").read().splitlines()
    prog = Program()
    prog.run(instructions)
    print(f"Part 1: {prog.strength}")
    print("Part 2:")
    for line in prog.screen:
        print("".join(line))

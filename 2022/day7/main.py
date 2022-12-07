class Node:
    def __init__(self, name: str, dir: bool, size=0, parent=None):
        self.name = name
        self.dir = dir
        self.size: int = size
        self.parent: Node = parent
        self.children: dict[str, Node] = {}

    def total_size(self):
        if self.dir:
            return sum(child.total_size() for child in self.children.values())
        else:
            return self.size

    def __repr__(self):
        sb = []
        queue = [(self, 0)]
        while queue:
            node, depth = queue.pop()
            if node.dir:
                sb.append("  " * depth + f"- dir {node.name}")
            else:
                sb.append("  " * depth + f"- {node.name} size={node.size}")
            for child in node.children.values():
                queue.append((child, depth + 1))
        return "\n".join(sb)


class Interpreter:
    def __init__(self):
        self.root: Node = Node("/", dir=True)
        self.current: Node = None

    def run(self, cmd: list[str]):
        if len(cmd) == 1:
            self._cd(cmd[0].split(" ")[1])
        else:
            self._ls(cmd[1:])

    def _cd(self, path: str):
        match path:
            case "/":
                self.current = self.root
            case "..":
                self.current = self.current.parent
            case dir:
                self.current = self.current.children[dir]

    def _ls(self, nodes: list[str]):
        for node in nodes:
            match node.split(" "):
                case ["dir", dir]:
                    if dir not in self.current.children:
                        child = Node(dir, dir=True, parent=self.current)
                        self.current.children[dir] = child
                case [size, name]:
                    if name not in self.current.children:
                        child = Node(
                            name, dir=False, parent=self.current, size=int(size)
                        )
                        self.current.children[name] = child

    # Find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes
    def part1(self):
        size = 0
        queue = [self.root]
        while queue:
            node = queue.pop()
            if node.dir and node.total_size() <= 100000:
                size += node.total_size()
            for child in node.children.values():
                queue.append(child)
        return size

    # Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update
    def part2(self):
        free_up = -(70000000 - interpreter.root.total_size() - 30000000)
        sizes = []
        queue = [self.root]
        while queue:
            node = queue.pop()
            size = node.total_size()
            if node.dir and size >= free_up:
                sizes.append(size)
            for child in node.children.values():
                queue.append(child)
        return min(sizes)


if __name__ == "__main__":
    with open("input", "r") as file:
        text = file.read()
        commands = [
            [x for x in xs.split("\n") if x.strip()] for xs in text.split("$ ")[1:]
        ]

        interpreter = Interpreter()
        for cmd in commands:
            interpreter.run(cmd)

        print(f"Part 1: {interpreter.part1()}")
        print(f"Part 2: {interpreter.part2()}")

class Node:
    def __init__(self, name: str, dir: bool, size=0, parent=None):
        self.name = name
        self.dir = dir
        self.size: int = size
        self.parent: Node = parent
        self.children: dict[str, Node] = {}

    def total_size(self):
        return sum(child.total_size() for child in self.children.values()) if self.dir else self.size


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

    def get_dirs(self):
        dirs = []
        q = [interpreter.root]
        while q:
            node = q.pop()
            if node.dir:
                dirs.append(node)
                q.extend(node.children.values())
        return dirs


if __name__ == "__main__":
    with open("input", "r") as file:
        text = file.read()
        commands = [
            [x for x in xs.split("\n") if x.strip()] for xs in text.split("$ ")[1:]
        ]

        interpreter = Interpreter()
        for cmd in commands:
            interpreter.run(cmd)

        # Find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes
        answer1 = sum([dir.total_size() for dir in interpreter.get_dirs() if dir.total_size() <= 100000])
        # Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update
        free_up = -(70000000 - 30000000 - interpreter.root.total_size())
        answer2 = min([dir.total_size() for dir in interpreter.get_dirs() if dir.total_size() >= free_up])

        print(f"Part 1: {answer1}")
        print(f"Part 2: {answer2}")

import math


class Node:
    def __init__(self, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '[{}, {}]'.format(repr(self.left), repr(self.right))

    def moveleft(self, node):
        prev = node.left
        curr = node
        # move value up-left
        while curr != None and curr.left == prev:
            prev = curr
            curr = curr.parent
        if curr != None:
            if type(curr.left) is int:
                curr.left += node.left
            else:
                curr = curr.left
                # now, move value down-right
                while type(curr.right) is Node:
                    curr = curr.right
                curr.right += node.left

    def moveright(self, node):
        prev = node.right
        curr = node
        # move value up-right
        while curr != None and curr.right == prev:
            prev = curr
            curr = curr.parent
        if curr != None:
            if type(curr.right) is int:
                curr.right += node.right
            else:
                curr = curr.right
                # now, move value down-left
                while type(curr.left) is Node:
                    curr = curr.left
                curr.left += node.right

    def explode(self):
        # DFS / traversing order is important
        q = [(0, self)]
        while q:
            depth, node = q.pop()
            if depth >= 4:
                self.moveleft(node)
                self.moveright(node)
                if node.parent.left == node:
                    node.parent.left = 0
                elif node.parent.right == node:
                    node.parent.right = 0
                return True
            else:
                if type(node.right) is Node:
                    q.append((depth+1, node.right))
                if type(node.left) is Node:
                    q.append((depth+1, node.left))
        return False

    def split(self):
        # DFS / traversing order is important
        q = [(self, self.parent)]
        while q:
            node, parent = q.pop()
            if type(node) is int:
                if node >= 10:
                    splitted = Node(parent, math.floor(
                        node/2), math.ceil(node/2))
                    if parent.left == node:
                        parent.left = splitted
                    elif parent.right == node:
                        parent.right = splitted
                    return True
            else:
                q.append((node.right, node))
                q.append((node.left, node))
        return False

    def reduce(self):
        while True:
            if not self.explode():
                if not self.split():
                    break


def list_to_node(arr, parent=None):
    if not parent:
        parent = Node()
    # left
    if type(arr[0]) is list:
        node = Node(parent)
        parent.left = node
        list_to_node(arr[0], node)
    else:
        parent.left = arr[0]
    # right
    if type(arr[1]) is list:
        node = Node(parent)
        parent.right = node
        list_to_node(arr[1], node)
    else:
        parent.right = arr[1]
    return parent


def add_nodes(a, b):
    root = Node()
    root.left = a
    root.right = b
    a.parent = root
    b.parent = root
    return root


def magnitude(node):
    if type(node) is int:
        return node
    else:
        return 3*magnitude(node.left) + 2*magnitude(node.right)


nodes = [list_to_node(eval(x))
         for x in open('./input').read().split('\n')]

state = nodes[0]
for node in nodes[1:]:
    state = add_nodes(state, node)
    state.reduce()

print('Answer 1:', magnitude(state))

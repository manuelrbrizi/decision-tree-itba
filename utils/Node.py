class Node:

    def __init__(self, attr, val):
        self.children = {}
        self.name = attr
        self.val = val

    def add_child(self, name, val):
        self.children[name] = Node(name, val)

    def print_node(self):
        print(self.name)

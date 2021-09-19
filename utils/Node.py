class Node:

    def __init__(self, attr):
        self.children = []
        self.name = attr
        self.index = 0

    def add_child(self, node):
        self.children[self.index] = node
        self.index += 1

    def print_node(self):
        print(self.name)

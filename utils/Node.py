class Node:

    def __init__(self, attr, previous_name, previous_value):
        self.value = None
        self.children = []
        self.name = attr
        self.previous_attr_name = previous_name
        self.previous_attr_value = previous_value
        self.is_final = False

    def add_child(self, name, previous_name, previous_value):
        self.children = self.children + [Node(name, previous_name, previous_value)]
        return self.children[-1]

    def set_node_final(self, value):
        self.is_final = True
        self.value = value

    def print_node(self):
        print(self.name, "- (", self.previous_attr_name, "-", self.previous_attr_value, ")")
        for child in self.children:
            child.print_node()

    def print_solo(self):
        print(self.name, "- (", self.previous_attr_name, "-", self.previous_attr_value, ")")

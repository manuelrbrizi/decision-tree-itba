class Node:

    def __init__(self, attr, previous_name, previous_value):
        self.value = None
        self.children = []
        self.name = attr
        self.previous_attr_name = previous_name
        self.previous_attr_value = previous_value
        self.is_final = False
        self.total_classified = 0
        self.total_ok = 0
        self.total_classified_one = 0

    def add_child(self, name, previous_name, previous_value):
        self.children = self.children + [Node(name, previous_name, previous_value)]
        return self.children[-1]

    def set_node_final(self, value):
        self.is_final = True
        self.value = value

    def print_node(self):
        if self.is_final:
            print(self.name, self.value, "- (", self.previous_attr_name, "-", self.previous_attr_value, ")")
        else:
            print(self.name, "- (", self.previous_attr_name, "-", self.previous_attr_value, ")")
            for child in self.children:
                child.print_node()

    def print_solo(self):
        print(self.name, "- (", self.previous_attr_name, "-", self.previous_attr_value, ")")

    # Tengo que ver que valor de atributo actual soy: por ejemplo si tengo Account Balance veo si es 1, 2, 3 o 4
    # Una vez que tengo ese valor, itero por los children a ver cual es la rama que es ese valor
    # Una vez que encuentro el hijo, reemplazo mi current_node por ese children y sigo en el loop
    # hasta que llego a un final node, ahi imprimo el resultado
    def classify(self, row):
        current_node = self

        while True:
            if current_node.is_final:
                print("Creditability = ", row["Creditability"], ", Classified = ", current_node.value)
                self.total_classified += 1
                if row["Creditability"] == current_node.value:
                    self.total_ok += 1
                if current_node.value == 1:
                    self.total_classified_one += 1
                return

            actual_value = row[current_node.name]
            for child in current_node.children:
                if child.previous_attr_value == actual_value:
                    current_node = child
                    break

    def reset(self):
        self.total_classified = 0
        self.total_ok = 0
        self.total_classified_one = 0

import copy

class ProductPrototype:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def clone(self):
        return copy.deepcopy(self)

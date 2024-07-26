# patterns/composite.py

class Category:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_products(self):
        return self.products

class Inventory:
    def __init__(self):
        self.categories = {}

    def add_category(self, category):
        self.categories[category.name] = category

    def get_category(self, name):
        return self.categories.get(name, None)

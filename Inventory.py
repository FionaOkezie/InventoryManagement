class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# class Inventory:
#     def __init__(self):
#         self.products = {}

#     def add_product(self, product, quantity):
#         self.products[product] = quantity

#     def update_inventory(self, product, quantity):
#         if product in self.products:
#             self.products[product] += quantity
#         else:
#             self.products[product] = quantity

#     def get_inventory(self):
#         return self.products
class Inventory:
    def __init__(self):
        self.products = {}  # Dictionary to hold products and their quantities

    def add_product(self, product, quantity):
        if product in self.products:
            self.products[product] += quantity
        else:
            self.products[product] = quantity

    def get_products(self):
        return self.products

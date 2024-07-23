# from Inventory import Inventory

# class InventoryFacade:
#     def __init__(self):
#         self.inventory = Inventory()

#     def add_product(self, product, quantity):
#         self.inventory.add_product(product, quantity)

#     def get_inventory(self):
#         return self.inventory.get_products()

#     def clone_product(self, prototype):
#         return prototype.clone()
from Inventory import Inventory

class InventoryFacade:
    def __init__(self):
        self.inventory = Inventory()

    def add_product(self, product, quantity):
        self.inventory.add_product(product, quantity)

    def get_inventory(self):
        return self.inventory.get_products()

    def clone_product(self, prototype):
        return prototype.clone()

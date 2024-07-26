from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddProductCommand(Command):
    def __init__(self, inventory, product, quantity):
        self.inventory = inventory
        self.product = product
        self.quantity = quantity

    def execute(self):
        self.inventory.add_product(self.product, self.quantity)

class UpdateInventoryCommand(Command):
    def __init__(self, inventory, product, quantity):
        self.inventory = inventory
        self.product = product
        self.quantity = quantity

    def execute(self):
        self.inventory.update_inventory(self.product, self.quantity)

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DeleteProductCommand(Command):
    def __init__(self, inventory, product_name):
        self.inventory = inventory
        self.product_name = product_name

    def execute(self):
        self.inventory.delete_product(self.product_name)


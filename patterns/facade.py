from inventory import Inventory

class InventoryFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryFacade, cls).__new__(cls)
            cls._instance.inventory = Inventory()
        return cls._instance

    def add_product(self, product, quantity):
        self.inventory.add_product(product, quantity)
        self.inventory.notify_observers(f"Added product {product.name} with price ${product.get_price():.2f} and quantity {quantity}")

    def get_inventory(self):
        return self.inventory

    def add_observer(self, observer):
        self.inventory.add_observer(observer)

    def remove_observer(self, observer):
        self.inventory.remove_observer(observer)

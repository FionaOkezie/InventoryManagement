class InventoryObserver:
    def update(self, product, quantity):
        pass

class Inventory:
    def __init__(self):
        self.observers = []
        self.products = {}

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, product, quantity):
        for observer in self.observers:
            observer.update(product, quantity)

    def add_inventory(self, product, quantity):
        self.products[product] = quantity
        self.notify_observers(product, quantity)

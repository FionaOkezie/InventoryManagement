import sys
from copy import deepcopy

# Singleton Pattern for Database Connection
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = cls._initialize_connection()
        return cls._instance

    @staticmethod
    def _initialize_connection():
        print("Database connection initialized")
        return "DatabaseConnectionObject"

# Factory Pattern for Creating Products
class ProductFactory:
    @staticmethod
    def create_product(product_type, name, price):
        if product_type == 'simple':
            return SimpleProduct(name, price)
        elif product_type == 'discounted':
            return DiscountedProduct(SimpleProduct(name, price), 0.1)
        elif product_type == 'taxed':
            return TaxedProduct(SimpleProduct(name, price), 0.2)

# Observer Pattern
class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)

class Inventory(Observable):
    def __init__(self):
        super().__init__()
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product
        self.notify_observers('product_added')

    def edit_product(self, name, new_product):
        self.products[name] = new_product
        self.notify_observers('product_edited')

    def delete_product(self, name):
        if name in self.products:
            del self.products[name]
            self.notify_observers('product_deleted')

    def view_products(self):
        return self.products.values()

# Strategy Pattern for Sorting
class SortStrategy:
    def sort(self, data):
        raise NotImplementedError

class SortByName(SortStrategy):
    def sort(self, data):
        return sorted(data, key=lambda x: x.name)

class SortByPrice(SortStrategy):
    def sort(self, data):
        return sorted(data, key=lambda x: x.price)

class ProductViewer:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def display_products(self, products):
        sorted_products = self._strategy.sort(products)
        for product in sorted_products:
            print(product)

# Decorator Pattern
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price

    def __str__(self):
        return f"{self.name}: ${self.get_price():.2f}"

class SimpleProduct(Product):
    pass

class ProductDecorator(Product):
    def __init__(self, product):
        self._product = product

    def get_price(self):
        return self._product.get_price()

    def __str__(self):
        return self._product.__str__()

class DiscountedProduct(ProductDecorator):
    def __init__(self, product, discount):
        super().__init__(product)
        self.discount = discount

    def get_price(self):
        return self._product.get_price() * (1 - self.discount)

class TaxedProduct(ProductDecorator):
    def __init__(self, product, tax_rate):
        super().__init__(product)
        self.tax_rate = tax_rate

    def get_price(self):
        return self._product.get_price() * (1 + self.tax_rate)

# Command Pattern
class Command:
    def execute(self):
        raise NotImplementedError

class AddProductCommand(Command):
    def __init__(self, inventory, product):
        self.inventory = inventory
        self.product = product

    def execute(self):
        self.inventory.add_product(self.product)

class EditProductCommand(Command):
    def __init__(self, inventory, name, new_product):
        self.inventory = inventory
        self.name = name
        self.new_product = new_product

    def execute(self):
        self.inventory.edit_product(self.name, self.new_product)

class DeleteProductCommand(Command):
    def __init__(self, inventory, name):
        self.inventory = inventory
        self.name = name

    def execute(self):
        self.inventory.delete_product(self.name)

# Template Method Pattern
class ProductOperationTemplate:
    def execute(self):
        self.pre_operation()
        self.operation()
        self.post_operation()

    def pre_operation(self):
        pass

    def operation(self):
        raise NotImplementedError

    def post_operation(self):
        pass

class AddProductOperation(ProductOperationTemplate):
    def __init__(self, inventory, product):
        self.inventory = inventory
        self.product = product

    def pre_operation(self):
        print("Preparing to add product")

    def operation(self):
        self.inventory.add_product(self.product)

    def post_operation(self):
        print("Product added successfully")

# Adapter Pattern for Third-Party Service
class ThirdPartyInventoryService:
    def add(self, product):
        print(f"Product {product.name} added to third-party service")

class InventoryServiceAdapter:
    def __init__(self, third_party_service):
        self.third_party_service = third_party_service

    def add_product(self, product):
        self.third_party_service.add(product)

# Memento Pattern for Undo Functionality
class Memento:
    def __init__(self, state):
        self.state = deepcopy(state)

class InventoryCaretaker:
    def __init__(self):
        self._mementos = []

    def save(self, inventory):
        self._mementos.append(Memento(inventory.products))

    def restore(self, inventory):
        if self._mementos:
            inventory.products = self._mementos.pop().state

# Proxy Pattern for Access Control
class InventoryProxy:
    def __init__(self, inventory):
        self._inventory = inventory

    def add_product(self, product):
        if self._has_permission():
            self._inventory.add_product(product)
        else:
            print("Permission denied")

    def edit_product(self, name, new_product):
        if self._has_permission():
            self._inventory.edit_product(name, new_product)
        else:
            print("Permission denied")

    def delete_product(self, name):
        if self._has_permission():
            self._inventory.delete_product(name)
        else:
            print("Permission denied")

    def view_products(self):
        return self._inventory.view_products()

    def _has_permission(self):
        # In a real application, you'd check user permissions here
        return True

# CLI Interface
def main():
    db_connection = DatabaseConnection()
    inventory = Inventory()
    caretaker = InventoryCaretaker()
    proxy_inventory = InventoryProxy(inventory)

    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Undo Last Action")
        print("6. Add Product to Third-Party Service")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            product_type = input("Enter product type (simple/discounted/taxed): ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            product = ProductFactory.create_product(product_type, name, price)
            caretaker.save(inventory)
            command = AddProductCommand(proxy_inventory, product)
            command.execute()
            print(f"Product {name} added successfully.")

        elif choice == '2':
            name = input("Enter product name to edit: ")
            new_type = input("Enter new product type (simple/discounted/taxed): ")
            new_name = input("Enter new product name: ")
            new_price = float(input("Enter new product price: "))
            new_product = ProductFactory.create_product(new_type, new_name, new_price)
            caretaker.save(inventory)
            command = EditProductCommand(proxy_inventory, name, new_product)
            command.execute()
            print(f"Product {name} edited successfully.")

        elif choice == '3':
            name = input("Enter product name to delete: ")
            caretaker.save(inventory)
            command = DeleteProductCommand(proxy_inventory, name)
            command.execute()
            print(f"Product {name} deleted successfully.")

        elif choice == '4':
            products = proxy_inventory.view_products()
            sort_choice = input("Sort by (name/price): ")
            if sort_choice == 'name':
                viewer = ProductViewer(SortByName())
            else:
                viewer = ProductViewer(SortByPrice())
            viewer.display_products(products)

        elif choice == '5':
            caretaker.restore(inventory)
            print("Last action undone.")

        elif choice == '6':
            product_type = input("Enter product type (simple/discounted/taxed): ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            product = ProductFactory.create_product(product_type, name, price)
            third_party_service = ThirdPartyInventoryService()
            adapter = InventoryServiceAdapter(third_party_service)
            adapter.add_product(product)
            print(f"Product {name} added to third-party service.")

        elif choice == '7':
            print("Exiting the system.")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

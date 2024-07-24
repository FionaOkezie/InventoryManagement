# inventory.py

from abc import ABC, abstractmethod
import click

class Observable(ABC):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Inventory(Observable):
    def __init__(self):
        super().__init__()
        self.categories = {}
        self.products = {}

    def add_product(self, product, quantity):
        self.products[product] = quantity
        product.add_observer(ProductObserver())
        self.notify_observers(f'Product {product.name} added with quantity {quantity}.')

    def get_product(self, name):
        for product in self.products.keys():
            if product.name == name:
                return product
        return None

    def get_products(self):
        return self.products

    def add_category(self, category):
        self.categories[category.name] = category

    def get_category(self, name):
        return self.categories.get(name, None)
    
    def delete_product(self, product_name):
        product = self.get_product(product_name)
        if product:
            del self.products[product]
            self.notify_observers(f'Product "{product_name}" has been deleted.')
            click.echo(f'Product "{product_name}" has been deleted.')
        else:
            click.echo(f'Product "{product_name}" not found.')

class Product(Observable):
    def __init__(self, name, price):
        super().__init__()
        self.name = name
        self.price = price
        self._strategy = None

    def set_price(self, new_price):
        self.price = new_price
        self.notify_observers(f'The price of {self.name} has been updated to ${self.price:.2f}')

    def get_price(self):
        if self._strategy:
            return self._strategy.calculate_price(self.price)
        return self.price

    def set_strategy(self, strategy):
        self._strategy = strategy
        self.notify_observers(f'The pricing strategy for {self.name} has been updated.')

class ProductObserver(Observer):
    def update(self, message):
        print(f"Notification: {message}")

class Category:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products

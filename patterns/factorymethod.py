from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def create(self):
        pass

class PhysicalProduct(Product):
    def create(self):
        return "Physical Product Created"

class DigitalProduct(Product):
    def create(self):
        return "Digital Product Created"

class ProductFactory:
    @staticmethod
    def get_product(product_type):
        if product_type == 'physical':
            return PhysicalProduct()
        elif product_type == 'digital':
            return DigitalProduct()

from abc import ABC, abstractmethod
from .factorymethod import PhysicalProduct, DigitalProduct

class ProductFactory(ABC):
    @abstractmethod
    def create_product(self):
        pass

class PhysicalProductFactory(ProductFactory):
    def create_product(self):
        return PhysicalProduct()

class DigitalProductFactory(ProductFactory):
    def create_product(self):
        return DigitalProduct()

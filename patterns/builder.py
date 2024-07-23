from Inventory import Product

class ProductBuilder:
    def __init__(self):
        self.product = Product("", 0)

    def set_name(self, name):
        self.product.name = name
        return self

    def set_price(self, price):
        self.product.price = price
        return self

    def build(self):
        return self.product

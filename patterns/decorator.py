# patterns/decorator.py

class PriceDecorator:
    def __init__(self, product):
        self._product = product

    def get_price(self):
        return self._product.get_price()

class DiscountDecorator(PriceDecorator):
    def __init__(self, product, discount):
        super().__init__(product)
        self._discount = discount

    def get_price(self):
        return self._product.get_price() * (1 - self._discount / 100)

class QuantityDecorator(PriceDecorator):
    def __init__(self, product, quantity_change):
        super().__init__(product)
        self._quantity_change = quantity_change

    def get_quantity(self, current_quantity):
        return current_quantity + self._quantity_change

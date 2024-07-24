# patterns/strategy.py

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_price(self, price):
        pass

class PercentageDiscountStrategy(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate_price(self, price):
        return price * (1 - self.percentage / 100)

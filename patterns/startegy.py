from abc import ABC, abstractmethod

class ReorderStrategy(ABC):
    @abstractmethod
    def reorder(self, product):
        pass

class SimpleReorderStrategy(ReorderStrategy):
    def reorder(self, product):
        return f"Reordering product: {product.name}"

class AdvancedReorderStrategy(ReorderStrategy):
    def reorder(self, product):
        return f"Advanced reordering of product: {product.name} based on complex algorithm"

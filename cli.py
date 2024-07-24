import click
from click import Context
from patterns.facade import InventoryFacade
from patterns.builder import ProductBuilder
from patterns.prototype import ProductPrototype
from patterns.startegy import PercentageDiscountStrategy
from patterns.decorator import QuantityDecorator
from patterns.composite import Category
from patterns.command import DeleteProductCommand
from inventory import Product, ProductObserver, Inventory  # Updated import

# Singleton Facade
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class InventoryFacade(metaclass=Singleton):
    def __init__(self):
        self.inventory = Inventory()

    def add_product(self, product, quantity):
        self.inventory.add_product(product, quantity)

    def get_inventory(self):
        return self.inventory

    def add_observer(self, observer):
        self.inventory.add_observer(observer)

inventory_facade = InventoryFacade()
observer = ProductObserver()
inventory_facade.add_observer(observer)

@click.group()
def cli():
    pass

@click.command()
@click.option('--category', required=True, help='The category name.')
@click.option('--name', required=True, help='The product name.')
@click.option('--price', required=True, type=float, help='The product price.')
@click.option('--quantity', required=True, type=int, help='The product quantity.')
def add_product(category, name, price, quantity):
    # Check if the category exists; if not, create it
    category_obj = inventory_facade.get_inventory().get_category(category)
    if not category_obj:
        category_obj = Category(category)
        inventory_facade.get_inventory().add_category(category_obj)
    
    # Create and add the product
    product = ProductBuilder().set_name(name).set_price(price).build()
    product.add_observer(observer)
    inventory_facade.add_product(product, quantity)
    category_obj.add_product(product)

    price_str = f"${price:.2f}"
    click.echo(f'Added product {name} with price {price_str} and quantity {quantity} to category {category}')

@click.command()
def show_inventory():
    click.echo("\nCurrent Inventory")

    categories = inventory_facade.get_inventory().categories
    if not categories:
        click.echo("No categories available.")
    else:
        for category_name, category in categories.items():
            click.echo(f"\nCategory: {category_name}")
            products = category.get_products()
            if not products:
                click.echo("  No products in this category.")
            else:
                for product in products:
                    price_str = f"${product.get_price():.2f}"
                    quantity = inventory_facade.get_inventory().products.get(product, 0)
                    click.echo(f"  Product: {product.name}, Price: {price_str}, Quantity: {quantity}")

    click.echo("\nUncategorized Products:")
    uncategorized_products = [prod for prod, qty in inventory_facade.get_inventory().get_products().items()
                              if not any(prod in cat.get_products() for cat in categories.values())]
    
    if not uncategorized_products:
        click.echo("  No uncategorized products.")
    else:
        for product in uncategorized_products:
            price_str = f"${product.get_price():.2f}"
            quantity = inventory_facade.get_inventory().products.get(product, 0)
            click.echo(f"  Product: {product.name}, Price: {price_str}, Quantity: {quantity}")



@click.command()
@click.option('--name', required=True, help='The product name to clone.')
@click.option('--price', required=True, type=float, help='The product price to clone.')
def clone_product(name, price):
    prototype = ProductPrototype(name, price)
    cloned_product = prototype.clone()
    price_str = f"${cloned_product.get_price():.2f}"
    click.echo(f'Cloned product {cloned_product.name} with price {price_str}')

@click.command()
@click.option('--name', required=True, help='The product name.')
@click.option('--discount', required=True, type=float, help='The discount percentage.')
def apply_discount(name, discount):
    product = inventory_facade.get_inventory().get_product(name)
    if product:
        product.set_strategy(PercentageDiscountStrategy(discount))
        click.echo(f'Applied {discount}% discount to {product.name}')

@click.command()
@click.option('--name', required=True, help='The product name.')
@click.option('--quantity-change', required=True, type=int, help='Change in quantity (can be positive or negative).')
def change_quantity(name, quantity_change):
    product = inventory_facade.get_inventory().get_product(name)
    if product:
        current_quantity = inventory_facade.get_inventory().products.get(product, 0)
        new_quantity = quantity_change
        if new_quantity < 0:
            new_quantity = 0  # Ensure quantity doesn't go below zero
        inventory_facade.get_inventory().products[product] = new_quantity
        click.echo(f'Updated quantity for {name} to {new_quantity}')
    else:
        click.echo(f'Product {name} not found.')

@click.command()
@click.option('--name', required=True, help='The name of the product to delete.')
def delete_product(name):
    inventory = inventory_facade.get_inventory()
    command = DeleteProductCommand(inventory, name)
    command.execute()


cli.add_command(add_product)
cli.add_command(show_inventory)
cli.add_command(delete_product)
cli.add_command(apply_discount)
cli.add_command(change_quantity)

def main_menu():
    while True:
        click.echo("\nInventory Management System")
        click.echo("1. Add Product")
        click.echo("2. Show Inventory")
        click.echo("3. Delete Product")
        click.echo("4. Apply Discount")
        click.echo("5. Change Quantity")
        click.echo("6. Exit")

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            click.echo("\nAdd a New Product")
            category = click.prompt("Enter category name")
            name = click.prompt("Enter product name")
            price = click.prompt("Enter product price", type=float)
            quantity = click.prompt("Enter product quantity", type=int)
            with Context(cli) as ctx:
                ctx.invoke(add_product, category=category, name=name, price=price, quantity=quantity)
        elif choice == 2:
            click.echo("\nCurrent Inventory")
            with Context(cli) as ctx:
                ctx.invoke(show_inventory)
        elif choice == 3:
            click.echo("\nDelete Product")
            name = click.prompt("Enter product name to Delete")
            # price = click.prompt("Enter product price to clone", type=float)
            with Context(cli) as ctx:
                ctx.invoke(delete_product, name=name)
        elif choice == 4:
            click.echo("\nApply Discount")
            name = click.prompt("Enter product name")
            discount = click.prompt("Enter discount percentage", type=float)
            with Context(cli) as ctx:
                ctx.invoke(apply_discount, name=name, discount=discount)
        elif choice == 5:
            click.echo("\nChange Quantity")
            name = click.prompt("Enter product name")
            quantity_change = click.prompt("Enter quantity change", type=int)
            with Context(cli) as ctx:
                ctx.invoke(change_quantity, name=name, quantity_change=quantity_change)
        elif choice == 6:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid option, please try again.")

if __name__ == '__main__':
    main_menu()

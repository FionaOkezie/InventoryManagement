import click
from click import Context
from patterns.facade import InventoryFacade
from patterns.builder import ProductBuilder
from patterns.prototype import ProductPrototype

inventory_facade = InventoryFacade()

@click.group()
def cli():
    pass

@click.command()
@click.option('--name', required=True, help='The product name.')
@click.option('--price', required=True, type=float, help='The product price.')
@click.option('--quantity', required=True, type=int, help='The product quantity.')
def add_product(name, price, quantity):
    product = ProductBuilder().set_name(name).set_price(price).build()
    inventory_facade.add_product(product, quantity)
    price_str = f"${price:.2f}"  # Format price with dollar sign and two decimal places
    click.echo(f'Added product {name} with price {price_str} and quantity {quantity}')

@click.command()
def show_inventory():
    inventory = inventory_facade.get_inventory()
    for product, quantity in inventory.items():
        price_str = f"${product.price:.2f}"  # Format price with dollar sign and two decimal places
        click.echo(f'Product: {product.name}, Price: {price_str}, Quantity: {quantity}')

@click.command()
@click.option('--name', required=True, help='The product name.')
@click.option('--price', required=True, type=float, help='The product price.')
def clone_product(name, price):
    prototype = ProductPrototype(name, price)
    cloned_product = prototype.clone()
    price_str = f"${cloned_product.price:.2f}"  # Format price with dollar sign and two decimal places
    click.echo(f'Cloned product {cloned_product.name} with price {price_str}')

cli.add_command(add_product)
cli.add_command(show_inventory)
cli.add_command(clone_product)

def main_menu():
    while True:
        click.echo("\nInventory Management System")
        click.echo("1. Add Product")
        click.echo("2. Show Inventory")
        click.echo("3. Clone Product")
        click.echo("4. Exit")

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            click.echo("\nAdd a New Product")
            name = click.prompt("Enter product name")
            price = click.prompt("Enter product price", type=float)
            quantity = click.prompt("Enter product quantity", type=int)
            with Context(cli) as ctx:
                ctx.invoke(add_product, name=name, price=price, quantity=quantity)
        elif choice == 2:
            click.echo("\nCurrent Inventory")
            with Context(cli) as ctx:
                ctx.invoke(show_inventory)
        elif choice == 3:
            click.echo("\nClone a Product")
            name = click.prompt("Enter product name to clone")
            price = click.prompt("Enter product price to clone", type=float)
            with Context(cli) as ctx:
                ctx.invoke(clone_product, name=name, price=price)
        elif choice == 4:
            click.echo("\nExiting the system...")
            break
        else:
            click.echo("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main_menu()

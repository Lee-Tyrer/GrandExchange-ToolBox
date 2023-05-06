import os
import time
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table

from grandexchange import Client

console = Console()


def clear():
    os.system("cls")


@click.group()
@click.option("--name", help="Add in your Discord ID or Email")
# @click.pass_context
def cli(name: str):
    pass


@cli.command()
@click.option("--item", help="Type in an item to be watched")
# @cli.pass_context
def watch(item):
    """Track the given item in the terminal"""
    client = Client("Hello")
    cached = None

    table = Table(expand=True)
    table.add_column("Item", justify="right")
    table.add_column("Timestamp")
    table.add_column("Low", justify="right")
    table.add_column("High", justify="right")

    if item not in [name for name in client.items.item_names()]:
        console.print(f"{item} is not a valid item")
        console.print("exiting...")
        exit()

    if cached is None:
        cached = client.get_current_prices(item)[0]

    while True:
        prices = client.get_current_prices(item)[0]

        if prices == cached:
            time.sleep(10)
            continue

        lowest, highest = prices.highest, prices.lowest
        table.add_row(item, str(highest.timestamp), str(lowest.price), str(highest.price))

        cached = prices.copy()
        clear()
        console.print(table)
        time.sleep(30)


if __name__ == '__main__':
    cli()

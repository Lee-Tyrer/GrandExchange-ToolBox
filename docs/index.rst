========
Overview
========

The GrandExchange Toolbox is a package to interact with the Oldschool
Runescape Grand Exchange API with pre-built calculators to help
you trade better.

A short example highlighting how we can check if an item is worth quickly
flipping:

>>> import grandexchange
>>> client = grandexchange.Client("ME")
>>> price = client.get_current_prices("Prayer potion (3)")
>>> grandexchange.flip(price)

The documentation contains a more thorough look into available calculators,
flips and best items to trade in almost real time.

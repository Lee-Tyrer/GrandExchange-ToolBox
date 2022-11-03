import grandexchange

client = grandexchange.Client("DISCORD_ID")

potions = [
    "Prayer potion (1)",
    "Prayer potion (2)",
    "Prayer potion (3)",
    "Prayer potion (4)"
]

prices = client.get_current_prices(potions)

sales = grandexchange.decant(prices, starting_dose=3, volume=2_000)

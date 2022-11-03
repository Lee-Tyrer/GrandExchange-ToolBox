import grandexchange

client = grandexchange.Client("DISCORD_ID")

prices = client.get_current_prices()

flip = grandexchange.best_flip(prices)

price = client.get_current_prices("Dragon claws")

flip = grandexchange.flip(price[0])

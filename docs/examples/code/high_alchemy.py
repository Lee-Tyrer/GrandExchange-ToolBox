import grandexchange

client = grandexchange.Client("DISCORD_ID")

alchable = client.get_current_prices("Air battlestaff")
nature = client.get_current_prices("Nature rune")

grandexchange.high_alchemy(nature[0], alchable[0], volume=1_000)

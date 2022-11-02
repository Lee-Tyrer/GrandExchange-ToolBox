import grandexchange
from grandexchange.items import Barrows, ItemSet


client = grandexchange.Client("DISCORD_ID")


dharoks = ItemSet.from_config(Barrows.Dharoks)

degraded = client.get_current_prices("Dharok's greataxe 0")
repaired = client.get_current_prices(dharoks.weapon)

grandexchange.repair_barrows(degraded[0], repaired[0], level=50, volume=1)
grandexchange.repair_barrows()

barrows = Barrows.from_config()

pieces = client.get_current_prices(barrows[0].piece_names)
client.get_current_prices(barrows[0].set)
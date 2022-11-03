"""
Setting up the client to interact with the API
"""

import grandexchange

# Setting up the user agent for the API owners to understand where
# their requests are coming from. It is a good idea to make this
# your discord ID in case you blow up their server.

client = grandexchange.Client("DISCORD_ID")

all_prices = client.get_current_prices()
single_price = client.get_current_prices("Dragon claws")

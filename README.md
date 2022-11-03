# GrandExchange-ToolBox
Package to interact with the OSRS live Grand Exchange API alongside additional
functions used in common money making approaches. 

# Quickstart
```python
import grandexchange

DISCORD_ID = "#1234"

client = grandexchange.Client(user_agent=DISCORD_ID)

all_current_prices = client.get_current_prices()

# Names are case sensitive
nature_rune = client.get_current_prices("Nature rune")[0]

# Accessing item properties from the API
# nature_rune.highest.price
# nature_rune.lowest.price
# nature_rune.highest.volume
# nature_rune.lowest.volume

flip = grandexchange.flip(nature_rune, volume=1000)
```

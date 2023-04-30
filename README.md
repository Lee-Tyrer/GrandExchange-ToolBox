# GrandExchange-ToolBox

Package to interact with the OSRS live Grand Exchange API alongside additional functions used in common money making
approaches.

## Getting Started

### Installing

The source code is hosted on Github at: https://github.com/Lee-Tyrer/GrandExchange-ToolBox and is available through
PyPi.

```sh
pip install grandexchangetoolbox
```

### Example
For more examples, please visit our documentation at https://grandexchange-toolbox.readthedocs.io/en/latest/.
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

## Features
* Python wrapper around the Oldschool Runescape Grand Exchange API 
* Functions to run common money making approaches
  * Instant flip
  * Potion decanting
  * Creating unfinished potions
  * Herb cleaning
  * Repairing barrows
  * Combining items
  * Bird nest crushing
  * High alchemy
  * Plank make

## License

[MIT](LICENSE)

## Acknowledgements

The Oldschool Runescape Wiki team and RuneLite for allowing the API to be openly accessible with a generous usage
policy. Please see their wiki page for more information on the underlying
API: https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices. 

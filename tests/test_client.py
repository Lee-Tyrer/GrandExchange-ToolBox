import pytest
from grandexchange.client import GrandExchangeClient
USER_AGENT = 'Pytest runs'
client = GrandExchangeClient(USER_AGENT)


no_items = None
single_item = 'Prayer potion(3)'
single_item_as_list = ['Prayer potion(3)']
multiple_item = ['Prayer potion(3)', 'Prayer potion(4)']

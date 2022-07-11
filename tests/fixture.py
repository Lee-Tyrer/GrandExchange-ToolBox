from datetime import datetime

import pytest

from grandexchange.items import Price, GrandExchangeItem, Timeseries

TIMESTAMP = datetime.now()


@pytest.fixture
def empty_price():
    return Price(timestamp=TIMESTAMP, price=None, volume=None)


@pytest.fixture
def single_price():
    return Price(timestamp=TIMESTAMP, price=1000, volume=1000)


@pytest.fixture
def two_list_price():
    return [
        Price(timestamp=TIMESTAMP, price=1000, volume=1000),
        Price(timestamp=TIMESTAMP, price=1100, volume=1000)
    ]


@pytest.fixture
def two_list_price_alt_prices():
    return [
        Price(timestamp=TIMESTAMP, price=1200, volume=1000),
        Price(timestamp=TIMESTAMP, price=1200, volume=1000)
    ]


@pytest.fixture
def two_list_price_with_empty():
    return [
        Price(timestamp=TIMESTAMP, price=1000, volume=1000),
        empty_price()
    ]


@pytest.fixture
def three_list_price():
    return [
        Price(timestamp=TIMESTAMP, price=1000, volume=1000),
        Price(timestamp=TIMESTAMP, price=1100, volume=1000),
        Price(timestamp=TIMESTAMP, price=900, volume=1000)
    ]


@pytest.fixture
def three_list_price_alt_prices():
    return [
        Price(timestamp=TIMESTAMP, price=1500, volume=1000),
        Price(timestamp=TIMESTAMP, price=1200, volume=1000),
        Price(timestamp=TIMESTAMP, price=950, volume=1000)
    ]


@pytest.fixture
def three_list_price_with_empty():
    return [
        Price(timestamp=TIMESTAMP, price=1000, volume=1000),
        Price(timestamp=TIMESTAMP, price=1100, volume=1000),
        empty_price()
    ]


@pytest.fixture
def three_list_price_with_empty_first():
    return [
        empty_price(),
        Price(timestamp=TIMESTAMP, price=1000, volume=1000),
        Price(timestamp=TIMESTAMP, price=1100, volume=1000)
    ]


@pytest.fixture
def an_item():
    return GrandExchangeItem(name="Item", id=0, value=100, high_alch=100, low_alch=50, limit=1_000)


@pytest.fixture
def complete_timeseries():
    return Timeseries(
        item=an_item(),
        highest=three_list_price(),
        lowest=three_list_price_alt_prices()
    )

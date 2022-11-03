from datetime import datetime

import pytest

from grandexchange.items import Price, GrandExchangeItem, GrandExchangeItems, Timeseries, ItemSet, Offer

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
def an_item_type_1():
    return GrandExchangeItem(name="Item", id=0, value=100, highalch=100, low_alch=50, limit=1_000)


@pytest.fixture
def an_item_type_2():
    return GrandExchangeItem(name="Item2", id=1, value=100, highalch=100, low_alch=50, limit=1_000)


@pytest.fixture
def multiple_items(an_item_type_1, an_item_type_2):
    return GrandExchangeItems(
        items=[an_item_type_1, an_item_type_2]
    )


@pytest.fixture
def complete_timeseries():
    return Timeseries(
        item=an_item_type_1(),
        highest=three_list_price(),
        lowest=three_list_price_alt_prices()
    )


@pytest.fixture
def item_set_without_nones():
    return ItemSet(
        weapon="weapon",
        helm="helm",
        body="body",
        shield="shield",
        legs="legs",
        set="set"
    )


@pytest.fixture
def item_set_with_nones():
    return ItemSet(
        weapon="weapon",
        helm="helm",
        body="body",
        shield=None,
        legs="legs",
        set="set"
    )


@pytest.fixture
def nature_rune_item():
    return GrandExchangeItem(
        name="Nature rune",
        id=0,
        value=100,
        highalch=100,
    )


@pytest.fixture
def nature_rune_offer(nature_rune_item):
    return Offer(
        item=nature_rune_item,
        highest=Price(timestamp=1, price=100),
        lowest=Price(timestamp=1, price=100),
    )


@pytest.fixture
def nature_rune_offer_with_profit(nature_rune_item):
    return Offer(
        item=nature_rune_item,
        highest=Price(timestamp=1, price=1000),
        lowest=Price(timestamp=1, price=100),
    )


@pytest.fixture
def alchable():
    return Offer(
        item=nature_rune_item,
        highest=Price(timestamp=1, price=1000),
        lowest=Price(timestamp=1, price=1000),
    )


@pytest.fixture
def potions():
    return [
        Offer(
            item=GrandExchangeItem(name="Prayer potion (1)", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=100),
            lowest=Price(timestamp=1, price=100)
        ),
        Offer(
            item=GrandExchangeItem(name="Prayer potion (2)", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=200),
            lowest=Price(timestamp=1, price=200)
        ),
        Offer(
            item=GrandExchangeItem(name="Prayer potion (3)", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=300),
            lowest=Price(timestamp=1, price=300)
        ),
        Offer(
            item=GrandExchangeItem(name="Prayer potion (4)", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=400),
            lowest=Price(timestamp=1, price=400)
        ),
    ]


@pytest.fixture
def log_and_planks() -> [Offer, Offer]:
    log = Offer(
        item=GrandExchangeItem(name="Logs", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=10),
        lowest=Price(timestamp=1, price=10),
    )
    plank = Offer(
        item=GrandExchangeItem(name="Plank", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=10),
        lowest=Price(timestamp=1, price=10),
    )

    return log, plank


@pytest.fixture
def repaired_barrows_item() -> Offer:
    return Offer(
        item=GrandExchangeItem(name="Dharok's greataxe", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=1_000_000),
        lowest=Price(timestamp=1, price=800_000)
    )


@pytest.fixture
def degraded_barrows_item() -> Offer:
    return Offer(
        item=GrandExchangeItem(name="Dharok's greataxe 0", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=800_000),
        lowest=Price(timestamp=1, price=750_000)
    )


@pytest.fixture
def degraded_barrows_item_2() -> Offer:
    return Offer(
        item=GrandExchangeItem(name="Guthan's warspear 0", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=800_000),
        lowest=Price(timestamp=1, price=750_000)
    )


@pytest.fixture
def full_repaired_barrows_set() -> list[Offer]:
    return [
        Offer(
            item=GrandExchangeItem(name="Dharok's greataxe", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's helm", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's platebody", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's platelegs", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
    ]


@pytest.fixture
def full_degraded_barrows_set() -> list[Offer]:
    return [
        Offer(
            item=GrandExchangeItem(name="Dharok's greataxe 0", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's helm 0", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's platebody 0", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Dharok's platelegs 0", id=1, value=0, highalch=0),
            highest=Price(timestamp=1, price=1_000_000),
            lowest=Price(timestamp=1, price=800_000)
        ),
    ]


@pytest.fixture
def barrows_set() -> Offer:
    return Offer(
        item=GrandExchangeItem(name="Dharok's set", id=1, value=0, highalch=0),
        highest=Price(timestamp=1, price=5_000_000),
        lowest=Price(timestamp=1, price=5_000_000)
    )


@pytest.fixture
def components_for_product() -> ([Offer, Offer], Offer):
    components = [
        Offer(
            item=GrandExchangeItem(name="Godsword blade", id=1, value=1, highalch=0),
            highest=Price(timestamp=1, price=300_000),
            lowest=Price(timestamp=1, price=250_000)
        ),
        Offer(
            item=GrandExchangeItem(name="Armadyl hilt", id=1, value=1, highalch=0),
            highest=Price(timestamp=1, price=9_000_000),
            lowest=Price(timestamp=1, price=9_000_000)
        )
    ]
    product = Offer(
        item=GrandExchangeItem(name="Armadyl godsword", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=10_000_000),
        lowest=Price(timestamp=1, price=10_000_000)
    )
    return components, product


@pytest.fixture
def grimy_and_clean_herbs() -> (Offer, Offer):
    grimy = Offer(
        item=GrandExchangeItem(name="Grimy Ranarr Weed", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=5_000),
        lowest=Price(timestamp=1, price=4_500),
    )
    clean = Offer(
        item=GrandExchangeItem(name="Ranarr Weed", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=5_500),
        lowest=Price(timestamp=1, price=5_400)
    )
    return grimy, clean


@pytest.fixture
def herb_and_unfinished(grimy_and_clean_herbs) -> (Offer, Offer):
    _, clean = grimy_and_clean_herbs

    unfinished = Offer(
        item=GrandExchangeItem(name="Prayer potion (unf)", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=7_000),
        lowest=Price(timestamp=1, price=6_800)
    )
    return clean, unfinished


@pytest.fixture
def birds_nest_and_crushed_nest() -> (Offer, Offer):
    birds_nest = Offer(
        item=GrandExchangeItem(name="Birds nest", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=300),
        lowest=Price(timestamp=1, price=250)
    )
    crushed_nest = Offer(
        item=GrandExchangeItem(name="Crushed nest", id=1, value=1, highalch=0),
        highest=Price(timestamp=1, price=400),
        lowest=Price(timestamp=1, price=370),
    )
    return birds_nest, crushed_nest

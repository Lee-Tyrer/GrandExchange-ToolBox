import pytest

from grandexchange.transactions import SaleTransaction
from grandexchange.constants import (
    SAWMILL_COSTS,
    PLANK_MAKE_COSTS
)
from grandexchange.exceptions import (
    ItemNotFoundError,
    InvalidLevelError,
    PriceNotAvailableError,
    IncorrectItemProvidedError
)
from grandexchange.calculators import (
    dosage,
    decant,
    flip,
    high_alchemy,
    check_skill_level,
    create_planks,
    repair_barrows,
    repair_barrows_set,
    combiner,
    clean_herbs,
    create_unfinished,
    crush,
    best_flip,
    ZAHURS_FEE,
    WESLEYS_FEE
)

from tests.fixtures import (
    nature_rune_item,
    nature_rune_offer,
    alchable,
    potions,
    nature_rune_offer_with_profit,
    log_and_planks,
    repaired_barrows_item,
    degraded_barrows_item,
    degraded_barrows_item_2,
    full_repaired_barrows_set,
    full_degraded_barrows_set,
    barrows_set,
    an_item_type_1,
    components_for_product,
    grimy_and_clean_herbs,
    herb_and_unfinished,
    birds_nest_and_crushed_nest
)


@pytest.mark.parametrize("name, dose", [
    ("Potion (1)", 1),
    ("Potion (2)", 2),
    ("Potion (3)", 3),
    ("Potion (4)", 4),
])
def test_dosage(name, dose):
    assert dosage(name) == dose


def test_dosage_error():
    with pytest.raises(ValueError):
        _ = dosage("Not a potion")


def test_decant(potions):
    sale = decant(potions, 1, 1)
    assert sale == [
        SaleTransaction(
            item=potions[1].item,
            full_buy_price=101,
            individual_sold_price=199,
            volume=0,
            tax=0.0,
            profit=-101.0
        ),
        SaleTransaction(
            item=potions[2].item,
            full_buy_price=101,
            individual_sold_price=299,
            volume=0,
            tax=0.0,
            profit=-101.0
        ),
        SaleTransaction(
            item=potions[3].item,
            full_buy_price=101,
            individual_sold_price=399,
            volume=0,
            tax=0.0,
            profit=-101.0)
    ]


def test_high_alchemy(nature_rune_offer):
    alch = high_alchemy(nature_rune_offer, nature_rune_offer)
    assert alch == -102


def test_combiner(components_for_product):
    components, product = components_for_product
    sale = combiner(components, product)
    assert sale.profit == 649999


def test_flip_no_profit(nature_rune_offer):
    profit = flip(nature_rune_offer, 1).profit
    assert profit == -2


def test_flip_with_profit(nature_rune_offer_with_profit):
    profit = flip(nature_rune_offer_with_profit, 1).profit
    assert profit == 888


def test_flip_raises_error_with_no_prices(nature_rune_offer_with_profit):
    nature_rune_offer_with_profit.highest.price = None

    with pytest.raises(PriceNotAvailableError):
        _ = flip(nature_rune_offer_with_profit)


def test_best_flip(nature_rune_offer, nature_rune_offer_with_profit):
    sale = best_flip([nature_rune_offer, nature_rune_offer_with_profit], top_n=1)
    assert sale[0].individual_sold_price == 999


def test_create_planks(log_and_planks):
    log, plank = log_and_planks
    sale = create_planks(log, plank, 1, method=SAWMILL_COSTS)
    assert sale.profit == -102


def test_create_planks_raises_error(log_and_planks, nature_rune_offer):
    log, plank = log_and_planks
    with pytest.raises(ItemNotFoundError):
        _ = create_planks(nature_rune_offer, plank, 1, method=SAWMILL_COSTS)


def test_clean_herbs(grimy_and_clean_herbs):
    grimy, clean = grimy_and_clean_herbs
    sale = clean_herbs(grimy, clean, volume=1)
    assert sale.full_buy_price == grimy.lowest.price + 1 + ZAHURS_FEE


def test_create_unfinished(herb_and_unfinished):
    clean, unfinished = herb_and_unfinished
    sale = create_unfinished(clean, unfinished, volume=1)
    assert sale.full_buy_price == clean.lowest.price + 1 + ZAHURS_FEE


def test_crush(birds_nest_and_crushed_nest):
    nest, crushed = birds_nest_and_crushed_nest
    sale = crush(nest, crushed, volume=1)
    assert sale.full_buy_price == nest.lowest.price + 1 + WESLEYS_FEE


def test_check_skill_level_uses_default_value_with_no_argument():
    @check_skill_level
    def to_be_decorated(level: int = 1) -> int:
        return level

    level = to_be_decorated()
    assert level == 1


@pytest.mark.parametrize("level", (0, 121))
def test_check_skill_level_raises_error_when_not_valid(level):
    @check_skill_level
    def to_be_decorated(level: int) -> int:
        return level

    with pytest.raises(InvalidLevelError):
        _ = to_be_decorated(level=level)


def test_repair_barrows_raises_incorrect_item_when_degraded_not_provided(repaired_barrows_item, nature_rune_offer):
    with pytest.raises(IncorrectItemProvidedError):
        _ = repair_barrows(repaired_barrows_item, nature_rune_offer)


def test_repair_barrows_raises_incorrect_item_when_item_not_in_set(repaired_barrows_item, degraded_barrows_item_2):
    with pytest.raises(IncorrectItemProvidedError):
        _ = repair_barrows(repaired_barrows_item, degraded_barrows_item_2)


def test_repair_barrows_returns_correct_profit(repaired_barrows_item, degraded_barrows_item):
    sale = repair_barrows(repaired_barrows_item, degraded_barrows_item)
    assert sale.profit == 140_500


def test_repair_barrows_set_returns_correct_profit(
        full_repaired_barrows_set,
        full_degraded_barrows_set,
        barrows_set
):
    sale = repair_barrows_set(
        full_repaired_barrows_set,
        full_degraded_barrows_set,
        barrows_set
    )
    assert sale.profit == 1421645

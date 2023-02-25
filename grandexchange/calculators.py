import functools
import inspect

from grandexchange.items import Offer, Timeseries, Barrows, Price
from grandexchange.constants import SAWMILL_COSTS, PLANK_MAKE_COSTS, REPAIR_BARROWS_COSTS
from grandexchange.transactions import SaleTransaction
from grandexchange.exceptions import (
    ItemNotFoundError,
    IncorrectItemProvidedError,
    InvalidLevelError,
    PriceNotAvailableError
)


def dosage(name: str) -> int:
    """Finds the number of doses in the potion based off the name

    Parses the last three characters of the potion name to determine the number of doses

    Parameters
    ----------
    name: str
        The name of the potion to be parsed. It must contain the ending dosage of the
        potion otherwise an error will be raised.

    Returns
    -------
    int:
        The number of doses in the potion
    """
    match name[-3:]:
        case "(1)":
            dose = 1
        case "(2)":
            dose = 2
        case "(3)":
            dose = 3
        case "(4)":
            dose = 4
        case _:
            raise ValueError("The given name was not parsed as a potion")
    return dose


def decant(potions: list[Offer], starting_dose: int, volume: int) -> list[SaleTransaction]:
    """Calculates the end number of potions after being decanted

    Parameters
    ----------
    potions: list[Offer]
        A list of the potions that will be decanted
    starting_dose: int
        The starting potion dosage to be used in the calculations
    volume: int
        Number of potions being decanted

    Returns
    -------
    list[SalesTransaction]:
        A list of transaction info on the potion's value
    """
    transactions = []
    sips = starting_dose * volume

    for index, potion in enumerate(potions):
        if (dose := dosage(potion.item.name)) == starting_dose:
            starting_potion = potions[index]
        potions[index].attributes['dose'] = dose

    for potion in potions:
        if (dose := potion.attributes['dose']) != starting_dose:
            transactions.append(SaleTransaction(
                item=potion.item,
                full_buy_price=(starting_potion.lowest.price + 1) * volume,
                individual_sold_price=potion.highest.price - 1,
                volume=sips / dose
            ))

    return transactions


def high_alchemy(nature_rune: Offer, alchable: Offer, volume: int = 1) -> float:
    """Calculates the profit of casting high alchemy on the item

    Parameters
    ----------
    nature_rune: Offer
        GrandExchange item for a nature rune
    alchable: Offer
        Item to be alched
    volume: int

    Returns
    -------
    float
    """
    cost = volume * (nature_rune.lowest.price + 1 + alchable.lowest.price + 1)
    high_alch_return = volume * alchable.item.high_alch
    return high_alch_return - cost


def combiner(parts: list[Offer], product: Offer, volume: int = 1) -> SaleTransaction:
    """Calculates the total profit from combining the items into the final product.

    Examples include Godswords, Dragonfire shields.

    Parameters
    ----------
    parts: list[Offer]
        All required items needed to create the product
    product: Offer
        The end product made after combining the items
    volume: int

    Returns
    -------
    SaleTransaction
    """
    cost = sum(volume * (part.lowest.price + 1) for part in parts)
    return SaleTransaction(
        item=product.item,
        full_buy_price=cost,
        individual_sold_price=product.highest.price + 1,
        volume=volume
    )


def best_flip(items: list[Offer], volume: int = 1, top_n: int = 10) -> list[SaleTransaction]:
    """Returns the best top n flips from

    Parameters
    ----------
    items
    volume
    top_n

    Returns
    -------
    list[SaleTransaction]
    """
    flips = [flip(item, volume) for item in items]
    flips.sort(reverse=True)

    return flips[0:top_n]


def flip(offer: Offer, volume: int = 1) -> SaleTransaction:
    """Calculates the profit from buying at the lowest price and selling at the highest

    Parameters
    ----------
    offer: GrandExchange Offer
    volume: int

    Returns
    -------
    SaleTransaction
    """
    try:
        return SaleTransaction(
            item=offer.item,
            full_buy_price=offer.lowest.price + 1,
            individual_sold_price=offer.highest.price - 1,
            volume=volume
        )
    except TypeError as err:
        if None in (offer.highest.price, offer.lowest.price):
            raise PriceNotAvailableError(offer.item)
        raise err


ZAHURS_FEE = 200
WESLEYS_FEE = 50


def transform(material: Offer, product: Offer, volume: int, fee: int = 0) -> SaleTransaction:
    """Calculates the profit from converting an item to another product, for example, cleaning herbs

    Parameters
    ----------
    material: Offer
        Initial item needed to be bought
    product: Offer
        The finished product of the material
    volume: int
    fee: int
        The fee required to pay for the conversion

    Returns
    -------
    SaleTransaction
    """
    cost = volume * (material.lowest.price + 1)
    fees = volume * fee

    return SaleTransaction(
        item=product.item,
        full_buy_price=cost + fees,
        individual_sold_price=product.highest.price - 1,
        volume=volume
    )


def create_planks(log: Offer, plank: Offer, volume: int,
                  method: SAWMILL_COSTS | PLANK_MAKE_COSTS = SAWMILL_COSTS) -> SaleTransaction:
    try:
        return transform(log, plank, volume, method[log.item.name])
    except KeyError:
        raise ItemNotFoundError(log.item, method.values())


def clean_herbs(grimy: Offer, clean: Offer, volume: int) -> SaleTransaction:
    return transform(grimy, clean, volume, ZAHURS_FEE)


def create_unfinished(herb: Offer, unfinished: Offer, volume: int) -> SaleTransaction:
    return transform(herb, unfinished, volume, ZAHURS_FEE)


def crush(material: Offer, product: Offer, volume: int) -> SaleTransaction:
    return transform(material, product, volume, WESLEYS_FEE)


def check_skill_level(func):
    """Decorator to check if the provided skill level is valid"""

    @functools.wraps(func)
    def is_between_1_and_120(*args, **kwargs):
        try:
            level = kwargs["level"]
        except KeyError:
            level = inspect.signature(func).parameters.get("level").default

        if not 1 <= level <= 120:
            raise InvalidLevelError(level)
        return func(*args, **kwargs)

    return is_between_1_and_120


@check_skill_level
def repair_barrows(repaired: Offer, degraded: Offer, level: int = 1, volume: int = 1) -> SaleTransaction:
    """Calculates the return of repairing a Barrows item

    Repair costs are determined by using the repair bench in a player's home. Default
    costs can be provided by supplying a smithing level of 1. The degraded item
    must be the same as the repaired item otherwise an error will be raised.

    Parameters
    ----------
    degraded: Offer
        The item being repaired
    repaired: Offer
        The repaired version of the item
    level: int
        Smithing level of the player
    volume:
        Total volume of items being repaired and sold

    Returns
    -------
    SaleTransaction

    Raises:
        IncorrectItemProvidedError: When the repair item does not match the degraded item
    """
    if degraded.item.name != repaired.item.name + " 0":
        raise IncorrectItemProvidedError(degraded.item.name)

    for _set in (ItemSet.from_config(brother) for brother in Barrows):
        if found_key := _set.find_key(repaired.item.name):
            break
    else:
        raise IncorrectItemProvidedError(repaired.item.name)

    default_cost = REPAIR_BARROWS_COSTS[found_key]

    repair_cost = (1 - (level / 200)) * default_cost * volume

    return SaleTransaction(
        item=repaired.item,
        full_buy_price=degraded.lowest.price * volume + repair_cost + 1,
        individual_sold_price=repaired.highest.price + 1,
        volume=volume,
    )


@check_skill_level
def repair_barrows_set(
        repaired: list[Offer],
        degraded: list[Offer],
        set_: Offer,
        level: int = 1,
        volume: int = 1,
) -> SaleTransaction:
    """Calculates the return of repairing a barrows set and selling the combined set

    Parameters
    ----------
    degraded: list[Offer]
        The list of barrow items being repaired
    repaired: list[Offer]
        The list of repaired barrow items
    set_: Offer
        The combined set being made
    level: int
        Smithing level of the player
    volume:
        Total volume of items being repaired and sold

    Returns
    -------
    SaleTransaction
    """
    sales: list[SaleTransaction] = []

    names = [piece.item.name + " 0" for piece in repaired]
    for piece in degraded:
        try:
            index = names.index(piece.item.name)
        except ValueError:
            raise ValueError("Degraded and repaired items do not match")

        sales.append(
            repair_barrows(repaired[index], piece, level, volume)
        )

    cost = sum(sale.full_buy_price for sale in sales)

    return SaleTransaction(
        item=set_.item,
        full_buy_price=cost,
        individual_sold_price=set_.highest.price - 1,
        volume=volume
    )

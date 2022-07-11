from grandexchange.items import Offer
from grandexchange.constants import SAWMILL_COSTS, PLANK_MAKE_COSTS
from grandexchange.transactions import SaleTransaction
from grandexchange.exceptions import ItemNotFoundError


def dosage(name: str) -> int:
    """Finds the number of doses in the potion based off the name

    Parses the last three characters of the potion name to determine the number of doses

    Parameters
    ----------
    name: str
        The name of the potion to be parsed

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
    return cost - high_alch_return


def combiner(parts: list[Offer], product: Offer, volume: int = 1) -> SaleTransaction:
    """Calculates the total profit from combining the items into the final product.

    Examples include Barrows, Godswords, Dragonfire shields.

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
    cost = [volume * (part.lowest.price + 1) for part in parts]
    return SaleTransaction(
        item=product.item,
        full_buy_price=cost,
        individual_sold_price=product.highest.price + 1,
        volume=volume
    )


def flip(item: Offer, volume: int = 1) -> SaleTransaction:
    """Calculates the profit from buying at the lowest price and selling at the highest

    Parameters
    ----------
    item: GrandExchange Offer
    volume: int

    Returns
    -------
    SaleTransaction
    """
    return SaleTransaction(
        item=item.item,
        full_buy_price=item.highest.price,
        individual_sold_price=item.lowest.price,
        volume=volume
    )


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

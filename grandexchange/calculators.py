from collections import defaultdict
from typing import Optional

from grandexchange.items import (
    Offer
)
from grandexchange.transactions import SaleTransaction


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


class Potions:
    """Calculator to identify potential profit from decanting potions"""

    def __init__(self, potions: list[Offer]):
        """Initialises the potions being decanted and adds a dose attribute to the item

        Parameters
        ----------
        potions: list[Offer]
        """
        for idx, potion in enumerate(potions):
            potions[idx].attributes[self._dose_key] = dosage(potion.item.name)

        self.potions = potions

    @property
    def _dose_key(self):
        return 'dose'

    def get_potions(self, dose: None | int):
        if dose is None:
            return self.potions
        return next(potion for potion in self.potions if potion.attributes[self._dose_key] == dose)

    def decant(self, volume: int, from_dose: int) -> list[SaleTransaction]:
        """Calculates the end number of potions after being decanted

        Parameters
        ----------
        volume: int
            Number of potions being decanted
        from_dose: int
            The starting potion dosage to be used in the calculations

        Returns
        -------
        list[SalesTransaction]:
            A list of transaction info on the potion's value
        """
        transactions: list[SaleTransaction] = []
        starting_potion = self.get_potions(from_dose)

        for potion in self.potions:
            dose = potion.attributes[self._dose_key]

            if dose == from_dose:
                continue

            vials = (from_dose * volume) / dose
            transaction = SaleTransaction(
                item=potion.item,
                full_buy_price=(starting_potion.lowest.price + 1) * volume,
                individual_sold_price=potion.highest.price + 1,
                volume=vials
            )
            transactions.append(transaction)

        return transactions

    def lowest_per_dose_value(self) -> dict:
        potions = defaultdict()
        for potion in self.potions:
            dose = potion.attributes[self._dose_key]
            potions[dose] = potion.lowest.price / dose

        return potions

    def highest_per_dose_value(self) -> dict:
        potions = defaultdict()
        for potion in self.potions:
            dose = potion.attributes[self._dose_key]
            potions[dose] = potion.highest.price / dose

        return potions


class HighAlchCalculator:
    pass


class CrushCalculator:
    """
    Bird's nest
    Superior dragon bones
    """
    pass


class CombineCalculator:
    def __init__(self, primary: Offer, secondary: Offer, final: Offer):
        self.primary = primary
        self.secondary = secondary
        self.final = final

    def combine(self, volume: int):
        raise NotImplementedError()

    """
    Hilts + Godswords
    Dragonfire wards
    """
    pass


class SetCalculator:
    """
    Barrows (Dharok's)
    Justiciar
    """


class FlipCalculator:
    """
    Ranarr seeds
    Snapdragon seeds
    Zulrah's scales
    Death rune
    """


class HerbCalculator:
    """
    Grimy to clean through Nardah
    """
    def __init__(self, grimy: Offer, clean: Offer, unfinished: Optional[Offer]):
        self.grimy = grimy
        self.clean = clean
        self.unfinished = unfinished if not None else None

    @property
    def _zahurs_fee(self) -> int:
        """Zahur charges 200gp to clean a herb, or making an unfinished potion"""
        return 200

    def _convert(self, material: Offer, product: Offer, volume: int) -> SaleTransaction:
        buy_price = volume * material.lowest.price + 1
        extra_cost = volume * self._zahurs_fee

        return SaleTransaction(product.item, buy_price + extra_cost, product.highest.price + 1, volume)

    def clean_grimy_herbs(self, volume: int):
        return self._convert(self.grimy, self.clean, volume)

    def clean_to_unfinished(self, volume: int):
        return self._convert(self.clean, self.unfinished, volume)

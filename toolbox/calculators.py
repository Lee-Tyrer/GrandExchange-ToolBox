from dataclasses import dataclass, field

from toolbox import constants
from toolbox.items import (
    Offer,
    Timeseries
)


@dataclass
class SaleTransaction:
    individual_price: int
    volume: int | float
    tax: float = field(init=False)
    price: float = field(init=False)

    def __post_init__(self):
        self.tax = self.calculate_tax()
        self.price = self.initial_cost - self.tax

    def calculate_tax(self):
        tax = self.initial_cost * constants.TAX_PERCENTAGE

        match self.is_taxed, tax:
            case True, tax if tax >= constants.TAX_THRESHOLD:
                return constants.TAX_THRESHOLD
            case False, tax:
                return 0
            case _:
                return tax

    @property
    def initial_cost(self):
        return self.individual_price * self.volume

    @property
    def is_taxed(self):
        return True if self.individual_price >= constants.TAX_LOWER_ITEM_PRICE else False


class Potions:
    """Calculates the profit potential through decanting potions"""

    def __init__(self, potion: Offer):
        self.potion: Offer = potion
        self.doses: int = self.find_dose(potion.item.name)
        # self.profit_calculator = ProfitCalculator()

    def find_dose(self, potion_name: str) -> int:
        """Parses the number of doses from the item name

        Parameters
        ----------
        potion_name: str
            The name of the potion to be parsed

        Returns
        -------
        int:
            The number of doses in the potion
        """
        match potion_name[-3:]:
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

    def decant(self, volume: int, potion: Offer) -> float:
        """Calculates the end number of potions after being decanted

        Parameters
        ----------
        volume: int
            Number of potions being decanted
        potion: Offer
            Target potion that will be decanted into

        Returns
        -------
        float:
            The number of potions that has been decanted into
        """
        purchase_price = (self.potion.lowest.price + 1) * volume

        dosage = self.find_dose(potion.item.name)
        decanted_potions = (self.doses * volume) / dosage

        sale_transacation = SaleTransaction(potion.highest.price, decanted_potions)

        return sale_transacation.price - purchase_price

    @property
    def lowest_per_dose_value(self) -> float:
        return self.potion.lowest.price / self.doses

    @property
    def highest_per_dose_value(self) -> float:
        return self.potion.highest.price / self.doses

    def total_doses(self, volume: int):
        return self.doses * volume


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
        total = volume * ((self.primary.lowest.price + 1) + (self.secondary.lowest.price - 1))

        sale = SaleTransaction(self.final.highest.price - 1, volume)

        return sale.price - total

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
    pass


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
    pass

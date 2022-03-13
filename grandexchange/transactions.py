from dataclasses import dataclass, field

from grandexchange import constants
from grandexchange.items import GrandExchangeItem


@dataclass
class SaleTransaction:
    item: GrandExchangeItem
    full_buy_price: int
    individual_sold_price: int
    volume: int | float
    tax: float = field(init=False)
    profit: float = field(init=False)

    def __post_init__(self):
        self.tax = calculate_tax(self.individual_sold_price, self.volume)
        self.profit = (self.individual_sold_price * self.volume) - self.tax - self.full_buy_price


def price_below_tax_threshold(price) -> bool:
    return True if price < constants.TAX_LOWER_ITEM_PRICE else False


def calculate_tax(price, volume):
    tax = price * volume * constants.TAX_PERCENTAGE

    if price_below_tax_threshold(price):
        return 0
    if tax > constants.TAX_THRESHOLD:
        return constants.TAX_THRESHOLD

    return tax
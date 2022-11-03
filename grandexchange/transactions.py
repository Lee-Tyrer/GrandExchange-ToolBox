from pydantic import BaseModel, validator

from grandexchange import constants
from grandexchange.items import GrandExchangeItem

from functools import total_ordering


@total_ordering
class SaleTransaction(BaseModel):
    item: GrandExchangeItem
    full_buy_price: int
    individual_sold_price: int
    volume: int | float
    tax: float = None
    profit: float = None

    def _is_valid_operand(self, other):
        return hasattr(other, "profit")

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            raise ValueError()
        return self.profit < other.profit

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            raise ValueError()
        return self.profit == other.profit

    @validator('full_buy_price', 'individual_sold_price', 'volume', pre=True)
    def value_is_above_zero(cls, value):
        if value < 0:
            raise ValueError('value can not be a negative number')
        return value

    @validator('tax', always=True)
    def set_tax(cls, v, values) -> float:
        return round(calculate_tax(values['individual_sold_price'], values['volume']), 0)

    @validator('profit', always=True)
    def set_profit(cls, v, values) -> float:
        sell_price = values["individual_sold_price"] * values["volume"]
        buy_price = values["full_buy_price"] * values["volume"]
        return sell_price - buy_price - values["tax"]


def price_below_tax_threshold(price: float) -> bool:
    """Returns true if the individual item price is below the threshold

    Parameters
    ----------
    price: float
        The price of the item

    Returns
    -------
    bool
    """
    return price < constants.TAX_LOWER_ITEM_PRICE


def calculate_tax(price: float, volume: int) -> float:
    """Calculates the amount of tax required to pay for the transaction

    Parameters
    ----------
    price: float
        The price of the item
    volume: int
        Total number of items being sold

    Returns
    -------
    float
    """
    tax = price * volume * constants.TAX_PERCENTAGE

    if price_below_tax_threshold(price):
        return 0
    if tax > constants.TAX_THRESHOLD:
        return constants.TAX_THRESHOLD

    return tax

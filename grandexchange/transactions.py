from typing import Optional
from pydantic import BaseModel, Field, validator

from grandexchange import constants
from grandexchange.items import GrandExchangeItem


class SaleTransaction(BaseModel):
    item: GrandExchangeItem
    full_buy_price: int
    individual_sold_price: int
    volume: int | float
    tax: float = None
    profit: float = None

    @validator('full_buy_price', 'individual_sold_price', 'volume', pre=True)
    def value_is_above_zero(cls, value):
        if value < 0:
            raise ValueError('value can not be a negative number')
        return value

    @validator('tax', always=True)
    def set_tax(cls, v, values) -> float:
        return calculate_tax(values['individual_sold_price'], values['volume'])

    @validator('profit', always=True)
    def set_profit(cls, v, values) -> float:
        return (values['individual_sold_price'] * values['volume']
                - values['tax'] - values['full_buy_price'])


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

import pytest

from grandexchange.transactions import SaleTransaction
from tests.fixtures import nature_rune_item


def test_sale_transaction_tax_with_price_above_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=1_000,
        individual_sold_price=1_000,
        volume=1
    )
    assert sale.tax == 10


def test_sale_transaction_profit_with_price_above_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=1_000,
        individual_sold_price=1_000,
        volume=1
    )
    assert sale.profit == -10


def test_sale_transaction_tax_with_price_below_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=99,
        individual_sold_price=99,
        volume=1
    )
    assert sale.tax == 0


def test_sale_transaction_profit_with_price_below_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=50,
        individual_sold_price=99,
        volume=1
    )
    assert sale.profit == 49


def test_sale_transaction_tax_multiple_items_with_price_below_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=99,
        individual_sold_price=99,
        volume=10
    )
    assert sale.tax == 0


def test_sale_transaction_profit_multiple_items_with_price_below_100gp(nature_rune_item):
    sale = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=99,
        individual_sold_price=99,
        volume=10
    )
    assert sale.profit == 0


def test_price_sorting(nature_rune_item):
    """Tests that the prices are being sorted correctly based off their profit margins"""
    low_profit = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=100,
        individual_sold_price=100,
        volume=1
    )
    even_lower_profit = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=100,
        individual_sold_price=100,
        volume=10
    )
    assert [even_lower_profit, low_profit] == sorted([low_profit, even_lower_profit])


def test_prices_are_equal(nature_rune_item):
    first = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=100,
        individual_sold_price=100,
        volume=1
    )
    second = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=100,
        individual_sold_price=100,
        volume=1
    )

    assert [first, second] == sorted([second, first])


def test_price_sorting_with_unrelated_item(nature_rune_item):
    first = SaleTransaction(
        item=nature_rune_item,
        full_buy_price=100,
        individual_sold_price=100,
        volume=1
    )
    other = "A"
    with pytest.raises(ValueError):
        _ = sorted([first, other])

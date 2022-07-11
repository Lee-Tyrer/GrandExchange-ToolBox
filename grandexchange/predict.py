from grandexchange.items import Timeseries


def sale_rate(orders: Timeseries):
    rates = []

    for idx in range(len(orders.lowest)):
        if idx == 0:
            continue

        current = orders.lowest[idx].volume
        timediff = orders.lowest[idx].timestamp - orders.lowest[idx - 1].timestamp

        try:
            rates.append(timediff / current)
        except ZeroDivisionError:
            rates.append(0)

    return rates

from grandexchange import client
cls = client.GrandExchangeClient('Lee')
prices = cls.timeseries_prices('Dragon claws')

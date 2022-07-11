import ruptures
from grandexchange.items import Timeseries


def change_point(prices: Timeseries, model: str = "rbf", margin: int = None):
    if margin is None:
        margin = find_penalty(prices)

    algo = ruptures.Pelt(model=model).fit(prices.highest_price_array)
    return algo.predict(margin)


def find_penalty(prices: Timeseries) -> float:
    for latest in reversed(prices.highest_price_array):
        if latest is not None:
            return latest * 0.1

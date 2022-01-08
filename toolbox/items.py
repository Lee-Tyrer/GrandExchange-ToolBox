import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass, field
from fuzzywuzzy import fuzz


@dataclass
class GrandExchangeItem:
    """Contains the name and identity of the Grand Exchange item"""
    name: str
    id: int
    value: int
    highalch: int = None
    lowalch: int = None
    limit: int = None


@dataclass
class GrandExchangeItems:
    items: list[GrandExchangeItem]

    def item_names(self) -> list[str]:
        """Returns the names of all the Grand Exchange items

        Returns
        -------
        list[str]
        """
        return [item.name for item in self.items]

    def search_for(self, name: str, threshold: int = 90) -> list[GrandExchangeItem]:
        """Performs fuzzy matching to return the Grand Exchange item

        The name and stored item name are both converted into lower case

        Parameters
        ----------
        name: str
            Name of the item we are searching for
        threshold: int
            Matching ratio of given name and stored item name

        Returns
        -------
        list[GrandExchangeItem]
        """
        matches = []

        for item in self.items:
            ratio = fuzz.ratio(item.name.lower(), name.lower())

            if ratio >= threshold:
                matches.append(item)

        return matches

    def get_id(self, identity: int) -> GrandExchangeItem:
        """Gets the GrandExchangeItem from the given unique ID

        Parameters
        ----------
        identity: int
            Grand Exchange item unique ID

        Returns
        -------
        GrandExchangeItem
        """

        for item in self.items:
            if identity == item.id:
                return item


@dataclass
class Price:
    """Lowest dataclass object that contains pricing data at individual timestamps"""
    timestamp: int
    price: int
    volume: int = field(default=None)


@dataclass
class Offer:
    """Utilises the Price dataclass to provide additional detail on the Item"""
    item: GrandExchangeItem
    highest: Price
    lowest: Price


@dataclass
class Timeseries:
    """"""
    item: GrandExchangeItem
    highest: list[Price] = field(default_factory=list)
    lowest: list[Price] = field(default_factory=list)
    margin: list[Price] = field(default_factory=list, init=False)

    def plot_highest(self) -> plt.Figure:
        return self._plot_prices(self.highest)

    def plot_lowest(self) -> plt.Figure:
        return self._plot_prices(self.lowest)

    def plot_margin(self) -> plt.Figure:
        return self._plot_prices(self.margin)

    @staticmethod
    def _plot_prices(price: list[Price]) -> plt.Figure:
        ts = pd.DataFrame(price)
        fig = plt.figure()
        fig.plot(ts.timestamp, ts.price)

        return fig

    def __post_init__(self):
        """Creates margin field using the highest and lowest prices"""
        for high, low in zip(self.highest, self.lowest):
            margin = high.price - low.price
            self.margin.append(
                Price(high.timestamp, margin)
            )

    def volume_weighted_mean(self, period: int):
        pass

    def rolling_average(self, window: int = 5):
        """

        Parameters
        ----------
        window: int
            The duration of each period that the moving average will calculate

        Returns
        -------

        """
        highest = pd.DataFrame([item for item in self.highest])
        highest.rolling = highest.price.rolling(window=window, center=False).mean()

    def volatility(self):
        pass

    @property
    def earliest_timestamp(self) -> int:
        if (earliest := self.highest[0].timestamp) != self.lowest[0].timestamp:
            raise ValueError("Timestamps in the high and low sample points do not match")
        return earliest

    @property
    def latest_timestamp(self) -> int:
        if (latest := self.highest[-1].timestamp) != self.lowest[-1].timestamp:
            raise ValueError("Timestamps in the high and low sample points do not match")
        return latest

import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass, field
from collections import defaultdict
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
        """Performs fuzzy matching to return a list of possible matching Grand Exchange items

        The name and stored item name are first converted into lower case

        Parameters
        ----------
        name: str
            Name of the item being searched for
        threshold: int
            Matching ratio of given name and stored item name. Default is 90

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

    def get_item_by_id(self, identities: int | list[int]) -> list[GrandExchangeItem]:
        """Gets the GrandExchangeItem from the given unique ID

        Parameters
        ----------
        identities: int | list[int]
            Grand Exchange item unique ID

        Returns
        -------
        GrandExchangeItem
        """
        identities = [identities] if isinstance(identities, int) else identities
        return [item for item in self.items if item.id in identities]

    def get_item_by_name(self, names: str | list[str]) -> list[GrandExchangeItem]:
        """Gets the GrandExchangeItem from the given unique ID

        Parameters
        ----------
        names: str | list[str]
            Grand Exchange item unique ID

        Returns
        -------
        list[GrandExchangeItem]
        """
        names = [names] if isinstance(names, str) else names
        return [item for item in self.items if item.name in names]


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
    attributes: defaultdict = field(default_factory=defaultdict)


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
        """Creates a price margin field using the highest and lowest prices"""
        for high, low in zip(self.highest, self.lowest):
            profit_margin = high.price - low.price

            self.margin.append(Price(high.timestamp, profit_margin))

    @property
    def earliest_timestamp(self) -> int:
        return self.highest[0].timestamp

    @property
    def latest_timestamp(self) -> int:
        return self.lowest[-1].timestamp

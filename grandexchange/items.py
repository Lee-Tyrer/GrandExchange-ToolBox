import numpy as np
import matplotlib.pyplot as plt
import yaml
import pkgutil

from enum import Enum
from pydantic import BaseModel, Field
from collections import defaultdict
from fuzzywuzzy import fuzz


class GrandExchangeItem(BaseModel):
    """Contains the name and identity of the Grand Exchange item"""
    name: str
    id: int
    value: int
    high_alch: int = Field(None, alias='highalch')
    low_alch: int = Field(None, alias='lowalch')
    limit: int = None


class GrandExchangeItems(BaseModel):
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

    def get_item_by_id(self, identity: int) -> GrandExchangeItem | None:
        """Gets the GrandExchangeItem from the given unique ID

        Parameters
        ----------
        identity: int
            Grand Exchange item unique ID

        Returns
        -------
        GrandExchangeItem
        """
        return next(iter(item for item in self.items if item.id == identity), None)

    def get_item_by_name(self, name: str) -> GrandExchangeItem:
        """Gets the GrandExchangeItem from the given name

        Parameters
        ----------
        name: str
            Grand Exchange item unique ID

        Returns
        -------
        GrandExchangeItem
        """
        for item in self.items:
            if item.name == name:
                return item

    def get_item_by_names(self, names: list[str]) -> list[GrandExchangeItem]:
        """Gets the GrandExchangeItem from the given names

        Parameters
        ----------
        names: list[str]
            Grand Exchange item unique ID

        Returns
        -------
        list[GrandExchangeItem]
        """
        return [item for item in self.items if item.name in names]


class Price(BaseModel):
    """Lowest dataclass object that contains pricing data at individual timestamps"""
    timestamp: int
    price: int | None
    volume: int | None = None


class Offer(BaseModel):
    """Utilises the Price dataclass to provide additional detail on the Item"""
    item: GrandExchangeItem
    highest: Price
    lowest: Price
    attributes: defaultdict = Field(default_factory=defaultdict)


class Timeseries(BaseModel):
    """Timeseries of Price dataclasses for an Item"""
    item: GrandExchangeItem
    highest: list[Price] = Field(default_factory=list)
    lowest: list[Price] = Field(default_factory=list)
    timestep: int = None

    @property
    def highest_price_array(self):
        return np.array([x.price for x in self.highest], dtype=np.float)

    @property
    def lowest_price_array(self):
        return np.array([x.price for x in self.lowest], dtype=np.float)

    @property
    def highest_timestamp_array(self):
        return np.array([x.timestamp for x in self.highest], dtype=np.float)

    @property
    def lowest_timestamp_array(self):
        return np.array([x.timestamp for x in self.lowest], dtype=np.float)

    @property
    def time_range(self):
        timestamps = self.highest_timestamp_array
        return (max(timestamps) - min(timestamps)).total_seconds()

    @property
    def total_volume(self):
        return sum(x.volume for x in self.highest)

    def as_offers(self) -> list[Offer]:
        return [Offer(item=self.item, highest=high, lowest=low) for high, low in zip(self.highest, self.lowest)]

    def latest_offer(self) -> Offer:
        return Offer(
            item=self.item,
            highest=self.highest[-1],
            lowest=self.lowest[-1]
        )


class Barrows(Enum):
    Dharoks = "Dharoks"
    Karils = "Karils"
    Ahrims = "Ahrims"
    Guthans = "Guthans"
    Torags = "Torags"
    Veracs = "Veracs"


class ItemSet(BaseModel):
    weapon: str | None
    helm: str
    body: str
    shield: str | None
    legs: str
    set: str

    @property
    def repaired_names(self):
        return [item for item in self.dict(exclude={"set"}).values() if item is not None]

    @property
    def broken_pieces_name(self):
        return [item + " 0" for item in self.dict(exclude={"set"}).values() if item is not None]

    @classmethod
    def from_config(cls, name: Barrows):
        """

        Parameters
        ----------
        name: str
            The name of the Barrow's brother to retrieve the data for

        Returns
        -------
        ItemSet
        """
        stream = pkgutil.get_data(__name__, "static/sets.yaml")
        obj = yaml.safe_load(stream)
        for key, val in obj.items():
            if name.value == key:
                return cls(**val)

    def find_key(self, item: str):
        return next(
            (key for key, name in self.dict().items() if name == item),
            None
        )


def plot_prices(timeseries: Timeseries):
    x = [p.timestamp for p in timeseries.highest]
    high = [i.price for i in timeseries.highest]
    low = [i.price for i in timeseries.lowest]

    plt.plot(x, low, label="High price")
    plt.plot(x, high, label="Low price")
    plt.title(f"Time series from {min(x)} to {max(x)}")
    plt.xlabel("Timestamps")
    plt.ylabel("Price (gp)")
    plt.show()

from dataclasses import dataclass

from grandexchange.constants import BARROWS

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
    def time_range(self) -> tuple[int, int]:
        timestamps = [x.timestamp for x in self.highest]
        return min(timestamps), max(timestamps)

    @property
    def total_volume(self) -> int:
        return sum(x.volume for x in self.highest)

    def as_offers(self) -> list[Offer]:
        return [Offer(item=self.item, highest=high, lowest=low) for high, low in zip(self.highest, self.lowest)]

    def latest_offer(self) -> Offer:
        return Offer(
            item=self.item,
            highest=self.highest[-1],
            lowest=self.lowest[-1]
        )


@dataclass
class Barrows:
    name: str
    helm: str
    body: str
    legs: str
    weapon: str
    set: str

    def pieces(self):
        return {self.helm, self.body, self.legs, self.weapon}

    def degraded(self):
        return {item + " 0" for item in self.pieces()}

    @classmethod
    def load(cls, name: str):
        try:
            barrows = BARROWS[name]
        except KeyError as err:
            raise KeyError(f"must provide a name from {BARROWS.keys()}")

        return Barrows(
            name,
            barrows["helm"],
            barrows["body"],
            barrows["legs"],
            barrows["weapon"],
            barrows["set"],
        )

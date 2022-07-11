import requests

from typing import Optional, Any
from grandexchange.constants import VALID_TIMESTEPS

from grandexchange.exceptions import MalformedResponseError
from grandexchange import endpoints
from grandexchange.items import (
    GrandExchangeItem,
    GrandExchangeItems,
    Price,
    Offer,
    Timeseries,
)


class GrandExchangeClient:
    """Client to interact with the Grand Exchange API"""

    def __init__(self, user_agent: str, **request_headers):
        """Initialises the Grand Exchange client"""
        self._headers = {"user-agent": user_agent, **request_headers}
        self._endpoints = endpoints.URL()
        self.items = GrandExchangeItems(items=self._mapping())

        self._cache = None

    def send_request(self, url: str, params: dict = None) -> requests.Response:
        """Sends the request to the API endpoint

        Parameters
        ----------
        url: str
            The endpoint URL to send a request
        params: dict
            Key, value pairs of the parameters given to the request

        Returns
        -------
        requests.Response
        """
        try:
            r = requests.get(url, params=params, headers=self._headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        return r

    def get_current_prices(self, names: Optional[str | list[str]] | None = None) -> list[Offer]:
        """Fetches the latest prices of an item from the Grand Exchange API

        Providing a specific ID fetches the latest prices from the Grand Exchange API
        for the latest in-game buy or sell event.

        If no ID or a list of IDs are given then all items are fetched due to caching
        that the API provides. The response is filtered to retrieve the list of IDs that
        were provided, otherwise all items prices are returned. There is caching on the
        server side which will return a stale transaction of at least 60 seconds.

        Parameters
        ----------
        names: Optional[str | list[str]]
            Fetches all items if None is selected, else returns the given item ID(s)

        Returns
        -------
        list[Offer]
        """
        prices = []

        r = self.send_request(self._endpoints.latest)
        contents = r.json()["data"]

        names = [names] if isinstance(names, str) else names
        if names is not None:
            ids = [item.id for item in self.items.items if item.name in names]
        else:
            ids = [item.id for item in self.items.items]

        # Item ID from the API is returned as a string and needs to be converted to integer before filtering
        # the data into an Offer dataclass
        for identity, values in contents.items():
            try:
                identity = int(identity)
            except ValueError('could not parse item ID from the API response') as err:
                raise err

            # Checks whether the item list is None to return all prices, or selectively returns the inputted items
            if identity not in ids:
                continue

            match values:
                case {
                    'highTime': high_timestamp,
                    'high': high_price,
                    'lowTime': low_timestamp,
                    'low': low_price
                }:
                    offer = Offer(
                        item=self.items.get_item_by_id(identity),
                        highest=Price(timestamp=high_timestamp, price=high_price),
                        lowest=Price(timestamp=low_timestamp, price=low_price)
                    )
                case _:
                    raise MalformedResponseError()

            prices.append(offer)

        return prices

    def timeseries_prices(self, name: str, timestep: int = "5m") -> Timeseries:
        """Provides the highest and lowest prices of the given item at specific time intervals

        The request only accepts a single item ID.

        Parameters
        ----------
        name: str
            Grand Exchange item name
        timestep: str
            Timestep parameter that must be one of: '5m', '1h', '6h'
        Returns
        -------
        live.prices.TimeseriesPrices
        """
        if timestep not in VALID_TIMESTEPS:
            raise ValueError(f"timestep must be in {VALID_TIMESTEPS}")

        item = self.items.get_item_by_name(name)
        timeseries = Timeseries(item=item)

        r = self.send_request(url=self._endpoints.timeseries, params={"id": item.id, "timestep": timestep})
        contents = r.json()["data"]

        for row in contents:
            match row:
                case {
                    'timestamp': timestamp,
                    'avgHighPrice': high_price, 'highPriceVolume': high_volume,
                    'avgLowPrice': low_price, 'lowPriceVolume': low_volume
                }:
                    timeseries.highest.append(Price(timestamp=timestamp, price=high_price, volume=high_volume))
                    timeseries.lowest.append(Price(timestamp=timestamp, price=low_price, volume=low_volume))

        return timeseries

    def _mapping(self) -> list[GrandExchangeItem]:
        """Fetches the item mappings from the API and converts them into a list of Grand Exchange items

        Returns
        -------
        list[GrandExchangeItem]
        """
        mappings = []

        r = self.send_request(url=self._endpoints.mapping)
        items = r.json()

        for item in items:
            matching_keys = item.keys() & GrandExchangeItem.__annotations__.keys()
            mappings.append(
                GrandExchangeItem(**{k: v for k, v in item.items() if k in matching_keys})
            )

        return mappings

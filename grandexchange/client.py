import requests

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

    def __init__(self, headers: dict | None = None):
        """Initialises the Grand Exchange client"""
        self.headers = {"user-agent": USER_AGENT} | (headers if headers is not None else {})

        self.endpoints = endpoints.Endpoints()
        self.items = GrandExchangeItems(self.mappings())

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
        r = requests.get(url, params=params, headers=self.headers)

        if r.status_code != 200:
            raise requests.exceptions.HTTPError()

        return r

    def latest_values(self, name: str = None, identity: int = None):
        raise NotImplemented

    def latest_prices(self, ids: None | int | list[int] = None) -> list[Offer]:
        """Returns all latest values from the Grand Exchange

        Parameters
        ----------
        ids: None | int
            Retrieves all items if None is selected, else returns the given item ID
        Returns
        -------
        list[Offer]
        """
        url = self.endpoints.latest

        prices = []
        ids = [ids] if not isinstance(ids, list) else ids

        match ids:
            case (None | []):
                params = None
            case int():
                params = {"ids": ids}
            case _:
                params = None

        r = self.send_request(url, params=params)
        contents = r.json()["data"]

        # Parse the response to include the item name in the data structure
        for identity, values in contents.items():
            try:
                identity = int(identity)
            except ValueError:
                raise ValueError("Unable to parse Grand Exchange API item ID into an integer")

            item = self.items.get_id(identity)
            # Continues to the next item since the ID could not be found
            if item is None:
                continue

            match values:
                case {"highTime": high_timestamp, "high": high_price, "lowTime": low_timestamp, "low": low_price}:
                    offers = Offer(
                        item=item,
                        highest=Price(timestamp=high_timestamp, price=high_price),
                        lowest=Price(timestamp=low_timestamp, price=low_price)
                    )
                case _:
                    raise ValueError("The API request did not return the expected response")

            if item.id in ids or ids == [None]:
                prices.append(offers)

        return prices

    def timeseries_prices(self, ids: int, timestep: int = "5m") -> Timeseries:
        """Provides the highest and lowest prices of the given item at specific time intervals

        Parameters
        ----------
        ids: int
            Grand Exchange unique ID
        timestep: str
            Timestep parameter that must be one of: '5m', '1h', '6h'
        Returns
        -------
        live.prices.TimeseriesPrices
        """
        url = self.endpoints.timeseries
        valid_timesteps = ["5m", "1h", "6h"]

        if timestep not in valid_timesteps:
            raise ValueError(f"timestep must be in {valid_timesteps}")

        url = self.endpoints.timeseries
        r = self.send_request(url, params={"id": ids, "timestep": timestep})
        contents = r.json()["data"]

        timeseries = Timeseries(self.items.get_id(ids))

        for row in contents:
            match row:
                case {"timestamp": timestamp,
                      "avgHighPrice": high_price, "highPriceVolume": high_volume,
                      "avgLowPrice": low_price, "lowPriceVolume": low_volume}:
                    timeseries.highest.append(Price(timestamp, high_price, high_volume))
                    timeseries.lowest.append(Price(timestamp, low_price, low_volume))

        return timeseries

    def mappings(self) -> list[GrandExchangeItem]:
        """Provides the mappings of each Grand Exchange item

        Returns
        -------
        list[GrandExchangeItem]
        """
        url = self.endpoints.mapping
        mappings = []

        r = self.send_request(url)
        items = r.json()

        for item in items:
            matching_keys = item.keys() & GrandExchangeItem.__annotations__.keys()
            mappings.append(
                GrandExchangeItem(**{k: v for k, v in item.items() if k in matching_keys})
            )

        return mappings

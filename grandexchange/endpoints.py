class Servers:
    DEFAULT = "https://prices.runescape.wiki/api/v1/osrs"
    DEADMAN = "https://prices.runescape.wiki/api/v1/dmm"
    FRESH_START = "https://prices.runescape.wiki/api/v1/fsw"


class URL:
    def __init__(self, base_url: str = Servers.DEFAULT):
        """Contains the URL endpoints of the Grand Exchange API"""
        self.base_url = base_url

    @property
    def mapping(self):
        return f"{self.base_url}/mapping"

    @property
    def latest(self):
        return f"{self.base_url}/latest"

    @property
    def timeseries(self):
        return f"{self.base_url}/timeseries"

    def directory(self, separator: str):
        return f"{self.base_url}/{separator}"

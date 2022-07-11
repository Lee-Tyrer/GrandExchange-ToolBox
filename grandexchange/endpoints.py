from grandexchange.constants import BASE_URL


class URL:
    def __init__(self):
        """Contains the URL endpoints of the Grand Exchange API"""
        self.base_url = BASE_URL

    @property
    def mapping(self):
        return f"{self.base_url}/mapping"

    @property
    def latest(self):
        return f"{self.base_url}/latest"

    @property
    def timeseries(self):
        return f"{self.base_url}/timeseries"

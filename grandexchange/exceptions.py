from dataclasses import dataclass, field
from grandexchange.items import GrandExchangeItem


@dataclass
class MalformedResponseError(Exception):
    """A malformed response was returned and could not be parsed"""


@dataclass
class ItemNotFoundError(Exception):
    item: GrandExchangeItem
    choices: list = field(default_factory=list)

    def message(self):
        return f"Unable to find {self.item.name}"

    def __post_init__(self):
        if self.choices is None:
            self.message += f"A choice must be taken from: {self.choices}"
        super().__init__(self.message())


@dataclass
class WindowLargerThanArrayError(Exception):
    n: int
    window: int

    @property
    def message(self):
        return f"{self.window} is larger than array length of {self.n}"

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class InvalidItemError(Exception):
    url: str
    item: int

    @property
    def message(self):
        return f"An invalid item ID <{self.item}> was provided to {self.url}"

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class IncorrectItemProvidedError(Exception):
    item: str

    @property
    def message(self):
        return f"Incorrect item provided to function"

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class InvalidLevelError(Exception):
    level: int

    @property
    def message(self):
        return f"Invalid level {self.level} was provided, must be between 1 and 120."

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class PriceNotAvailableError(Exception):
    item: GrandExchangeItem

    @property
    def message(self):
        return f"{self.item.name} had no available price"

    def __post_init__(self):
        super().__init__(self.message)

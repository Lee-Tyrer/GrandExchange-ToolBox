import numpy as np

from grandexchange.items import Timeseries
from grandexchange.exceptions import WindowLargerThanArrayError


def rolling_average(x: np.array, window: int) -> np.array:
    """Performs a convolution over the given array and window

    Accepts nan values via

    Parameters
    ----------
    x: np.array
    window: int

    Returns
    -------
    np.array
    """
    if window > (n := len(x)):
        raise WindowLargerThanArrayError(n, window)

    cumsum = np.cumsum(x, dtype=float)
    cumsum[window:] = cumsum[window:] - cumsum[:-window]

    return cumsum[window - 1:] / window



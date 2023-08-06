import collections.abc
import math
from dataclasses import dataclass, field
from typing import overload

from gspaces import LinearSpace

# TODO overloads
# TODO complex numbers


def logspace(
    start: float,
    stop: float,
    num: int = 50,
    endpoint: bool = True,
    base: float = 10.0,
    **kwargs,
):
    """Returns numbers spaced evenly on a log scale.

    Args:
        start: ``base ** start`` is the starting value of the sequence.
        stop: base ** stop is the final value of the sequence, unless endpoint is False.
            In that case, ``num + 1`` values are spaced over the interval in log-space,
            of which all but the last (a sequence of length num) are returned.
        num: Number of samples to generate. Default is 50.
        endpoint: If true, stop is the last sample. Otherwise, it is not included. Default is True.
        base: The base of the log space. The step size between the elements in ln(samples) / ln(base) (or log_base(samples)) is uniform. Default is 10.0.

    Returns:
        samples: num samples, equally spaced on a log scale.
    """
    return LogSpace(start, stop, num=num, endpoint=endpoint, base=base)


@dataclass
class LogSpace(collections.abc.Sequence):
    """Logarithmic space for numbers spaced evenly on a log scale.

    Args:
        start: ``base ** start`` is the starting value of the sequence.
        stop: base ** stop is the final value of the sequence, unless endpoint is False.
            In that case, ``num + 1`` values are spaced over the interval in log-space,
            of which all but the last (a sequence of length num) are returned.
        num: Number of samples to generate. Default is 50.
        endpoint: If true, stop is the last sample. Otherwise, it is not included. Default is True.
        base: The base of the log space. The step size between the elements in ln(samples) / ln(base) (or log_base(samples)) is uniform. Default is 10.0.

    Returns:
        samples: num samples, equally spaced on a log scale.
    """

    start: float
    stop: float
    num: int = 50
    endpoint: bool = True
    base: float = 10.0
    _y_linear_space: LinearSpace = field(init=False)

    def __post_init__(self):
        self._y_linear_space = LinearSpace(
            self.start,
            self.stop,
            num=self.num,
            endpoint=self.endpoint,
        )

    def __getitem__(self, index):
        return self.base ** self._y_linear_space[index]  # type: ignore

    def __len__(self):
        """Total number of values in the space."""
        return self.num


def geomspace(start, stop, num=50, endpoint=True):
    """Return numbers spaced evenly on a log scale (a geometric progression).

    This is similar to `logspace`, but with endpoints specified directly.
    Each output sample is a constant multiple of the previous.

    Args:
        start: The starting value of the sequence.
        stop: The final value of the sequence, unless endpoint is False.
            In that case, ``num + 1`` values are spaced over the interval in log-space,
            of which all but the last (a sequence of length num) are returned.
        num: Number of samples to generate. Default is 50.
        endpoint: If true, stop is the last sample. Otherwise, it is not included. Default is True.

    Returns:
        samples: num samples, equally spaced on a log scale.
    """
    return GeometricSpace(start, stop, num=num, endpoint=endpoint)


@dataclass()
class GeometricSpace(collections.abc.Sequence):
    """Geometric space for evenly spaced numbers on a log scale (a geometric progression).

    This is similar to `logspace`, but with endpoints specified directly.
    Each output sample is a constant multiple of the previous.

    Args:
        start: The starting value of the sequence.
        stop: The final value of the sequence, unless endpoint is False.
            In that case, ``num + 1`` values are spaced over the interval in log-space,
            of which all but the last (a sequence of length num) are returned.
        num: Number of samples to generate. Default is 50.
        endpoint: If true, stop is the last sample. Otherwise, it is not included. Default is True.

    Returns:
        samples: num samples, equally spaced on a log scale.
    """

    start: float
    stop: float
    num: int = 50
    endpoint: bool = True
    _y_log_space: LogSpace = field(init=False)

    def __post_init__(self):
        base = 10.0
        log_start = math.log(self.start, base)
        log_end = math.log(self.stop, base)

        self._y_log_space = LogSpace(
            log_start, log_end, num=self.num, endpoint=self.endpoint, base=base
        )

        if self.start == 0 or self.stop == 0:
            raise ValueError("Geometric sequence cannot include zero")

    def __getitem__(self, index):
        # Ensure the endpoints match
        if self.num > 0:
            if index == 0:
                return self.start

            if self.num > 1 and self.endpoint and index in [-1, self.num - 1]:
                return self.stop

        return self._y_log_space[index]

    def __len__(self):
        """Total number of values in the space."""
        return self.num

import collections.abc
import math
from dataclasses import dataclass
from typing import Optional, overload

# TODO overloads


def arange(start: int, stop: int, step: int, **kwargs):
    """Returns an iterator for evenly spaced values within a given interval.

    Values are generated within the half-open interval [start, stop)
    (in other words, the interval including start but excluding stop).

    Args:
        start: Start of interval. The interval includes this value. The default start value is 0.
        stop: End of interval. The interval does not include this value,
            except in some cases where step is not an integer and floating point round-off affects the length of out.
        step: Spacing between values. For any output out, this is the distance between
            two adjacent values, out[i+1] - out[i]. The default step size is 1.
            If step is specified as a position argument, start must also be given.

    Returns:
        LinearSpace for evenly spaced values.

        For floating point arguments, the length of the result is ceil((stop - start)/step).
        Because of floating point overflow, this rule may result in the last element of out being greater than stop.
    """
    return LinearSpace(start, stop, step=step, endpoint=False)


def linspace(
    start: float,
    stop: float,
    num: int = 50,
    endpoint: bool = True,
    retstep: bool = False,
    **kwargs,
):
    """Returns a LinearSpace iterator for evenly spaced values within a given interval.

    Returns num evenly spaced samples, calculated over the interval [start, stop].

    The endpoint of the interval can optionally be excluded.

    Args:
        start: The starting value of the sequence.
        stop: The end value of the sequence, unless `endpoint` is set to False.
            In that case, the sequence consists of all but the last of ``num + 1``
            evenly spaced samples, so that `stop` is excluded.  Note that the step
            size changes when `endpoint` is False.
        num: Number of samples to generate. Default is 50. Must be non-negative.
        endpoint: If True, `stop` is the last sample. Otherwise, it is not included.
            Default is True.
        retstep: If True, return (`samples`, `step`), where `step` is the spacing
            between samples.

    Returns:
        samples: There are `num` equally spaced samples in the closed interval
            ``[start, stop]`` or the half-open interval ``[start, stop)``
            (depending on whether `endpoint` is True or False).
        step: Only returned if `retstep` is True
            Size of spacing between samples.
    """
    return LinearSpace(start, stop, num=num, endpoint=endpoint, retstep=retstep)


@dataclass()
class LinearSpace(collections.abc.Sequence):
    """Linear space for evenly spaced values.

    Args:
        start: The starting value of the sequence.
        stop: The end value of the sequence, unless `endpoint` is set to False.
            In that case, the sequence consists of all but the last of ``num + 1``
            evenly spaced samples, so that `stop` is excluded.  Note that the step
            size changes when `endpoint` is False.
        num: Number of samples to generate. Default is 50. Must be non-negative.
        step: Spacing between values. For any output out, this is the distance between two adjacent values,
            ``out[i+1] - out[i]``. The default step size is 1.
            If step is specified as a keyword argument, num is ignored and calculated
            based on the start, step and step values.
        endpoint: If True, `stop` is the last sample. Otherwise, it is not included.
            Default is True.
        retstep: If True, return (`samples`, `step`), where `step` is the spacing
            between samples.

    Returns:
        samples: There are `num` equally spaced samples in the closed interval
            ``[start, stop]`` or the half-open interval ``[start, stop)``
            (depending on whether `endpoint` is True or False).
        step: Only returned if `retstep` is True
            Size of spacing between samples.
    """

    start: float
    stop: float
    num: int = 50
    step: Optional[float] = None
    endpoint: bool = True
    retstep: bool = False

    def __post_init__(self):
        if self.step is None:
            div = (self.num - 1) if self.endpoint else self.num
            self.step = (self.stop - self.start) / div if div > 0 else None
        else:
            num = math.ceil((self.stop - self.start) / self.step)
            self.num = num + 1 if self.endpoint else num

        if self.num < 0:
            raise ValueError("Number of samples, %s, must be non-negative." % self.num)

    def __getitem__(self, index):
        if index == self.num - 1 and self.endpoint:
            return self.stop

        if index >= self.num:
            raise IndexError(
                f"Index out of range. For index={index} with num={self.num}"
            )

        y = self.start + index * self.step  # type: ignore

        return (y, self.step) if self.retstep else y

    def __len__(self):
        """Total number of values in the space."""
        return self.num

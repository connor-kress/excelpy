"""
References:
- https://en.wikipedia.org/wiki/Box-drawing_characters
┌─┬─┐╷╭─┬─╮
├─┼─┤│├─┼─┤╶╴
└─┴─┘╵╰─┴─╯
┏━━━┯━━━┯━━━┓
┃ A │ B │ C ┃
┣━━━┿━━━┿━━━┫
┃ 1 │ 2 │ 3 ┃
┠───┼───┼───┨
┃ 4 │ 5 │ 6 ┃
┗━━━┷━━━┷━━━┛
"""

from functools import partial
from itertools import zip_longest
from typing import Generator, Iterable, Iterator, Self
from currency import Currency
from percent import Percent
from util import get_value, number


Value = number | Currency | Percent


def add_values(a: Value, b: Value) -> Value:
    if isinstance(a, Currency) and isinstance(b, Percent):
        return Currency(a.value + b.value)
    elif isinstance(a, Percent) and isinstance(b, Currency):
        return Percent(a.value + b.value)
    else:
        return a + b # type: ignore


class Span:
    def __init__(self, values: Iterable[Value]):
        self.values = list(values)
        for val in self.values:
            if not isinstance(val, Value):
                raise TypeError("Span values must be of a numeric type.")

    def __add__(self, other: Self | Value) -> Self:
        if isinstance(other, Span):
            new_values = [
                add_values(a, b)
                for a, b in zip_longest(self, other, fillvalue=0)
            ]
        else:
            new_values = map(partial(add_values, b=other), self)
        return self.__class__(new_values)

    def __radd__(self, other: Self | Value) -> Self:
        return self.__add__(other)

    def __neg__(self) -> Self:
        return self.__class__(-val for val in self)

    def __sub__(self, other: Self | Value) -> Self:
        return self.__add__(-other)

    def __rsub__(self, other: Self | Value) -> Self:
        return (-self).__add__(other)

    def __mul__(self, other: Value) -> Self:
        return self.__class__(val*get_value(other) for val in self)
    
    def __rmul__(self, other: Value) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: Value) -> Self:
        return self.__class__(val/get_value(other) for val in self)

    def __pow__(self, other: Value) -> Self:
        return self.__class__(val**get_value(other) for val in self)
    
    def __repr__(self) -> str:
        if len(self) == 0:
            return "┌───────┐\n" \
                   "│ Empty │\n" \
                   "└───────┘"
        val_strs = list(map(str, self))
        max_len = max(map(len, val_strs))
        delimiter = "├" + "─"*(max_len+2) + "┤\n"
        s = "┌" + "─"*(max_len+2) + "┐\n"
        for i, val_str in enumerate(val_strs):
            s += f"│ {val_str:>{max_len}} │\n"
            if i < len(self) - 1:
                s += delimiter
            else:
                s += "└" + "─"*(max_len+2) + "┘"
        return s

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> Iterator[Value]:
        return iter(self.values)

    def __len__(self) -> int:
        return len(self.values)

    def len(self) -> int:
        return len(self)

    def sum(self) -> Value:
        return sum(self)

    def mean(self) -> Value:
        if len(self) == 0:
            raise ValueError("Cannot calculate mean of empty set.")
        return sum(self) / len(self)

    def var_p(self) -> Value:
        """Calculates the population variance."""
        if len(self) == 0:
            raise ValueError(
                "Cannot calculated population variance of empty set."
            )
        mean = get_value(self.mean())
        return sum((val - mean)**2 for val in self) / len(self)

    def var_s(self) -> Value:
        """Calculates the sample variance."""
        if len(self) < 2:
            raise ValueError(
                "Sample variance requires at least 2 data points."
            )
        mean = get_value(self.mean())
        return sum((val - mean)**2 for val in self) / (len(self) - 1)

    def stdev_p(self) -> Value:
        """Calculates the population standard deviation."""
        return self.var_p()**0.5

    def stdev_s(self) -> Value:
        """Calculates the sample standard deviation."""
        return self.var_s()**0.5

    def iter_currency(self) -> Generator[Currency]:
        return (Currency(get_value(val)) for val in self)

    def iter_percent(self) -> Generator[Percent]:
        return (Percent(get_value(val)) for val in self)

    def iter_number(self) -> Generator[number]:
        return (get_value(val) for val in self)

    def as_currency(self) -> Self:
        return self.__class__(self.iter_currency())

    def as_percent(self) -> Self:
        return self.__class__(self.iter_percent())

    def as_number(self) -> Self:
        return self.__class__(self.iter_number())


if __name__ == "__main__":
    s = Span([1, 2, 300, Currency(100), Percent(0.1)])
    u = Span([1, 2, 3, 4, 5])
    v = Span([1, 2, 3, 4, 5, 6])

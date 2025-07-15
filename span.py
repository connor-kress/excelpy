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
            new_items = [
                add_values(a, b)
                for a, b in zip_longest(self.values, other.values, fillvalue=0)
            ]
        else:
            new_items = map(partial(add_values, b=other), self.values)
        return self.__class__(new_items)

    def __radd__(self, other: Self | Value) -> Self:
        return self.__add__(other)

    def __neg__(self) -> Self:
        return self.__class__([-item for item in self.values])

    def __sub__(self, other: Self | Value) -> Self:
        return self.__add__(-other)

    def __rsub__(self, other: Self | Value) -> Self:
        return (-self).__add__(other)

    def __mul__(self, other: Value) -> Self:
        return self.__class__([item*get_value(other) for item in self.values])
    
    def __rmul__(self, other: Value) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: Value) -> Self:
        return self.__class__([item/get_value(other) for item in self.values])

    def __pow__(self, other: Value) -> Self:
        return self.__class__([item**get_value(other) for item in self.values])
    
    def __repr__(self) -> str:
        if len(self.values) == 0:
            return "┌───────┐\n" \
                   "│ Empty │\n" \
                   "└───────┘"
        item_strs = list(map(str, self.values))
        max_len = max(map(len, item_strs))
        delimiter = "├" + "─"*(max_len+2) + "┤\n"
        s = "┌" + "─"*(max_len+2) + "┐\n"
        for i, item_str in enumerate(item_strs):
            s += f"│ {item_str:>{max_len}} │\n"
            if i < len(item_strs) - 1:
                s += delimiter
            else:
                s += "└" + "─"*(max_len+2) + "┘"
        return s

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> Iterator[Value]:
        return iter(self.values)

    def iter_currency(self) -> Generator[Currency]:
        return (Currency(get_value(item)) for item in self.values)

    def iter_percent(self) -> Generator[Percent]:
        return (Percent(get_value(item)) for item in self.values)

    def iter_number(self) -> Generator[number]:
        return (get_value(item) for item in self.values)

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

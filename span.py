from functools import partial
from itertools import zip_longest
from typing import Iterable, Self
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
    def __init__(self, items: Iterable[Value]):
        for item in items:
            if not isinstance(item, Value):
                raise TypeError("items must be a number, Currency, or Percent")
        self.items = list(items)

    def __add__(self, other: Self | Value) -> Self:
        if isinstance(other, Span):
            new_items = [
                add_values(a, b)
                for a, b in zip_longest(self.items, other.items, fillvalue=0)
            ]
        else:
            new_items = list(map(partial(add_values, b=other), self.items))
        return self.__class__(new_items)

    def __radd__(self, other: Self | Value) -> Self:
        return self.__add__(other)

    def __neg__(self) -> Self:
        return self.__class__([-item for item in self.items])

    def __sub__(self, other: Self | Value) -> Self:
        return self.__add__(-other)

    def __rsub__(self, other: Self | Value) -> Self:
        return (-self).__add__(other)

    def __mul__(self, other: Value) -> Self:
        return self.__class__([item*get_value(other) for item in self.items])
    
    def __rmul__(self, other: Value) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: Value) -> Self:
        return self.__class__([item/get_value(other) for item in self.items])

    def __pow__(self, other: Value) -> Self:
        return self.__class__([item**get_value(other) for item in self.items])
    
    def __repr__(self) -> str:
        item_strs = list(map(str, self.items))
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


if __name__ == "__main__":
    s = Span([1, 2, 300, Currency(100), Percent(0.1)])
    u = Span([1, 2, 3, 4, 5])
    v = Span([1, 2, 3, 4, 5, 6])

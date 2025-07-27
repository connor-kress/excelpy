import math
import operator
from functools import reduce
from itertools import zip_longest
from typing import Generator, Iterable, Iterator, Self
from currency import Currency
from percent import Percent
from util import get_value, number
from value import Value, ValueType


class Span:
    def __init__(self, values: Iterable[Value | ValueType]):
        self.values = list(map(Value, values))
        for val in self.values:
            if not isinstance(val, Value):
                raise TypeError("Span values must be of a numeric type.")

    def __add__(self, other: Self | Value) -> Self:
        if isinstance(other, Span):
            new_values = (
                a + b for a, b in zip_longest(self, other, fillvalue=0)
            )
        else:
            new_values = (a + other for a in self)
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

    def clear(self) -> None:
        self.values.clear()

    def copy(self) -> Self:
        return self.__class__(val.copy() for val in self)

    def convert_inferred_type(self, val: float) -> Value:
        """Converts a float to the inferred type of the Span."""
        ret_cls = self.values[0].data.__class__
        if ret_cls.__name__ == "int":
            ret_cls = float
        return Value(ret_cls(val))

    def sort(self) -> None:
        self.values.sort(key=Value.get_value)

    def sorted(self) -> Self:
        return self.__class__(sorted(self, key=Value.get_value))

    def reverse(self) -> None:
        self.values.reverse()

    def reversed(self) -> Self:
        values = self.values
        return self.__class__(reversed(values))

    def clamp(self, b: Value, t: Value) -> Self:
        return self.__class__(
            val.clamp(b, t) for val in self
        )

    def sum(self) -> Value:
        return sum(self, Value(0))

    def prod(self) -> Value:
        return reduce(operator.mul, self, 1)

    def mean(self) -> Value:
        if len(self) == 0:
            raise ValueError("Cannot calculate mean of empty set.")
        return self.sum() / len(self)

    def var_p(self) -> float:
        """Calculates the population variance."""
        if len(self) == 0:
            raise ValueError(
                "Cannot calculated population variance of empty set."
            )
        mean = self.mean().get_value()
        return sum((val - mean)**2 for val in self.iter_number()) / len(self)

    def var_s(self) -> float:
        """Calculates the sample variance."""
        if len(self) < 2:
            raise ValueError(
                "Sample variance requires at least 2 data points."
            )
        mean = self.mean().get_value()
        return sum(
            (val - mean)**2 for val in self.iter_number()
        ) / (len(self) - 1)

    def stdev_p(self) -> Value:
        """Calculates the population standard deviation."""
        return self.convert_inferred_type(self.var_p()**0.5)

    def stdev_s(self) -> Value:
        """Calculates the sample standard deviation."""
        return self.convert_inferred_type(self.var_s()**0.5)

    def quantile(self, q: float) -> Value:
        """Calculates the quantile of the data using the
        weighted average of the two nearest values.
        """
        n = len(self)
        if n == 0:
            raise ValueError("Cannot calculate quantile of empty set.")
        if not 0 <= q <= 1:
            raise ValueError("Quantile must be between 0 and 1.")
        values = sorted(self.iter_number())
        if n == 1:
            return self.convert_inferred_type(values[0])
        h = (n - 1) * q
        i = int(math.floor(h))
        f = h - i
        if f == 0:
            return self.convert_inferred_type(values[i])
        res = values[i] * (1 - f) + values[i + 1] * f
        return self.convert_inferred_type(res)

    def median(self) -> Value:
        return self.quantile(0.5)

    def iter_currency(self) -> Generator[Currency]:
        return (Currency(val.get_value()) for val in self)

    def iter_percent(self) -> Generator[Percent]:
        return (Percent(val.get_value()) for val in self)

    def iter_number(self) -> Generator[number]:
        return (val.get_value() for val in self)

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

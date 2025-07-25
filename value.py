from currency import Currency
from percent import Percent
from util import get_value, number
from typing import Self


ValueType = number | Currency | Percent


class Value:
    def __init__(self, data: Self | ValueType):
        if isinstance(data, self.__class__):
            self.data: ValueType = data.data
        else:
            self.data: ValueType = data # type: ignore

    def copy(self) -> Self:
        if isinstance(self.data, number):
            return self.__class__(self.data)
        else:
            return self.__class__(self.data.copy())

    def __neg__(self) -> Self:
        return self.__class__(-self.data)

    def __add__(self, other: Self | ValueType) -> Self:
        a = self.data
        if isinstance(other, self.__class__):
            b: ValueType = other.data
        else:
            b: ValueType = other # type: ignore
        if isinstance(a, Currency) and isinstance(b, Percent):
            res = Currency(a.value + b.value)
        elif isinstance(a, Percent) and isinstance(b, Currency):
            res = Percent(a.value + b.value)
        else:
            res = a + b # type: ignore
        return self.__class__(res)

    def __radd__(self, other: Self | ValueType) -> Self:
        return self + other

    def __sub__(self, other: Self | ValueType) -> Self:
        return self + (-other)

    def __rsub__(self, other: Self | ValueType) -> Self:
        return (-self) + other

    def __mul__(self, other: Self | ValueType) -> Self:
        return self.__class__(self.data * get_value(other))
    
    def __rmul__(self, other: Self | ValueType) -> Self:
        return self * other
    
    def __truediv__(self, other: Self | ValueType) -> Self:
        return self.__class__(self.data / get_value(other))

    def __rtruediv__(self, other: Self | ValueType) -> Self:
        return self.__class__(get_value(other) / self.data)

    def __pow__(self, other: Self | ValueType) -> Self:
        return self.__class__(self.data ** get_value(other))
    
    def __rpow__(self, other: Self | ValueType) -> Self:
        return self.__class__(get_value(other) ** self.data)

    def __repr__(self) -> str:
        return repr(self.data)
    
    def __str__(self) -> str:
        return str(self.data)

    def get_value(self) -> number:
        return get_value(self.data)

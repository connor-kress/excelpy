from typing import Self
from util import get_value, number


class Percent:
    def __new__(cls, value: Self | number) -> Self:
        if isinstance(value, cls):
            return value
        return super().__new__(cls)

    def __init__(self, value: Self | number) -> None:
        if isinstance(value, Percent):
            return
        self.value = float(value)

    def __add__(self, other: Self | number) -> Self:
        if not isinstance(other, self.__class__ | number):
            return NotImplemented
        return self.__class__(self.value + get_value(other))

    def __radd__(self, other: number) -> Self:
        return self + other
    
    def __sub__(self, other: Self | number) -> Self:
        if not isinstance(other, self.__class__ | number):
            return NotImplemented
        return self.__class__(self.value - get_value(other))

    def __rsub__(self, other: number) -> Self:
        return self.__class__(other - self.value)

    def __mul__(self, other: number) -> Self:
        if not other.__class__ in (float, int):
            return NotImplemented
        return self.__class__(self.value * other)

    def __rmul__(self, other: number) -> Self:
        return self * other

    def mul(self, other: Self) -> Self:
        return self.__class__(self.value * other.value)
    
    def __truediv__(self, other: number) -> Self:
        return self.__class__(self.value / other)

    def __rtruediv__(self, other: number) -> float:
        return other / self.value

    def div(self, other: Self) -> float:
        return self.value / other.value

    def __pow__(self, other: number) -> Self:
        return self.__class__(self.value ** other)

    def __rpow__(self, other: number) -> float:
        return other ** self.value

    def __neg__(self) -> Self:
        return self.__class__(-self.value)

    def __repr__(self) -> str:
        return f"{self.value:.2%}"

    def __str__(self) -> str:
        return repr(self)

    def copy(self) -> Self:
        return self.__class__(self.value)

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

    def clamp(self, b: Self | ValueType, t: Self | ValueType) -> Self:
        self_val = self.data
        b_val = b.data if isinstance(b, self.__class__) else b
        t_val = t.data if isinstance(t, self.__class__) else t
        ret_cls = self_val.__class__
        if ret_cls.__name__ == "int"  and (
            b_val.__class__.__name__ != "int" or
            t_val.__class__.__name__ != "int"
        ):
            ret_cls = float
        return self.__class__(ret_cls(
            min(
                max(get_optional_value(self), get_optional_value(b)),
                get_optional_value(t),
            )
        ))

def get_optional_value(val: Value | ValueType) -> number:
    if isinstance(val, Value):
        return get_value(val.data)
    else:
        return get_value(val)

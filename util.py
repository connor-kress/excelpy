from typing import Protocol


number = float | int


class HasValue(Protocol):
    value: float


def get_value(obj: number | HasValue) -> float:
    if isinstance(obj, number):
        return obj
    else:
        return obj.value

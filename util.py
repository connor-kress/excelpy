from typing import Protocol


type number = float | int


class HasValue(Protocol):
    value: float


def get_value(obj: number | HasValue) -> float:
    if isinstance(obj, float | int):
        return obj
    else:
        return obj.value

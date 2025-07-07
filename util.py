from typing import Protocol


type number = float | int


class HasValue(Protocol):
    value: float


def get_value(obj: HasValue | float | int) -> float:
    if isinstance(obj, float | int):
        return obj
    else:
        return obj.value

from typing import Any, Protocol


number = float | int


class HasValue(Protocol):
    value: float


class HasData(Protocol):
    data: Any


def get_value(obj: number | HasValue | HasData) -> float:
    if isinstance(obj, number):
        return obj
    try:
        return obj.value # type: ignore
    except AttributeError:
        return obj.data.value # type: ignore

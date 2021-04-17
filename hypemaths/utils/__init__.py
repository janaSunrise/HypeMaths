import typing as t

from ..models import Vector


def linspace(start: t.Union[int, float], end: t.Union[int, float], count: int) -> list:
    step = (end - start) / (count - 1)
    linear_space = [start + step * i for i in range(count)]

    return linear_space


def scale_value(value: t.Union[int, float], old_range: tuple, new_range: tuple) -> t.Union[int, float]:
    old_range_v = old_range[1] - old_range[0]
    new_range_v = new_range[1] - new_range[0]

    new_value = (((value - old_range[0]) * new_range_v) / old_range_v) + new_range[0]
    return new_value


def scale_list(dataframe: Vector, range_: tuple) -> Vector:
    old_range = (min(dataframe.points), max(dataframe.points))

    scaled_list = [round(scale_value(elem, old_range, range_)) for elem in dataframe.points]
    return Vector(scaled_list)


def norm(vector: Vector, p: t.Union[int, float] = 2) -> t.Union[int, float]:
    return sum(elem ** p for elem in vector.points) ** (1 / p)

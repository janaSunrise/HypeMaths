import math
import typing as t

from ..mixins import CopyMixin


class Point(CopyMixin):
    def __init__(self, x: t.Union[int, float], y: t.Union[int, float]) -> None:
        self.x = self.cleaned_point_value(x)
        self.y = self.cleaned_point_value(y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def cleaned_point_value(value: t.Any) -> t.Union[int, float]:
        if not isinstance(value, (int, float)):
            raise TypeError(f"All points must be integers or floats, but the value is {type(value)}")

        return value

    def calculate_distance(self, other: t.Union["Point", tuple, list]) -> t.Union[int, float]:
        if isinstance(other, self.__class__):
            x = self.x
            y = self.y
        elif isinstance(other, (tuple, list)):
            x, y = other
        else:
            raise TypeError("The other value must be a tuple, list or another Point.")

        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance

    def to_tuple(self) -> tuple:
        return self.x, self.y

import math
import typing as t

import hypemaths as hm
from ..exceptions import MatrixDimensionError, VectorDimensionError
from ..mixins import CopyMixin


class Vector(CopyMixin):
    def __init__(self, *points: t.Union[int, tuple, list]) -> None:
        """
        Constructor for the `Vector` class.
        Parameters
        ----------
        points: tuple
            All the points for the vector.
        """
        self.points = self._cleaned_vector(points)

        # Get the XYZW Dimensions
        if self.dimensions <= 4:
            for attribute, value in zip(list("xyzw"), self.points):
                setattr(self, attribute, value)

    @staticmethod
    def _cleaned_vector(points: tuple) -> list:
        """
        Clean and validate the vector by using this method.
        Parameters
        ----------
        points: tuple
            The vector points stored in it.
        Returns
        -------
        list:
            The cleaned vector,
        """
        def value_check(vector_points: list) -> bool:
            for index, point in enumerate(vector_points):
                if not isinstance(point, (int, float)):
                    raise TypeError(f"All points must be integers or floats, but point[{index}] is {type(point)}")

            return True

        if len(points) == 1 and isinstance(points[0], list):
            points = points[0]
        else:
            points = list(points)

        if not value_check(points):
            pass

        return points

    @property
    def dimensions(self) -> int:
        """
        Return the dimensions of the vector object.
        Returns
        -------
        The length / dimension of the vector.
        """
        return len(self)

    def __len__(self) -> int:
        return len(self.points)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.points})"

    def __eq__(self, other: "Vector") -> bool:
        if not isinstance(other, Vector):
            raise TypeError(
                f"Equality comparison with vector can only be performed with another vector, got {type(other)}"
            )

        return self.points == other.points

    def __getitem__(self, index: int) -> t.Union[int, float]:
        return self.points[index]

    def __setitem__(self, index: t.Union[int, tuple], value: t.Union[int, float]) -> None:
        if isinstance(value, (int, float)):
            self.points[index] = value
        else:
            raise TypeError(
                f"All values must be integers or floats, but value[{value}] is {type(value)}."
            )

    def __delitem__(self, index: int) -> None:
        del self.points[index]

    def __add__(self, other: "Vector") -> "Vector":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Vector can only be added with another Vector, not with {type(other)}")

        if self.dimensions != other.dimensions:
            raise VectorDimensionError(
                "These vectors cannot be added due to wrong dimensions."
            )

        vector = [self[index] + other[index]
                  for index in range(self.dimensions)]
        return cls(vector)

    def __sub__(self, other: "Vector") -> "Vector":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Vector can only be subtracted with another Vector, not with {type(other)}")

        if self.dimensions != other.dimensions:
            raise VectorDimensionError(
                "These vectors cannot be subtracted due to wrong dimensions."
            )

        vector = [self[index] - other[index] for index in range(self.dimensions)]
        return cls(vector)

    def __matmul__(self, other: "Vector") -> float:
        if self.dimensions != other.dimensions:
            raise VectorDimensionError("These vectors cannot be multiplied due to wrong dimensions.")

        return sum(x * y for x, y in zip(self, other))

    def __mul__(self, other: "Vector") -> "Vector":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Vector can only be added with another Vector, not with {type(other)}")

        if self.dimensions != other.dimensions:
            raise VectorDimensionError(
                "These vectors cannot be added due to wrong dimensions."
            )

        vector = [self[index] * other[index]
                  for index in range(self.dimensions)]
        return cls(vector)

    def __truediv__(self, other: "Vector") -> "Vector":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Vector can only be added with another Vector, not with {type(other)}")

        if self.dimensions != other.dimensions:
            raise VectorDimensionError(
                "These vectors cannot be added due to wrong dimensions."
            )

        vector = [self[index] / other[index] for index in range(self.dimensions)]
        return cls(vector)

    def __floordiv__(self, other: "Vector") -> "Vector":
        return self.__truediv__(other)

    def __radd__(self, other: "Vector") -> "Vector":
        return self.__add__(other)

    def __abs__(self) -> "Vector":
        cls = self.__class__

        points = [abs(point) for point in self.points]
        return cls(*points)

    @staticmethod
    def absolute(param: t.Any) -> float:
        points = math.sqrt(param @ param)
        return points

    @classmethod
    def from_matrix(cls, matrix: "hm.Matrix") -> "Vector":
        """
        Create a `vector` object by flattening a `matrix`.
        Parameters
        ----------
        matrix: Matrix
            The matrix to be converted into a vector.
        Returns
        -------
        Vector:
            The converted vector.
        """
        if matrix.cols != 1:
            raise MatrixDimensionError("Matrix must only have 1 column.")

        points = [column[0] for column in matrix]
        return cls(*points)

    @classmethod
    def from_point(cls, point: "hm.Point") -> "Vector":
        points = point.x, point.y
        return cls(*points)

    def parallel_to(self, other: "Vector") -> bool:
        """
        Check if the Vectors are parallel to each other.

        Parameters
        ----------
        other: Vector
            The other vector to be compared.

        Returns
        -------
        bool
            If it's parallel or not.
        """
        return math.isclose(abs(self @ other), self.absolute(self) * self.absolute(other))

    def orthogonal_to(self, other: "Vector") -> bool:
        """
        Check if the Vectors are at a orthogonal from each other.

        Parameters
        ----------
        other: Vector
            The other vector to be compared.

        Returns
        -------
        bool
            If it's at an orthogonal distance.
        """
        return math.isclose(self @ other, 0)

    def mean(self, decimal: int = 2) -> float:
        """
        Returns the mean, which is the sum of all the elements divided by the number of elements

        Parameters
        ----------
        decimal: Optional, defaultes to 2
            To what decimal point the output should be rounded

        Returns
        -------
        float:
            The mean of the vector

        Examples
        --------
        >>> x = Vector([1, 2, 3])
        >>> x.mean()
        2.0
        >>> y = Vector([1.7, 2.6, 3])
        >>> y.mean(decimal=4)
        2.4333
        """
        if not isinstance(decimal, int):
            raise TypeError(f"Decimal parameter should be an integer not {type(decimal)}")
        else:
            mean = sum(self.points) / len(self.points)
            return round(mean, decimal)

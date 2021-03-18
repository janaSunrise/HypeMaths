import typing as t

import hypemaths as hm
from hypemaths.exceptions import MatrixDimensionError, VectorDimensionError


class Vector:
    def __init__(self, *points: t.Union[int, tuple, list]) -> None:
        """
        Constructor for the `Vector` class.
        Parameters
        ----------
        points: tuple
            All the points for the vector.
        """
        self.points = self._cleaned_vector(points)

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
                    raise TypeError(
                        f"All points must be integers or floats, but point[{index}] is {type(point)}")
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

        vector = [self[index] - other[index]
                  for index in range(self.dimensions)]
        return cls(vector)

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

        vector = [self[index] / other[index]
                  for index in range(self.dimensions)]
        return cls(vector)

    def __floordiv__(self, other: "Vector") -> "Vector":
        return self.__truediv__(other)

    def __radd__(self, other: "Vector") -> "Vector":
        return self.__add__(other)

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
            raise TypeError(
                f"Decimal parameter should be an integer not {type(decimal)}")
        else:
            mean = sum(self.points) / len(self.points)
            return round(mean, decimal)

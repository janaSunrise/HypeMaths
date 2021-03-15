import copy
import math
import random
import typing as t

import hypemaths as hm
from hypemaths.exceptions import (
    InvalidMatrixError,
    MatrixDimensionError,
    MatrixNotSquare,
)


class Matrix:
    def __init__(
            self,
            matrix: t.Union[int, float, list] = None,
    ) -> None:
        """
        Parameters
        ----------
        matrix : t.Union[int, float, list]
            This is the nested 2D lists which will be converted into an efficient `Matrix` object capable of several
            calculations and features. Defaults to `None`.
        """
        if not matrix:
            raise ValueError("You need to pass the 2D for the matrix object!")
        else:
            self.matrix = self._cleaned_matrix(matrix)

    @property
    def rows(self) -> int:
        """
        Returns
        -------
        int
            The number of rows in the 2D matrix created.
        """
        return len(self.matrix)

    @property
    def cols(self) -> int:
        """
        Returns
        -------
        int
            The number of the columns in the 2D matrix created.
        """
        return len(self.matrix[0])

    @property
    def dims(self) -> tuple:
        """
        Returns
        -------
        tuple
            The tuple containing the shape or the rows and columns in the matrix created.
        """
        return tuple(self._get_mat_dimension(self.matrix))

    @property
    def size(self) -> int:
        """
        Returns
        -------
        int
            The integer which is the total number of items in the matrix
        """
        matrix = Matrix(self.matrix)
        return matrix.cols * matrix.rows

    def __repr__(self) -> str:
        return "{}([{}])".format(self.__class__.__name__, ",\n         ".join([str(x) for x in self.matrix]))

    def __eq__(self, other: "Matrix") -> bool:
        if not isinstance(other, Matrix):
            raise TypeError(
                f"Equality comparison with Matrix can only be performed with another Matrix, got {type(other)}"
            )

        return self.matrix == other.matrix

    def __getitem__(self, index: t.Union[int, tuple]) -> t.Union[int, float, list]:
        if isinstance(index, int):
            return self.matrix[index]
        else:
            return self.matrix[index[0]][index[1]]

    def __setitem__(self, index: t.Union[int, tuple], value: t.Union[int, float]) -> None:
        if isinstance(value, (int, float)):
            if isinstance(index, int):
                self.matrix[index] = value
            else:
                self.matrix[index[0]][index[1]] = value
        else:
            raise TypeError(
                f"All values must be integers or floats, but value[{value}] is {type(value)}."
            )

    def __add__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Matrix can only be added with other matrix. Not {type(other)}")

        if not (self.rows, self.cols) == (other.rows, other.cols):
            raise MatrixDimensionError(
                "These matrices cannot be added due to wrong dimensions.")

        matrix = [[self[row][cols] + other[row][cols]
                   for cols in range(self.cols)] for row in range(self.rows)]

        return cls(matrix)

    def __sub__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(
                f"Matrix can only be subtracted with other matrix. Not {type(other)}")

        if not (self.rows, self.cols) == (other.rows, other.cols):
            raise MatrixDimensionError(
                "These matrices cannot be subtracted due to wrong dimensions.")

        matrix = [[self[row][cols] - other[row][cols]
                   for cols in range(self.cols)] for row in range(self.rows)]

        return cls(matrix)

    def __mul__(self, other: t.Union["Matrix"]) -> "Matrix":
        cls = self.__class__

        if isinstance(other, (int, float)):
            matrix = [[element * other for element in row] for row in self]
            return cls(matrix)

        if not isinstance(other, cls):
            raise TypeError(
                f"Matrix can only be multiplied with other matrix. Not {type(other)}")

        if self.cols != other.rows:
            raise MatrixDimensionError(
                "These matrices cannot be multiplied due to wrong dimensions.")

        matrix = [[
            sum(a * b for a, b in zip(self_row, other_col)) for other_col in zip(*other)] for self_row in self
        ]

        return cls(matrix)

    def __truediv__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if isinstance(other, (int, float)):
            matrix = [[element / other for element in row] for row in self]
            return cls(matrix)

        if not isinstance(other, cls):
            raise TypeError(
                f"Matrix can only be divided with other matrix. Not {type(other)}")

        if self.cols != other.rows:
            raise MatrixDimensionError(
                "These matrices cannot be divided due to wrong dimensions.")

        matrix = [[
            sum(a / b for a, b in zip(self_row, other_col)) for other_col in zip(*other)] for self_row in self
        ]

        return cls(matrix)

    def __radd__(self, other: "Matrix") -> "Matrix":
        return self.__add__(other)

    def __rmul__(self, other: "Matrix") -> "Matrix":
        return self.__mul__(other)

    def __matmul__(self, other: "Matrix") -> "Matrix":
        return self.__mul__(other)

    def __abs__(self) -> "Matrix":
        cls = self.__class__

        matrix = [[abs(self[row][cols]) for cols in range(self.cols)]
                  for row in range(self.rows)]
        return cls(matrix)

    def __round__(self, n: t.Optional[int] = None) -> "Matrix":
        cls = self.__class__

        matrix = [[round(self[row][cols], ndigits=n)
                   for cols in range(self.cols)] for row in range(self.rows)]
        return cls(matrix)

    def __int__(self) -> "Matrix":
        cls = self.__class__

        matrix = [[int(self[row][cols]) for cols in range(self.cols)]
                  for row in range(self.rows)]
        return cls(matrix)

    def __float__(self) -> "Matrix":
        cls = self.__class__

        matrix = [[float(self[row][cols]) for cols in range(self.cols)]
                  for row in range(self.rows)]
        return cls(matrix)

    @classmethod
    def get_filled_matrix(cls, dims: tuple, fill: t.Union[int, float]) -> "Matrix":
        """
        Create a Matrix object with dimension specified containing fill value specified.
        Parameters
        ----------
        dims : tuple
            This is the dimensions of the fill matrix, created when the `matrix` parameter is not specified and only
            this value and the fill value is provided. Defaults to `None`.
        fill : t.Union[int, float]
            This is the fill value, which works with the `dims` parameter to create a filled matrix with the given
            value. Defaults to `None`.
        Returns
        -------
        Matrix
            Returns filled matrix object with the dimensions and fill value passed.
        Examples
        --------
        Create a matrix of dimensions : (2, 2) with the fill value of 5.
        >>> matrix = Matrix.get_filled_matrix((2, 2), 5)
        >>> matrix
        Matrix([[5, 5], [5, 5]])
        Create a matrix of dimensions : (4, 3) with the fill value 9
        >>> matrix = Matrix.get_filled_matrix((4, 3), 9)
        >>> matrix
        Matrix([[9, 9, 9], [9, 9, 9], [9, 9, 9], [9, 9, 9]])
        """
        return cls(cls._create_filled_matrix(dims, fill))

    @classmethod
    def get_randomized_matrix(
            cls, dims: tuple, min_value: int, max_value: int, seed: int = None, round_digits: t.Optional[int] = 2
    ) -> "Matrix":
        """
        Generate a random matrix object with the specified parameters.
        Parameters
        ----------
        dims: tuple
            The dimensions for the matrix to be generated.
        min_value: int
            The minimum value for random number generation
        max_value: int
            The maximum value for random number generation
        seed: int
            The seed for random numer generation which can be recreated later.
        round_digits: int
            The number of digits to be in the number after decimal. Set the value as number for integer values.
        Returns
        -------
        Matrix
            The random matrix generated from the function.
        Examples
        --------
        Generate a matrix with random integer values
        >>> matrix = Matrix.get_randomized_matrix((2, 2), 1, 10, round_digits=None)
        >>> matrix
        Matrix([[4, 9], [9, 2]])
        Generate a reproducible matrix with seed of 7
        >>> matrix = Matrix.get_randomized_matrix((2, 2), 1, 10, seed=7)
        >>> matrix
        Matrix([[3.91, 2.36], [6.86, 1.65]])
        Generate a float matrix with 5 digits after decimal
        >>> matrix = Matrix.get_randomized_matrix((2, 2), 1, 10, round_digits=5)
        >>> matrix
        Matrix([[5.82294, 4.2912], [1.52199, 5.56692]])
        """
        def is_float_or_int(value: t.Any) -> bool:
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"The values or value must be integer or float, but the given fill value is {type(value)}."
                )
            return True

        if len(dims) != 2:
            raise ValueError(
                "You must pass the 2 DIMENSIONS for the Matrix fill.")

        if is_float_or_int(min_value) and is_float_or_int(max_value):
            if seed is not None:
                random.seed(seed)

            if not round_digits:
                matrix = [
                    [
                        round(random.uniform(min_value, max_value)) for _ in range(dims[1])
                    ] for _ in range(dims[0])
                ]
                return cls(matrix)
            else:
                matrix = [
                    [
                        round(random.uniform(min_value, max_value), ndigits=round_digits) for _ in range(dims[1])
                    ] for _ in range(dims[0])
                ]
                return cls(matrix)

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
        """
        Checks if a matrix passed is valid or not and returns the processed and cleaned matrix.
        Parameters
        ----------
        matrix : list
            The matrix passed to this function for processing, validation and cleaning.
        Returns
        -------
        list
            The list consisting the validated and cleaned matrix after passing the checks.
        Raises
        ------
        TypeError
            If the matrix contains any datatype other than `int` or `float`.
        InvalidMatrixError
            If the matrix has invalid size or cannot be validated.
        """
        def contains_sublist(mat: list) -> bool:
            """
            Parameters
            ----------
            mat: list
                The matrix passed for checking if it contains sublist.
            Returns
            -------
            bool
                If the matrix passed contains sublist.
            """
            return all(isinstance(element, list) for element in mat)

        def value_check(mat: list) -> bool:
            """
            Parameters
            ----------
            mat: list
                The matrix passed for validating the datatypes in it.
            Returns
            -------
            bool
                If the matrix contains any datatypes other than `int` or `float`.
            Raises
            ------
            TypeError
                Raised if the matrix consists of value which is not a `int` or `float`.
            """
            for row, row_values in enumerate(mat):
                for col, value in enumerate(row_values):
                    if not isinstance(value, (int, float)):
                        raise TypeError(
                            f"All values must be integers or floats, but value[{row}][{col}] is {type(value)}"
                        )
            return True

        if isinstance(matrix, (int, float)):
            return [[matrix]]

        matrix = [matrix] if not contains_sublist(matrix) else matrix
        if value_check(matrix):
            len_set = set([len(x) for x in matrix])
            if len(len_set) > 1 and value_check(matrix):
                raise InvalidMatrixError(
                    "Matrix sizes are invalid! Must have same number of element in each sub list."
                )
            return matrix

    @staticmethod
    def _create_filled_matrix(dims: tuple, fill: t.Union[int, float] = None) -> list:
        """
        Parameters
        ----------
        dims: tuple
            The dimensions for the matrix to be initialized. Only 2 dimensions (X, Y) are allowed.
        fill: t.Union[int, float]
            The value to be filled across the matrix of the specified dimension.
        Returns
        -------
        list
            The 2D python list, to be converted into `Matrix` object.
        Raises
        ------
        ValueError
            If the number of dimensions don't equal to 2.
        TypeError
            If the fill value isn't either `int` or `float`.
        """
        if len(dims) != 2:
            raise ValueError(
                "You must pass the 2 DIMENSIONS for the Matrix fill.")

        if not fill:
            fill = 0

        if not isinstance(fill, (int, float)):
            raise TypeError(
                f"The fill value must be integer or float, but the given fill value is {type(fill)}."
            )

        matrix_structure = []
        first_row = [fill] * dims[1]
        for _ in range(dims[0]):
            matrix_structure.append(first_row.copy())

        return matrix_structure

    def _get_mat_dimension(self, matrix: list) -> list:
        """
        Parameters
        ----------
        matrix : list
            The matrix whose dimensions are to be figured out.
        Returns
        -------
        list
            A tuple containing the dimensions of the matrix passed.
        """
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

    def clone(self) -> "Matrix":
        """
        Returns the copy of the matrix.
        Returns
        -------
        Matrix
            The copy of the present matrix.
        Examples
        --------
        Getting the copy instead of directly assigning, when you want to modify the matrix without disturbing the first one.
        >>> matrix = Matrix([[1, 2], [3, 4]])
        >>> matrix.clone()
        Matrix([[1, 2], [3, 4]])
        """
        return copy.deepcopy(self)

    def trace(self) -> t.Union[int, float]:
        """
        Returns the sum of the diagonals of the matrix
        Returns
        -------
        t.Union[int, float]
            The sum of the diagonals of the current `Matrix`
        Raises
        ------
        MatrixNotSquare
            If the number of columns and rows are not equal in the `Matrix`.
        Examples
        --------
        Getting the sum of the rows of the specified matrix.
        >>> matrix = Matrix([[5, 5], [3, 4]])
        >>> matrix.trace()
        9
        """
        if self.rows != self.cols:
            raise MatrixNotSquare(
                "Cannot retrieve the sum of diagonals as the row and column count are not same.")

        total = 0
        for i in range(self.rows):
            total += self[i, i]
        return total

    def transpose(self) -> "Matrix":
        """
        Transposes the matrix.
        This converts the matrix elements order, by converting the rows into columns and vice versa.
        Returns
        -------
        Matrix
            The transposed matrix.
        Examples
        --------
        >>> mat = Matrix([[1, 2], [3, 4]])
        >>> mat.transpose()
        Matrix([[1, 3], [2, 4]])
        """
        cls = self.__class__

        matrix = [[self[cols][row]
                   for cols in range(self.rows)] for row in range(self.cols)]

        return cls(matrix)

    def frobenius_norm(self) -> float:
        """
        Calculate the frobenius norm of the matrix.
        The frobenius norm is computed by taking square root of the sums the squares of each entry of the matrix.
        This can be used to calculate the 2-norm of a column vector.
        Returns
        -------
        float:
            The computed frobenius norm.
        """
        sum_of_squares = 0
        for column in self.matrix:
            for elem in column:
                sum_of_squares += elem ** 2
        return math.sqrt(sum_of_squares)

    def determinant(self) -> float:
        """
        Get the determinant of a matrix.
        In linear algebra, the determinant is a scalar value that can be computed from the elements of a square
        matrix and encodes certain properties of the linear transformation described by the matrix. The determinant of
        a matrix A is denoted det, det A, or |A|.
        Returns
        -------
        float:
            The determinant of the matrix.
        """
        matrix_size = len(self.matrix)
        matrix_copy = self.clone()

        for fd in range(matrix_size):  # FD - The focus diagonal.
            for i in range(fd + 1, matrix_size):
                if matrix_copy[fd][fd] == 0:
                    matrix_copy[fd][fd] = 1.0e-18

                current_row_scaler = matrix_copy[i][fd] / matrix_copy[fd][fd]

                for j in range(matrix_size):
                    matrix_copy[i][j] = matrix_copy[i][j] - \
                        current_row_scaler * matrix_copy[fd][j]

        product = 1.0
        for i in range(matrix_size):
            product *= matrix_copy[i][i]

        return product

    @classmethod
    def from_vector(cls, vector: "hm.Vector") -> "Matrix":
        """
        Convert a `Vector` into a `Matrix` object.
        Parameters
        ----------
        vector: Vector
            The vector which is going to be converted into Matrix.
        Returns
        -------
        Matrix
            The matrix formed after conversion of vector.
        Examples
        --------
        >>> from hypemaths import Vector
        >>> vec = Vector(1, 2, 3, 4)
        >>> vec
        Vector([1, 2, 3, 4])
        >>> Matrix.from_vector(vec)
        Matrix([[1], [2], [3], [4]])
        """
        matrix_list = [[value] for value in vector]
        return cls(matrix_list)

    def flatten(self) -> "hm.Vector":
        """
        Return a flattened version of the matrix.
        All elements of the matrix are placed into a single row.

        Returns
        -------
        hm.Vector
            A vector containing the elements of the matrix passed.
        Examples
        --------
        >>> m = hm.Matrix([[1,2], [3,4]])
        >>> m.flatten()
        Vector([[1, 2, 3, 4]])
        """

        flat_list = []
        for element in self.matrix:
            if type(element) is list:
                # If the element is of type list, iterate through the sublist
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return hm.Vector(flat_list)

    def sum(self, axis: int = None) -> t.Union[int, float, "hm.Vector", "hm.Matrix"]:
        """
        Returns the sum of the entire matrix or along a specific axis

        Parameters
        ----------
        Axis: {0, 1}, Optional
            The sum of the matix along which axis

        Returns
        -------
        int, float
            The sum of the elements of the matrix

        Examples
        --------
        >>> m = Matrix([[1, 2], [4, 2], [7, 2]])
        >>> m.sum()
        18
        >>> m.sum(0)
        Matrix([[12, 6]])
        >>> m.sum(1)
        Matrix([[3], [6], [9]])
        """
        matrix = Matrix(self.matrix)
        if axis is None:
            return sum(matrix.flatten())

        if axis not in [-1, 0, 1, None]:
            raise TypeError(
                f"axis {axis} is out of bounds for array of dimension 2")

        if not isinstance(axis, (list, int)):
            raise TypeError(
                f"Axis should be int or list indices. Got {type(axis)}")
        if axis == 0:
            return Matrix([float(sum(i)) for i in zip(*matrix)])
        elif axis == 1:
            return Matrix([[sum(i)] for i in matrix])

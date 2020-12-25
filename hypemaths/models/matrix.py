import typing as t

from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(
            self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None
    ) -> None:
        if not matrix:
            if not dims or fill:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")

            self.matrix = self._create_filled_matrix(dims, fill)
        else:
            self.matrix = self._cleaned_matrix(matrix)

    @property
    def rows(self) -> int:
        return len(self.matrix)

    @property
    def columns(self) -> int:
        return len(self.matrix[0])

    @property
    def dims(self) -> tuple:
        return tuple(self._get_mat_dimension(self.matrix))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.matrix})"

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
        """Checks if a matrix passed is valid or not and returns the clean matrix."""
        def value_check(mat: list) -> bool:
            for row, row_values in enumerate(mat):
                for col, value in enumerate(row_values):
                    if not isinstance(value, (int, float)):
                        raise TypeError(
                            f"All values must be integers or floats, but value[{row}][{col}] is {type(value)}"
                        )
            return True

        if isinstance(matrix, (int, float)):
            return [[matrix]]

        if len(matrix) == 1:
            if isinstance(matrix[0], list):
                if value_check(matrix):
                    return matrix
            return [matrix]

        if len(matrix) >= 2:
            if isinstance(matrix[0], list):
                if value_check(matrix):
                    return matrix
            else:
                is_valid_matrix = all(isinstance(element, list) for element in matrix)
                if not is_valid_matrix:
                    len_set = set([len(x) for x in matrix])
                    if len(len_set) > 1 and value_check(matrix):
                        raise InvalidMatrixError(
                            "Matrix sizes are invalid! Must have same number of element in each sub list."
                        )
                return matrix

        raise InvalidMatrixError("Matrix sizes are invalid!")

    @staticmethod
    def _create_filled_matrix(dims: tuple, fill: t.Union[int, float]) -> list:
        if len(dims) != 2:
            raise ValueError("You must pass the 2 DIMENSIONS for the Matrix fill.")

        if not isinstance(fill, (int, float)):
            raise TypeError(
                f"The fill value must be integer or float, but the given fill value is {type(fill)}."
            )

        return [[fill] * dims[1]] * dims[0]

    def _get_mat_dimension(self, matrix: list) -> list:
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

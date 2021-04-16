import copy
import typing as t


class CopyMixin:
    def copy(self) -> t.Any:
        return copy.copy(self)

    def deepcopy(self) -> t.Any:
        return copy.deepcopy(self)

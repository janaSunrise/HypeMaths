import abc
import typing as t


class Integral(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format(self, func: t.Callable, a: t.Union[int, float], b: t.Union[int, float]) -> t.Any:
        raise NotADirectoryError

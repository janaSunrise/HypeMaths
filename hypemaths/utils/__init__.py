import typing as t


def linspace(start: t.Union[int, float], end: t.Union[int, float], count: int) -> list:
    step = (end - start) / (count - 1)
    linear_space = [start + step * i for i in range(count)]

    return linear_space

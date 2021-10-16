import abc


def swap_values_in(ary, x, y):
    if x == y:
        return
    ary[x], ary[y] = ary[y], ary[x]


class BaseSorter(abc.ABC):
    __slots__ = ('name')

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def sort(self, numbers):
        pass

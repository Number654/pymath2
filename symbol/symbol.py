# -*- coding: utf-8 -*-
from abc import ABC
from numbers import Real as RealNumber


class Assignator:

    def __init__(self):
        self.k = 1
        self.b = 0

    # Для арифметических операций с присваиванием
    def assign(self, other):
        if not isinstance(other, Assignator):
            raise TypeError("expected Assignator, got %s instead" % type(other))
        self.k = other.k
        self.b = other.b


class PySymbol(Assignator, RealNumber, ABC):

    def __init__(self):
        super(PySymbol, self).__init__()

    def __str__(self):
        return "symbol %s %s" % (self.k, self.b)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return 1

    def __abs__(self):
        return 1

    def __ceil__(self):
        return 1

    def __eq__(self, other):
        return 1

    def __float__(self):
        return 1.0

    def __floor__(self):
        return 1

    def __floordiv__(self, other):
        return 1

    def __le__(self, other):
        return 1

    def __lt__(self, other):
        return 1

    def __mod__(self, other):
        return 1

    def __mul__(self, other):
        return 1

    def __neg__(self):
        return 1

    def __pos__(self):
        return 1

    def __pow__(self, power):
        return 1

    def __radd__(self, other):
        return 1

    def __rfloordiv__(self, other):
        return 1

    def __rmod__(self, other):
        return 1

    def __rmul__(self, other):
        return 1

    def __round__(self, n=0):
        return 1

    def __rpow__(self, other):
        return 1

    def __rtruediv__(self, other):
        return 1

    def __truediv__(self, other):
        return 1

    def __trunc__(self):
        return 1


if __name__ == '__main__':
    from pymath2 import Fraction
    from math import log10

    a = PySymbol()
    print(log10(a))
    print(a)

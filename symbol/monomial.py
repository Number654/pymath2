# -*- coding: utf-8 -*-

from numbers import Real as RealNumber
from core.fractions import Fraction, Double, LiteralFraction, PeriodicFraction

VALID_SIGNS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class PySymbol:

    """
    Буква (переменная) в буквенном выражении.

    name - сама буква, например, a или x
    index - индекс переменной, например, x1 или a1
    """

    def __init__(self, name, index=None):
        if not isinstance(name, str):
            raise TypeError("expected str but %s given" % type(name))
        for s in name:
            if s not in VALID_SIGNS:
                raise ValueError("unexpected character: %s" % s)

        self.name = name if index is None else name+str(index)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__str__())


class Monomial:

    def __init__(self, mono):
        if not isinstance(mono, (RealNumber, Fraction, Double, LiteralFraction, PeriodicFraction, PySymbol)):
            raise TypeError
        if not isinstance(mono, PySymbol):
            self.koeff = mono
        else:
            self.koeff = 1
            self.variable = mono

    def __str__(self):
        return (str(self.koeff) if self.koeff != 1 else "") + (str(self.variable) if hasattr(self, "variable") else "")

    def __repr__(self):
        return str(self.__str__())

    def __abs__(self):
        return Monomial(self.var, k=abs(self.k))

    def __ceil__(self):
        return


if __name__ == '__main__':
    x = PySymbol("x", index=1)
    a = Monomial(x)
    print(a)

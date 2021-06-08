# -*- coding: utf-8 -*-

from copy import copy
from .fractions import to_fraction

"""
Решение уравнений на Python.

Основная задача - упростить уравнение до вида:
    kx ± y = z
    y ± kx = z

    xk ± y = z
    y ± xk = z

    k/x ± y = z
    y ± k/x = z

    x/k ± y = z
    y ± x/k = z

где k - коэффициент неизвестного,  x - само неизвестное, y - слагаемое или вычитаемое,
z - равное выражению число.
"""


def format_sign(x):
    return "-"+str(x).replace("-", "") if x < 0 else "+"+str(x).replace("+", "")


def get_sign(x):
    return "-" if x < 0 else "+"


# Абстрактный класс для двух типов уравнений: линейные и дробные
class AbstractSymbol:
    # Буква - это неизвестное, умноженное на коэффициент и сложенное с дополнительным числом.

    def __init__(self, k=1, y=0):
        self.k = k
        self.y = y

    # Одинаково для всех
    def __repr__(self):
        return str(self.__str__())

    # Изменить знак буквы на противоположный
    def __neg__(self):
        a = copy(self)
        a.k = -a.k
        a.y = -a.y
        return a

    # Сложить букву с числом
    def __add__(self, other):
        a = copy(self)
        if isinstance(other, AbstractSymbol):
            a.k += other.k
            a.y += other.y
        else:
            a.y += other
        return a

    # Сложить число с буквой
    def __radd__(self, other):
        return self.__add__(other)

    # Вычесть число из буквы
    def __sub__(self, other):
        return self.__add__(-other)

    # Из числа вычесть букву
    def __rsub__(self, other):
        return (-self).__add__(other)

    # Умножить букву на число
    def __mul__(self, other):
        if isinstance(other, AbstractSymbol):
            raise TypeError("'equations' module does not support 'power equations'")
        else:
            a = copy(self)
            a.k *= other
            a.y *= other
            return a

    # Умножить число на букву
    def __rmul__(self, other):
        return self.__mul__(other)

    # Разделить букву на число
    def __truediv__(self, other):
        if isinstance(other, AbstractSymbol):
            raise ValueError("x - any number")  # Неизвестные сократятся внутри дроби, останутся только числа
        a = copy(self)
        a.k /= other
        a.y /= other
        return a

    # Если дробь в ответе нельзя перевести в десятичную, то оставляем в видео обыконовенной
    @staticmethod
    def accurate_result(a, b):
        # Делим a на b (в виде дробей), если не получится перевести частное в десятичную дробь
        return to_fraction(to_fraction(a) / to_fraction(b)).reduce().format_to_mixed_number()

    # Решить уравнение
    def get(self, z):
        pass


# z = k*x+y
class LinearSymbol(AbstractSymbol):

    def __str__(self):
        return "%sx%s" % (self.k, format_sign(self.y))

    def get(self, z):
        return self.accurate_result(z-self.y, self.k)


# z = k/x+y
class FractionalSymbol(AbstractSymbol):

    def __str__(self):
        return "%s/x%s" % (self.k, format_sign(self.y))

    def get(self, z):
        return self.accurate_result(self.k, z-self.y)


# Уравнение, которое может менять свой вид
class Symbol(AbstractSymbol):

    def __init__(self, k=1, y=0):
        super().__init__(k=k, y=y)
        self.is_linear = True  # Является ли уравнение линейным?

    # Деление числа на букву - вот как уравнение меняет вид
    def __rtruediv__(self, other):
        if isinstance(other, AbstractSymbol):
            raise ValueError("x - any number")  # Неизвестные сократятся внутри дроби, останутся только числа
        self.is_linear = not self.is_linear  # Вид уравнения меняется на противоположный

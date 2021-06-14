# -*- coding: utf-8 -*-

from copy import copy
from .fractions import to_fraction

"""
Решение уравнений на Python.

Основная задача - упростить уравнение до вида:

    kx ± y = z
       или
    k/x ± y = z

где k - коэффициент неизвестного,  x - само неизвестное, y - слагаемое или вычитаемое,
z - равное выражению число (правая часть уравнения).
"""


def format_sign(x):
    return "-"+str(x).replace("-", "") if x < 0 else "+"+str(x).replace("+", "")


def get_sign(x):
    return "-" if x < 0 else "+"


class AnyNumber:

    def __str__(self):
        return "Any Number"

    def __repr__(self):
        return str(self.__str__())


# Абстрактный класс для двух типов уравнений: линейные и дробные
class SuperSymbol:
    # Буква - это неизвестное, умноженное на коэффициент и сложенное с дополнительным числом.

    def __init__(self, symbol="x"):
        self.k = 1
        self.y = 0
        self.symbol = symbol

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
        if isinstance(other, SuperSymbol):
            # Нельзя складывать / вычитать разнотипные буквы
            if type(self) != type(other):
                raise TypeError("Cannot add or subtract '%s' with '%s'" % (type(self), type(other)))
            elif isinstance(self, Symbol) and isinstance(other, Symbol):
                if self.is_linear != other.is_linear:
                    raise TypeError("Cannot add or subtract 'linear' and 'fractional' symbols")
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
        if isinstance(other, SuperSymbol):
            raise TypeError("'equations' module does not support 'power equations'")
        a = copy(self)
        a.k *= other
        a.y *= other
        return a

    # Умножить число на букву
    def __rmul__(self, other):
        return self.__mul__(other)

    # Разделить букву на число
    def __truediv__(self, other):
        if isinstance(other, SuperSymbol):
            return AnyNumber()  # Неизвестные сократятся внутри дроби, останутся только числа
        a = copy(self)
        a.k = self.accurate_result(a.k, other)
        a.y = self.accurate_result(a.y, other)
        return a

    # Если дробь в ответе нельзя перевести в десятичную, то оставляем в виде обыконовенной
    @staticmethod
    def accurate_result(a, b):
        # Делим a на b (в виде дробей), если не получится перевести частное в десятичную дробь
        f = to_fraction(to_fraction(a) / to_fraction(b)).reduce()
        if f.is_translatable_to_decimal():
            return a / b
        return f.format_to_mixed_number()

    # Решить уравнение
    def get(self, z):
        if isinstance(z, SuperSymbol):  # Перенос слагаемого
            if z.symbol != self.symbol:  # В линейном или в дробном уравнении должно быть только одно неизветсное
                raise ValueError("Unexpected symbol: '%s'" % z.symbol)
            return ((self.k-z.k)*Symbol(self.symbol)).get(z.y-self.y)
        return "continue"  # Перенос слагаемого не потребовался, решить уравнение


# z = k*x+y
class LinearSymbol(SuperSymbol):

    def __str__(self):
        return "%s%s%s" % (self.k, self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)
        return self.accurate_result(z-self.y, self.k) if s_g == "continue" else s_g


# z = k/x+y
class FractionalSymbol(SuperSymbol):

    def __str__(self):
        return "%s/%s%s" % (self.k, self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)
        return self.accurate_result(self.k, z-self.y) if s_g == "continue" else s_g


# Уравнение, которое может менять свой вид
class Symbol(SuperSymbol):

    def __init__(self, symbol="x"):
        super().__init__(symbol=symbol)
        self.is_linear = True  # Является ли уравнение линейным?

    # Здесь определяется еще и знак между числом "k" и неизвестным
    def __str__(self):
        return "%s%s%s%s" % (self.k, "" if self.is_linear else "/", self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)
        if self.is_linear:
            return self.accurate_result(z-self.y, self.k) if s_g == "continue" else s_g  # Решение линейного уравнения
        return self.accurate_result(self.k, z-self.y) if s_g == "continue" else s_g  # Решение дробного уравнения

    # Деление числа на букву - вот как уравнение меняет вид
    def __rtruediv__(self, other):
        if isinstance(other, SuperSymbol):
            return AnyNumber()  # Неизвестные сократятся внутри дроби, останутся только числа

        f_other = to_fraction(other).format_to_improper_fraction()  # Другое число в неправильную дробь
        a = copy(self)
        a.is_linear = not a.is_linear  # Вид меняется на противоположный

        # Делим числитель другой дроби на произведение коэффициента буквы и знаменателя другой дроби
        # Затем так же, только произведение числа "k" и знаменателя другой дроби
        a.k = self.accurate_result(f_other.numerator, a.k * f_other.denominator)
        a.y = self.accurate_result(f_other.numerator, a.y * f_other.denominator) if a.y else 0  # Устраняем деление на 0
        return a

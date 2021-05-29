# -*- coding: utf-8 -*-

from copy import copy
from .fractions import Fraction

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


# Схемы уравнений и схемы решения
solvers = {
    "k*x+y=z": "(z-y)/k",
    "k*x-y=z": "(z+y)/k",
    "y+k*x=z": "(z-y)/k",
    "y-k*x=z": "(y-z)/k",

    "x*k+y=z": "(z-y)/k",
    "x*k-y=z": "(z+y)/k",
    "y+x*k=z": "(z-y)/k",
    "y-x*k=z": "(y-z)/k",

    "k/x+y=z": "k/(z-y)",
    "k/x-y=z": "k/(z+y)",
    "y+k/x=z": "k/(z-y)",
    "y-k/x=z": "k/(y-z)",

    "x/k+y=z": "k*(z-y)",
    "x/k-y=z": "k*(z+y)",
    "y+x/k=z": "k*(z-y)",
    "y-x/k=z": "k*(y-z)"
}


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
            raise ValueError("x - any number")
        else:
            a = copy(self)
            a.k /= other
            a.y /= other
            return a

    # Если дробь в ответе нельзя перевести в десятичную, то оставляем в видео обыконовенной
    @staticmethod
    def accurate_result(a, b):
        f = Fraction("%s/%s" % (a, b)).reduce()
        if not f.is_translatable_to_decimal() and (a % b):  # И если "a" не делится на "b"
            return f.format_to_mixed_number()
        return a / b

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


class Equation:

    def __init__(self, string):
        self.eq = string  # Само уравнение
        self.letter = list(set(self.eq).intersection("abcdefghijklmnopqrstuvwxyz"))[0]  # Буква в уравнении
        self.left = self.eq.split("=")[0]  # Левая часть уравнения
        self.right = self.eq.split("=")[1]  # Правая часть уравнения
        print(self.letter)

    def __str__(self):
        return self.eq

    def __repr__(self):
        return str(self.eq)


def solve(simplified, letter="x"):
    # В любом случае заменяем неизвестную букву на х для удобства
    _stripped = simplified.replace(letter, "x").split("=")
    stripped = []  # Уравнение, разделенное на знаки, буквы и числа
    letters_and_numbers = {}  # Соответствие букв числам
    eq_scheme = ""  # Шаблон уравнения

    # Поиск и разделение левой части уравнения на части с операцией сложения или вычитания
    if simplified.find("-") != -1:
        _stripped[0] = _stripped[0].split("-")
        _stripped[0].insert(1, "-")
    elif simplified.find("+") != -1:
        _stripped[0] = _stripped[0].split("+")
        _stripped[0].insert(1, "+")

    # Если в уравнении нет операции сложения или вычитания, то приписываем "+0" в конец левой части
    elif simplified.find("-") == -1 or simplified.find("+") == -1:
        _stripped[0] = [_stripped[0], "+", "0"]

    # Раскрываем вложенные списки
    for x in _stripped[0]:
        if type(x) is list:
            [stripped.append(v) for v in x]
        else:
            stripped.append(x)
    stripped.append(_stripped[1])

    # Получаем шаблон для решения уравнения
    for part in stripped[:-1]:
        _p = part
        # Замена коэффициента-числа коэффициентом-буквой
        if "*" in _p or "/" in _p:
            # Делить на части: x и коэффициент
            if "*" in _p:
                split = _p.split("*")
                sign = "*"  # Знак
            else:
                split = _p.split("/")
                sign = "/"

            # Ищем часть с коэффициентом
            if split[0] != "x":
                letters_and_numbers["k"] = split[0]
                split[0] = "k"
            if split[1] != "x":
                letters_and_numbers["k"] = split[1]
                split[1] = "k"

            split.insert(1, sign)
            _p = "".join(split)

        # Возможно сложение с числом или вычитание: тогда просто знак прикрепляем к схеме уравнения
        elif _p == "+" or _p == "-":
            pass

        # Иначе: число, не относящееся к коэффициенту, определяем как y
        else:
            letters_and_numbers["y"] = _p
            _p = "y"
        eq_scheme += _p

    eq_scheme += "=z"  # Заканчиваем схему уравнения
    letters_and_numbers["z"] = stripped[-1]
    solve_scheme = solvers[eq_scheme]  # Ищем схему решения уравнения
    solve_expr = solve_scheme.replace("k", letters_and_numbers["k"]).replace("y", letters_and_numbers["y"]). \
        replace("z", letters_and_numbers["z"])  # Заменяем букву числами

    return eval(solve_expr)  # Вычисляем выражение в строке

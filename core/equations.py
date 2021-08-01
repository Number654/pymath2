# -*- coding: utf-8 -*-

from copy import copy
from .fractions import to_fraction


def format_sign(x):
    return "-"+str(x).replace("-", "") if x < 0 else "+"+str(x).replace("+", "")


def get_sign(x):
    return "-" if x < 0 else "+"


class AnyNumber:

    def __str__(self):
        return "Any Number"

    def __repr__(self):
        return str(self.__str__())


# Суперкласс для двух типов уравнений: линейные и дробные
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

    # ==
    def __eq__(self, other):
        if not isinstance(other, SuperSymbol):
            return
        return self.k == other.k and self.y == other.y

    # !=
    def __ne__(self, other):
        return not self.__eq__(other)

    # Если дробь в ответе нельзя перевести в десятичную, то оставляем в виде обыконовенной
    @staticmethod
    def accurate_result(a, b):
        # Делим a на b (в виде дробей), если не получится перевести частное в десятичную дробь
        f = to_fraction(to_fraction(a) / to_fraction(b)).reduce()
        if f.is_translatable_to_decimal():
            return a / b
        return f.format_to_mixed_number()

    # Есть ли корни у уравнения
    # При данной правой части
    def can_solve(self, z):
        """ Если коэффициенты неизвестного левой и правой
        частей не равны, а независимые величины
        (числа "y") равны в левой и в правой частях,
        то уравнение не имеет решений. """
        return not (self.k != z.k and self.y == z.y)

    # Решить уравнение
    def get(self, z):
        if isinstance(z, SuperSymbol):  # Перенос слагаемого
            if z.symbol != self.symbol:  # В линейном или в дробном уравнении должно быть только одно неизветсное
                raise ValueError("Unexpected symbol: '%s'" % z.symbol)
            elif self == z:  # Если у уравнения бесконечное количество решений ("x" - любое число)
                return AnyNumber()
            elif not self.can_solve(z):  # Если у уравнения нет решений ("x" не равен правой части уравнения)
                return
            return ((self.k - z.k) * Symbol(self.symbol)).get(z.y - self.y)
        return "continue"  # Перенос слагаемого не потребовался, решить уравнение

    # Вычислить левую часть уравнения, подставив вместо неизвестного число "n"
    def post_symbol(self, n):
        pass


# z = k*x+y
class LinearSymbol(SuperSymbol):

    def __str__(self):
        return "%s%s%s" % (self.k, self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)
        return self.accurate_result(z-self.y, self.k) if s_g == "continue" else s_g

    def post_symbol(self, n):
        return self.k*n+self.y


# z = k/x+y
class FractionalSymbol(SuperSymbol):

    def __str__(self):
        return "%s/%s%s" % (self.k, self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)
        return self.accurate_result(self.k, z-self.y) if s_g == "continue" else s_g

    def post_symbol(self, n):
        return self.accurate_result(self.k, n)+self.y


# Уравнение, которое может менять свой вид
class Symbol(SuperSymbol):

    def __init__(self, symbol="x"):
        super().__init__(symbol=symbol)
        self.is_linear = True  # Является ли уравнение линейным?

    # Здесь определяется еще и знак между числом "k" и неизвестным
    def __str__(self):
        return "%s%s%s%s" % (self.k, "" if self.is_linear else "/", self.symbol, format_sign(self.y))

    def get(self, z):
        s_g = super().get(z)  # Получение сигнала "continue" или уже результата
        if self.is_linear:
            return self.accurate_result(z-self.y, self.k) if s_g == "continue" else s_g  # Решение линейного уравнения
        return self.accurate_result(self.k, z-self.y) if s_g == "continue" else s_g  # Решение дробного уравнения

    def post_symbol(self, n):
        if self.is_linear:
            return self.k*n+self.y
        return self.accurate_result(self.k, n)+self.y

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


# Суперкласс всех уравнений с двумя неизвестными
class SuperDoubleSymbol(Symbol):

    def __init__(self, sub=False, symbol1="x", symbol2="y"):
        super().__init__(symbol=symbol1)
        self.symbol2 = symbol2
        self.k2 = 1 if not sub else -1  # Если нужно вычесть второе неизвестное

    def __str__(self):
        return "%s%s%s%s%s%s%s" % (self.k, "" if self.is_linear else "/", self.symbol,
                                   format_sign(self.k2), "" if self.is_linear else "/", self.symbol2,
                                   format_sign(self.y))

    def __neg__(self):
        return SuperDoubleSymbol.from_symbol(super().__neg__(), -self.k2, symbol1=self.symbol,
                                             symbol2=self.symbol2)

    def __add__(self, other):
        if isinstance(other, SuperSymbol) and \
                not isinstance(other, DoubleSymbol):  # Для сложения с другими типами уравнений
            a = copy(self)
            if other.symbol not in (self.symbol, self.symbol2):
                raise ValueError("Invalid symbol: '%s'" % other.symbol)
            # Ищем букву другого уравнения, и складываем коэффициент этой буквы с коэффициентом
            # Такой же буквы в уравнении
            if a.symbol == other.symbol:
                a.k += other.k
            elif a.symbol2 == other.symbol:
                a.k2 += other.k
            return a

        a = SuperDoubleSymbol.from_symbol(super().__add__(other), self.k2, symbol1=self.symbol,
                                          symbol2=self.symbol2)
        a.is_linear = self.is_linear  # Указывем, линейное или дробное уравнение

        if isinstance(other, SuperSymbol):
            if isinstance(other, DoubleSymbol):
                a.k2 += other.k2  # Если складываем с другим "DoubleSymbol", то складываем и втроые коэффициенты

        if a.k == 0 or a.k2 == 0:  # Если один из коэффициентов равен 0, то неизвестное(-ые) взаимоуничтожатся
            raise ValueError("Zero coefficient, cannot solve equations system")
        return a

    def __mul__(self, other):
        a = SuperDoubleSymbol.from_symbol(super().__mul__(other), self.k2, symbol1=self.symbol,
                                          symbol2=self.symbol2)
        a.k2 *= other  # Просто умножаем еще и коэффициент второго неизвестного
        return a

    def __truediv__(self, other):
        if isinstance(other, SuperSymbol):
            raise ValueError("Cannot divide by other symbol: unknown values will mutually annihilate.")
        a = SuperDoubleSymbol.from_symbol(super().__truediv__(other), self.k2, symbol1=self.symbol,
                                          symbol2=self.symbol2)
        a.k2 = self.accurate_result(a.k2, other)  # Просто делим еще и коэффициент второго неизвестного
        return a

    def __rtruediv__(self, other):
        if isinstance(other, SuperSymbol):
            raise ValueError("Cannot divide by other symbol: unknown values will mutually annihilate.")

        f_other = to_fraction(other).format_to_improper_fraction()  # Пришлось снова переводить другое число в дробь
        a = SuperDoubleSymbol.from_symbol(super().__rtruediv__(other), self.k2, symbol1=self.symbol,
                                          symbol2=self.symbol2)
        a.k2 = self.accurate_result(f_other.numerator, a.k2 * f_other.denominator)  # Так же, как и с "k1"
        a.is_linear = not a.is_linear
        return a

    # ==
    def __eq__(self, other):
        raise TypeError("Equations (symbols with specified in __init__() 'z') can be equivalent, not equal")

    def get(self, z):  # Решить можно только с помощью системы уравнений
        raise TypeError("'DoubleSymbol' cannot be solved out of equations system")

    # Из уравнения с одним неизвестным в уравнение с двумя неизвестными
    @staticmethod
    def from_symbol(obj, self_k2, symbol1="x", symbol2="y"):
        a = SuperDoubleSymbol(symbol1=symbol1, symbol2=symbol2)
        a.k, a.y, a.k2 = obj.k, obj.y, self_k2  # Просто переносим данные
        # Т. к. это статический метод, аргумент "self_k2" предоставляет доступ к переменной self.k2
        return a


# Уравнение с двумя неизвестными, правая часть без неизвестных
class DoubleSymbol(SuperDoubleSymbol):

    def __init__(self, z, sub=False, symbol1="x", symbol2="y"):
        super().__init__(sub=sub, symbol1=symbol1, symbol2=symbol2)
        self.z = z  # Сразу получаем правую часть уравнения

    def __str__(self):
        return "%s%s%s%s%s%s%s=%s" % (self.k, "" if self.is_linear else "/", self.symbol,
                                      format_sign(self.k2), "" if self.is_linear else "/", self.symbol2,
                                      format_sign(self.y), self.z)

    def __neg__(self):
        return self._from_super(super().__neg__())

    def __add__(self, other):
        return self._from_super(super().__add__(other))

    def __mul__(self, other):
        return self._from_super(super().__mul__(other))

    def __truediv__(self, other):
        return self._from_super(super().__truediv__(other))

    def __rtruediv__(self, other):
        return self._from_super(super().__rtruediv__(other))

    # Выразить "x" (первое неизвестное) из этого уравнения в системе
    def express_x(self):
        if self.is_linear:
            return (self.z-self.y-self.k2*Symbol(self.symbol2)) / self.k
        return self.k / (self.z-self.y-self.k2*Symbol(self.symbol2))

    def _from_super(self, obj):
        # Добавить переменную экземпляра "self.z", которой нет в суперклассе
        # "equations.SuperDoubleSymbol", то есть перенести все данные этого экземпляра
        # И добавляем переменную "z".
        a = DoubleSymbol(self.z, symbol1=obj.symbol, symbol2=obj.symbol2)
        a.k, a.k2, a.y = obj.k, obj.k2, obj.y
        return a


# Уравнение с двумя неизвстными,
# В котором есть неизвестные и в правой части
# Правую часть не нужно указывать в конструкторе класса
class TwoSidedDoubleSymbol(SuperDoubleSymbol):

    def __init__(self, sub=False, symbol1="x", symbol2="y"):
        super().__init__(sub=sub, symbol1=symbol1, symbol2=symbol2)

    def __neg__(self):
        return TwoSidedDoubleSymbol._from_super(super().__neg__())

    def __add__(self, other):
        return TwoSidedDoubleSymbol._from_super(super().__add__(other))

    def __mul__(self, other):
        return TwoSidedDoubleSymbol._from_super(super().__mul__(other))

    def __truediv__(self, other):
        return TwoSidedDoubleSymbol._from_super(super().__truediv__(other))

    def __rtruediv__(self, other):
        return TwoSidedDoubleSymbol._from_super(super().__rtruediv__(other))

    # Перевести результат работы методов суперкласса в экземпляр
    # Класса TwoSidedDoubleSymbol
    @staticmethod
    def _from_super(obj):
        a = TwoSidedDoubleSymbol(symbol1=obj.symbol, symbol2=obj.symbol2)
        a.k, a.k2, a.y = obj.k, obj.k2, obj.y
        return a


# Система уравнений
class EqSystem:

    def __init__(self, eq1, eq2):
        self.eq1 = eq1  # Первое уравнение в системе
        self.eq2 = eq2  # Второе уравнение
        self.symbol = eq1.symbol
        self.symbol2 = eq1.symbol2

    def __str__(self):
        return " %s\n{\n %s" % (self.eq1, self.eq2)

    def __repr__(self):
        return str(self.__str__())

    def get(self):
        expressed_x = self.eq1.express_x()

        if self.eq1.is_linear:
            new_symbol = self.eq2.k*expressed_x+(self.eq2.k2*Symbol(self.symbol2)+self.eq2.y)
        else:
            new_symbol = self.eq2.k/expressed_x+(self.eq2.k2/Symbol(self.symbol2)+self.eq2.y)

        v1 = new_symbol.get(self.eq2.z)
        v2 = expressed_x.post_symbol(v1)
        return {self.symbol: v2, self.symbol2: v1}


class TransferEqSystem(EqSystem):

    """
       Система уравнений с возможностью переноса слагаемых.
       Получает два уравнения с двумя неизвестными,
       То есть их левую и правую части в кортежах.
    """

    def __init__(self, para1, para2):
        super().__init__(para1[0], para2[0])
        self.para1 = tuple(para1)  # Левая и правая части первого уравнения
        self.para2 = tuple(para2)  # Левая и правая часть второго уравнения

        # Для удобства, если первым в паре уравнений указано уравнение,
        # В котором одно неизвестное, такое уравнение перемещается в правую часть.
        if isinstance(self.para1[0], SuperSymbol) and \
                not isinstance(self.para1[0], SuperDoubleSymbol):
            self.para1 = tuple(reversed(self.para1))

        # То же касается и второго уравнения системы
        if isinstance(self.para2[0], SuperSymbol) and \
                not isinstance(self.para2[0], SuperDoubleSymbol):
            self.para2 = tuple(reversed(self.para2))

    def __str__(self):
        return " %s=%s\n{\n %s=%s" % (self.para1[0], self.para1[1],
                                      self.para2[0], self.para2[1])

    # Решить систему уравнений,
    # Перенеся неизвестные в левую часть
    def get(self):
        transferred_eq1 = DoubleSymbol(self.para1[1].y-self.para1[0].y,
                                       symbol1=self.symbol, symbol2=self.symbol2)
        transferred_eq2 = DoubleSymbol(self.para2[1].y-self.para2[0].y,
                                       symbol1=self.symbol, symbol2=self.symbol2)
        # Передаем коэффициенты уравнений в классы для переноса слагаемых
        transferred_eq1.k = self.para1[0].k
        transferred_eq1.k2 = self.para1[0].k2
        transferred_eq2.k = self.para2[0].k
        transferred_eq2.k2 = self.para2[0].k2

        # Если в первом уравнении в правой части только одно неизвестное
        if isinstance(self.para1[1], SuperSymbol) and \
                not isinstance(self.para1[1], SuperDoubleSymbol):
            # Если неизвестное в правой части совпадает с одним
            # Из неизвестных в левой части, то вычитаем соответствующие
            # Коэффициенты
            if self.para1[0].symbol == self.para1[1].symbol:
                # Первое неизвестное из левой части совпадает с неизвестным из правой части
                transferred_eq1.k -= self.para1[1].k
            elif self.para1[0].symbol2 == self.para1[1].symbol:
                # Второе неизвестное из левой части совпадает с неизвестным из правой части
                transferred_eq1.k2 -= self.para1[1].k
        # Если в первом уравнении в правой части два неизвестных
        else:
            # Вычитаем соответствующие коэффициенты
            transferred_eq1.k -= self.para1[1].k
            transferred_eq1.k2 -= self.para1[1].k2

        # Если во втором уравнении в правой части только одно неизвестное
        if isinstance(self.para2[1], SuperSymbol) and \
                not isinstance(self.para2[1], SuperDoubleSymbol):
            # Если неизвестное в правой части совпадает с одним
            # Из неизвестных в левой части, то вычитаем соответствующие
            # Коэффициенты
            if self.para2[0].symbol == self.para2[1].symbol:
                # Первое неизвестное из левой части совпадает с неизвестным из правой части
                transferred_eq2.k -= self.para2[1].k
            elif self.para2[0].symbol2 == self.para2[1].symbol:
                # Второе неизвестное из левой части совпадает с неизвестным из правой части
                transferred_eq2.k2 -= self.para2[1].k
        # Если во втором уравнении в правой части два неизвестных
        else:
            # Вычитаем соответствующие коэффициенты
            transferred_eq2.k -= self.para2[1].k
            transferred_eq2.k2 -= self.para2[1].k2

        return EqSystem(transferred_eq1, transferred_eq2).get()

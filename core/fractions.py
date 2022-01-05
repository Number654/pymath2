# -*- coding: utf-8

from abc import ABC
from numbers import Real as RealNumber
from .pymath import is_odd, gcd, lcm, prime_factorization, better_divmod, root, trunc


# Является ли сторка числом с плавающей точкой?
def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    else:
        return True


# Целое число в неправильную дробь: n/1
def int2fraction(integer):
    return Fraction('%s/1' % integer)


# Число с плавающей точкой в обыкновенную дробь
def float2ordinary(_float):
    string = repr(_float)
    splitted = string.split('.')
    integer_part = splitted[0]
    numerator = splitted[1]
    denominator = str(10 ** len(numerator))

    if not int(integer_part):
        return Fraction('%s/%s' % (numerator, denominator))
    else:
        return Fraction('%s&%s/%s' % (integer_part, numerator, denominator))


# Список строк, содержащих дроби в список самих дробей
def strings_list2fractions_list(my_list):
    new_list = []
    for m in my_list:
        # Если элемент m уже является экземпляром класса Fraction,
        # То просто добавляем его, не приводя
        if isinstance(m, Fraction):
            new_list.append(m)
        else:
            new_list.append(Fraction(m))

    return new_list


# Любой числовой объект в обыкновенную дробь
def to_fraction(__obj):
    if isinstance(__obj, Fraction):
        return __obj
    elif isinstance(__obj, int):
        return int2fraction(__obj)
    elif isinstance(__obj, float):
        return float2ordinary(__obj)


# Проверить список по маске: найти в списке элементы, отличные от тех, что указаны в маске
# Если такой элемент (или элементы) найден, то цикл прерывается, возвращается False
def check_list(_list, mask):
    for val in _list:
        if val not in mask:
            return False
    return True


# Приведение нескольких дробей к общему знаменателю
def reduce_to_common_denominator(my_fractions):
    # Переводим список дробей в список экземпляров класса Fraction
    fractions = strings_list2fractions_list(my_fractions)

    # Числители и знаменатели
    numerators = []
    denominators = []
    # Дополнительные множители дробей
    additional_factors = []
    # Приведенные к общему знаменателю дроби (числитель*доп.множ./НОК знам-телей)
    formatted_fractions = []
    # Если это смешанные числа, делаем из них неправильные дроби
    for fraction in fractions:
        fraction1 = fraction.format_to_improper_fraction()
        fraction1 = fraction1.reduce()  # Сокращаем дроби
        # Числители и знаменатели отформатированных выше дробей
        numerators.append(fraction1.numerator)
        denominators.append(fraction1.denominator)
    # НОК знаменателей
    denominators_lcm = int(lcm(*denominators))
    # Находим доп. множители и добавляем их в additional_factors
    for den in denominators:
        additional_factors.append(int(denominators_lcm / den))
    # Приводим дроби к общ. знам-телю и добавляем в formatted_fractions
    for add_factor, numerator in zip(additional_factors, numerators):
        formatted_fractions.append(Fraction('%s/%s' % (str(int(add_factor * numerator)),
                                                       str(int(denominators_lcm)))))

    return formatted_fractions


# Сортировка дробей
def sort_fractions(my_fractions, reverse=False):
    # Переводим список дробей в список экземпляров класса Fraction
    fractions = strings_list2fractions_list(my_fractions)

    # Приводим дроби к общему знаменателю
    reduced_fractions = reduce_to_common_denominator(fractions)
    # Числители приведенных дробей
    numerators = []
    # Отсортированные дроби
    sorted_fractions = []
    # Словарь, чтобы найти оригинал дроби по ее приведенному к общему знам-телю-двойнику
    to_sort = {}
    # Словарь, чтобы найти приведенную дробь по ее числителю
    find_fraction_by_numerator = {}

    # Добавляем элементы в словарь to_sort: ключ - приведенная дробь, значение - оригинал этой дроби
    for fraction, reduced in zip(fractions, reduced_fractions):
        to_sort[reduced] = fraction

    # Добавляем элементы в список числителей приведенных дробей
    # И в словарь find_fraction_by_numerator: ключ - числитель приведенной дроби, значение - приведенная дробь
    for fraction in reduced_fractions:
        n = fraction.numerator
        numerators.append(n)
        find_fraction_by_numerator[n] = fraction
    # Главная функция - сортировка числителей приведенных дробей
    numerators.sort(reverse=reverse)
    # Добавляем в sorted_fractions оригиналы приведенных дробей, найденные по знаменателям приведенных дробей
    for numerator in numerators:
        sorted_fractions.append(to_sort[find_fraction_by_numerator[numerator]])

    return sorted_fractions


# Решить выражение с дробями
def solve_fraction_expr(expr):
    if not isinstance(expr, str):
        raise TypeError("solve() support only str expressions")
    if expr.lower() == "dubstep is good":
        print("Of course! :D")
        print("https://www.youtube.com/channel/UCTqiMIC99QK2l4EibKUlp-g")
        return ""

    # Разделяем выражение на дроби и знаки арифметических действий
    fractions_and_operands = expr.split(" ")
    expression = ""  # Здесь будет составленное выражение для вычисления

    for something in fractions_and_operands:
        if something in ["+", "-", "*", "/", "//", "**", "%"]:
            expression += something

        # Дроби и скобки
        else:
            # Открывающая скобка
            if something[0] == "(":
                # В дробь попадает все, что идет после откр. скобки
                expression += "(Fraction('%s')" % something.split("(")[1]
            # Закрывающая скобка
            elif something[-1] == ")":
                # В дробь попадает все, что идет до закр. скобки
                expression += "Fraction('%s'))" % something.split(")")[0]
            # Просто дробь
            else:
                expression += "Fraction('%s')" % something

    return eval(expression)  # Возвращаем вычисленное выражение


# Тип данных: дробь
class Fraction(RealNumber, ABC):

    # Передаем в конструктор строку вида m/n
    def __init__(self, fraction):
        if isinstance(fraction, float):
            self.fraction = float2ordinary(fraction).fraction
        elif isinstance(fraction, int):
            self.fraction = int2fraction(fraction).fraction
        else:
            if fraction.isdigit():
                self.fraction = int2fraction(int(fraction)).fraction
            if isfloat(fraction):
                self.fraction = float2ordinary(float(fraction)).fraction
            else:
                self.fraction = str(fraction)

        int_and_fr = self.fraction.split("&")  # Целая и дробная части
        num_and_den = int_and_fr[-1].split("/")  # Числитель и знаменатель
        self.integer_part = int_and_fr[0]  # Целая часть

        # Проверка на смешанное число
        # Если это смешанное число, то берем и целую часть
        if self.is_mixed_number():
            if self.integer_part == "-0":
                num_and_den = ["-"+num_and_den[0], num_and_den[1]]
            self.integer_part = int(self.integer_part)
        else:
            self.integer_part = 0

        # Числитель и знаменатель
        self.numerator = int(num_and_den[0])
        self.denominator = int(num_and_den[1])

        self.update_fraction()
        self.assign(self.format_sign())  # Упрощаем запись дроби со знаком

    # Когда пишем: print(fraction) - выводим на экран дробь
    def __str__(self):
        return self.fraction

    def __repr__(self):
        return str(self.__str__())

    # Изменить знак дроби на противоположный
    def __neg__(self):
        a = self.format_to_improper_fraction()
        a.numerator = -a.numerator
        a.update_fraction()  # Обновить дробь
        return a

    # Унарный плюс (+x) - ничего не делает с числовым объектом
    def __pos__(self):
        return self

    # Функция сложения этой дроби с другой
    def __add__(self, other):
        # Выполняем необходимые преобразования
        formatted = self._arithmetic_formatting(other)

        # Складываем преобразованные дроби
        result = Fraction('%s/%s' % (formatted[0].numerator + formatted[1].numerator,
                                     formatted[0].denominator))
        # Если надо - сокращаем и переводим в смешанное число
        result = result.reduce()
        result = result.format_to_mixed_number()

        return result

    # Сложение с присваиванием (изменением числителя и знаменателя)
    def __iadd__(self, other):
        a = self.__add__(other)
        self.assign(a)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    # Вычитание
    def __sub__(self, other):
        return self.__add__(-other)

    # Вычитание с присваиванием (тоже, что и со сложением, только наоборот)
    def __isub__(self, other):
        s = self.__sub__(other)
        self.assign(s)
        return self

    # Вычитание из другого числа дробь
    def __rsub__(self, other):
        return (-self).__add__(other)

    # Умножение
    def __mul__(self, other):
        # Если не получается умножить дробь на другое число, пытаемся сделать наоборот
        if to_fraction(other) is None:
            return other.__rmul__(self)

        # Приводим другое число в обыкновенную дробь
        other = to_fraction(other)

        self_m = self.format_to_improper_fraction()
        other_m = other.format_to_improper_fraction()

        result = Fraction('%s/%s' % (self_m.numerator * other_m.numerator,
                                     self_m.denominator * other_m.denominator))
        # Если надо - сокращаем и переводим в смешанное число
        result = result.reduce()
        result = result.format_to_mixed_number()

        return result

    # Умножение с присваиванием
    def __imul__(self, other):
        m = self.__mul__(other)
        self.assign(m)
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    # Деление
    def __truediv__(self, other):
        if to_fraction(other) is None:  # Если не получается разделить дробь на другое число, делаем наоборот
            return other.__rtruediv__(self)
        return self.__mul__(to_fraction(other).reverse())

    # Деление с присваиванием
    def __itruediv__(self, other):
        m = self.__truediv__(other)
        self.assign(m)
        return self

    # Деление на дробь
    def __rtruediv__(self, other):
        return to_fraction(other).__mul__(self.reverse())

    # Целочисленное деление
    def __floordiv__(self, other):
        return to_fraction(trunc(self / other))

    # Целочисленнное деление с присваиваением
    def __ifloordiv__(self, other):
        m = self.__floordiv__(other)
        self.assign(m)
        return self

    # Целочисленное деление на дробь
    def __rfloordiv__(self, other):
        return to_fraction(trunc(other / self))

    # Возведение в степень
    # Чтобы возвести дробь в степень, нужно возвести в степень ее числитель и знаменатель
    def __pow__(self, power):
        if isinstance(power, Fraction) or isinstance(power, Double):
            raise TypeError("'Fraction' does not support fractional exponentiation")
        m = self.format_to_improper_fraction()
        mf = Fraction("%s/%s" % (pow(m.numerator, power), pow(m.denominator, power)))
        return mf.reduce().format_to_mixed_number()

    # Возведение в степень с присваиванием
    def __ipow__(self, power):
        m = self.__pow__(power)
        self.assign(m)
        return self

    # Возведение другого числа в дробную степень
    def __rpow__(self, power):
        a = self.format_to_improper_fraction()
        return root(pow(power, a.numerator), a.denominator)

    # Остаток от деления дроби на другое значение
    def __mod__(self, other):
        return to_fraction(abs(self - other*(self // other)))

    # Остаток от деления с присваиванием
    def __imod__(self, other):
        m = self.__mod__(other)
        self.assign(m)
        return self

    # Остаток от деления другого значения на дробь
    def __rmod__(self, other):
        return to_fraction(abs(other - self*(other // self)))

    # Отсечение дробной части
    def __trunc__(self):
        return to_fraction(self.integer_part)

    # Модуль дроби
    def __abs__(self):
        return Fraction("%s%s/%s" % (str(abs(self.integer_part))+"&" if self.integer_part else "",
                                     abs(self.numerator), abs(self.denominator)))

    # ==
    def __eq__(self, other):
        return self.__compare(other, "==")

    # !=
    def __ne__(self, other):
        return not self.__eq__(other)

    # <
    def __lt__(self, other):
        return self.__compare(other, "<")

    # >
    def __gt__(self, other):
        return self.__compare(other, ">")

    # <=
    def __le__(self, other):
        return self.__compare(other, "<=")

    # >=
    def __ge__(self, other):
        return self.__compare(other, ">=")

    # Отсечь дробную часть и вернуть int
    def __int__(self):
        return self.integer_part

    # Перевести во float с потерей точности
    def __float__(self):
        _f = self.format_to_improper_fraction()
        return float(_f.numerator / _f.denominator)

    def __ceil__(self):
        if self < 0:
            return self.format_to_mixed_number().integer_part
        elif self == 0:
            return 0

        _f = self.format_to_mixed_number()
        if _f.numerator == 0:
            return _f.integer_part
        return _f.integer_part+1

    def __floor__(self):
        if self > 0:
            return self.format_to_mixed_number().integer_part
        elif self == 0:
            return 0

        _f = self.format_to_mixed_number()
        if _f.numerator == 0:
            return _f.integer_part
        return _f.integer_part-1

    # Округлить обыкновенную дробь
    def __round__(self, n=None):
        # Обыкновенные дроби так просто не округлить
        # Поэтому точность максимум до 15 знаков после запятой
        return round(float(self), n)

    # Общий алгоритм сравнения дробей, нужно лишь указать нужный операнд сравнения
    def __compare(self, other, cmp_sign):
        common = reduce_to_common_denominator([self, to_fraction(other)])  # Привести к общему знаменателю
        return eval("common[0].numerator %s common[1].numerator" % cmp_sign)

    # Метод проверки дроби на смешанное число
    def is_mixed_number(self):
        # Если при разбивки дроби на дробную часть и целую часть список будет содержать 1 элемент
        # (нет символа &, скрепляющего цел. и дробн. части), то это не смешанное число
        if len(self.fraction.split('&')) > 1:
            return True
        else:
            return False

    # Проверка дроби на неправильность
    def is_improper(self):
        # Если модуль числителя >= модулю знаменателя, то это неправильная дробь
        if abs(self.numerator) >= abs(self.denominator):
            return True
        else:
            return False

    # Проверка дроби на "типичность" (если она не смешанное число и не неправильная дробь)
    def is_typical(self):
        if not self.is_mixed_number() and not self.is_improper():
            return True
        else:
            return False

    # Проверка дроби на сократимость
    def is_contract(self):
        # Если числитель и знаменатель дроби взаимно простые, то это несократимая дробь
        if gcd(self.numerator, self.denominator) == 1:
            return False
        else:
            return True

    # Метод переведения дроби из смешанного числа в неправильную дробь
    def format_to_improper_fraction(self):
        # Числитель неправильной дроби: знаменатель * цел.ч + числитель (смешанного числа)
        # Возвращает новый экземпляр класса Fraction
        if self.is_improper():
            return self
        if self.is_typical():
            return self

        if self.integer_part < 0:  # Если данная дробь является отрицательным смешанным числом,
            # То переводим модуль данной дроби, а затем делаем результат отрицательным
            fmt = abs(self)
            return Fraction('-%s/%s' % (fmt.denominator * fmt.integer_part + fmt.numerator, fmt.denominator))
        return Fraction("%s/%s" % (self.denominator * self.integer_part + self.numerator, self.denominator))

    # Переведение неправильной дроби в смешанное число
    def format_to_mixed_number(self):
        if self.is_mixed_number():
            return self
        if self.is_typical():
            return self
        # Иначе делим числитель на знаменатель - это целая часть, остаток от деления - числитель смеш. числа
        dvmd = better_divmod(self.numerator, self.denominator)
        if not dvmd[1]:
            return Fraction("%s&0/1" % dvmd[0])
        return Fraction('%s&%s/%s' % (dvmd[0], dvmd[1], self.denominator))

    # Сокращение дроби
    def reduce(self):
        if self.is_mixed_number():
            return self.format_to_improper_fraction().reduce()
        if not self.is_contract():
            return self

        # Сокращение проходит так: делим числитель и знаменатель дроби на НОД
        # Числителя и знаменателя
        nd_gcd = gcd(self.numerator, self.denominator)
        if self.is_mixed_number():
            return Fraction('%s&%s/%s' % (int(self.integer_part), int(self.numerator / nd_gcd),
                                          int(self.denominator / nd_gcd)))
        else:
            return Fraction('%s/%s' % (int(self.numerator / nd_gcd), int(self.denominator / nd_gcd)))

    # Метод создания дроби, обратной данной (меняем местами числитель и знаменатель)
    def reverse(self):
        if self.is_mixed_number():
            m = self.format_to_improper_fraction().reverse()
            return Fraction("%s/%s" % (m.numerator, m.denominator))
        else:
            return Fraction('%s/%s' % (self.denominator, self.numerator))

    # Приведение обыкновенной дроби к десятичному знаменателю
    def to_decimal(self):
        if not self.is_translatable_to_decimal():
            raise ValueError("Cannot translate this fraction to decimal")
        fmt = abs(self).format_to_improper_fraction()  # Убираем минус у переводимой дроби для удобства
        den = 10
        while den % self.denominator:
            den *= 10
        if self < 0:  # Возвращаем минус, если переводимая дробь была отриуательной
            return Fraction("%s/%s" % (-fmt.numerator * (den // fmt.denominator), den))
        return Fraction("%s/%s" % (fmt.numerator * (den // fmt.denominator), den))

    # Проверка дроби на переводимость в конечную десятичную
    def is_translatable_to_decimal(self):
        if self.is_contract():
            self.reduce()
        mask = [2, 5]
        # Если знаменатель дроби при разложении на простые множители содержит ТОЛЬКО 2 и 5,
        # То эта дробь переводима. Если НЕ только 2 и 5, то непереводима.
        simple_multiples = prime_factorization(self.denominator)[0].values()
        if self.denominator == 5 or self.denominator == 2:
            return True
        if not check_list(simple_multiples, mask):
            return False
        else:
            return True

    # Упростить знак дроби
    # Например, если у дроби и числитель, и знаменатель имеют минусы, то дробь будет
    # Положительной.
    def format_sign(self):
        if not self.is_mixed_number():
            if self.numerator < 0 and self.denominator < 0:
                return Fraction("%s/%s" % (abs(self.numerator), abs(self.denominator)))
            elif self.denominator < 0:
                return Fraction("%s/%s" % (-self.numerator, abs(self.denominator)))
            return self

        # Знак у смешанного числа должен быть указан ТОЛЬКО перед дробной частью
        elif self.is_mixed_number() and (self.numerator < 0 or self.denominator < 0):
            raise ValueError("Invalid fraction: '%s'. Sign must be defined before integer part" % self.fraction)
        return self

    # Метод для перевода этой и другой дробей в неправильные дроби
    # Этот метод необходим для выполнения арифметических действий с дробями (+, -)
    # Для умножения и деления дробей этот метод не нужен
    def _arithmetic_formatting(self, other):
        other = to_fraction(other)

        # Переводим, если дроби - смешанные числа, в неправильные дроби
        this_fraction = self.format_to_improper_fraction()
        other_fraction = other.format_to_improper_fraction()

        # Если у дробей разные знаменатели, то приводим их к общему знаменателю
        if this_fraction.denominator != other_fraction.denominator:
            this_fraction, other_fraction = reduce_to_common_denominator([this_fraction, other_fraction])

        return this_fraction, other_fraction

    # Присваивание этой дроби значений от другой дроби
    # Нужна для арифметических действий с присваиванием.
    # Например: self.__iadd__() - сложение с присваиванием
    def assign(self, m):
        _m = to_fraction(m)

        self.numerator = _m.numerator
        self.denominator = _m.denominator
        self.integer_part = _m.integer_part
        self.update_fraction()

    # Обновить строку с дробью
    # Полезно, когда проводятся операции с присваиванием
    def update_fraction(self):
        self.fraction = "%s%s/%s" % (str(self.integer_part)+"&" if self.integer_part else "",
                                     self.numerator, self.denominator)


class LiteralFraction:

    def __init__(self, body):
        self.numerator = body[0]
        self.denominator = body[1]

    def __str__(self):
        return "(%s, %s)" % (self.numerator, self.denominator)

    def __repr__(self):
        return str("(%s, %s)" % (self.numerator, self.denominator))

    def append_to_numerator(self, string):
        self.numerator += string

    def append_to_denominator(self, string):
        self.denominator += string


# Числа с плавающей точкой неограниченной точности
class Double(RealNumber, ABC):

    def __init__(self, double):
        # Передаем только строки.
        # Если передадаим float, то дробь округлится.
        if not isinstance(double, str):
            raise ValueError("'Double' class supports only 'str' values")

        self.int_part = double.split(".")[0]  # Целая часть
        self.fraction_part = double.split(".")[1]  # Дробная часть

        if self.int_part == "":
            self.int_part = "0"
        if self.int_part == "-":
            self.int_part = "-0"

        if self.fraction_part == "":
            self.fraction_part = "0"

        while self.fraction_part[-1] == "0" and self.fraction_part != "0":  # Убираем лишние нули в конце дробной части
            self.fraction_part = self.fraction_part.removesuffix("0")
        self.double = self.int_part+"."+self.fraction_part  # Формируем строку с десятичной дробью
        self.format_sign()  # Упрощаем знак десятичной дроби

    def __str__(self):
        return self.double

    def __repr__(self):
        return str(self.__str__())

    # Поменять знак числа
    def __neg__(self):
        return Double("-"+self.double) if self.double[0] != "-" else Double(self.double[1:])

    def __pos__(self):
        return self

    # Сложение
    # Просто переводим тип Fraction в тип Double
    def __add__(self, other):
        if not isinstance(other, Double):
            return self.__add__(Double.from_fraction(other))

        fr1 = self.fraction_part  # Дробная часть этой десятичной дроби
        fr2 = other.fraction_part  # Дробная часть другой десятичной дроби
        fr1_len = len(fr1)
        fr2_len = len(fr2)

        if fr1_len < fr2_len:  # Если дробная часть этой дроби короче, чем у дрогой
            fr1 += "0" * (fr2_len-fr1_len)
        elif fr1_len > fr2_len:
            fr2 += "0" * (fr1_len-fr2_len)

        _sum = str(int(self.int_part+fr1) + int(other.int_part+fr2))
        result = Double("%s.%s" % (_sum[:len(_sum)-len(fr1)], _sum[len(_sum)-len(fr1):]))
        return result

    # Сложение с присваиванием
    def __iadd__(self, other):
        self.assign(self.__add__(other))
        return self

    def __radd__(self, other):
        return self.__add__(other)

    # Вычитание
    def __sub__(self, other):
        return self.__add__(-other)

    # Вычитание с присваиванием
    def __isub__(self, other):
        self.assign(self.__sub__(other))
        return self

    # Вычесть из другого числа Double
    def __rsub__(self, other):
        return -self.__add__(other)

    # Умножение
    def __mul__(self, other):
        if not isinstance(other, Double):
            return self.__mul__(Double.from_fraction(other))

        move_point = len(self.fraction_part) + len(other.fraction_part)  # На сколько знаков нужно двигать запятую
        _mul = str(int(self.double.replace(".", ""))*int(other.double.replace(".", "")))
        result = Double("%s.%s" % (_mul[:len(_mul)-move_point], _mul[len(_mul)-move_point:]))
        return result

    # Умножение с присваиванием
    def __imul__(self, other):
        self.assign(self.__mul__(other))
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    # Деление
    def __truediv__(self, other):
        if not isinstance(other, Double):
            return self.__truediv__(Double.from_fraction(other))

        # Переводим эту десятичную дробь и другоую в обыкновенные
        f1 = Fraction("%s&%s/%s" % (self.int_part, self.fraction_part, 10**len(self.fraction_part))).reduce()
        f2 = Fraction("%s&%s/%s" % (other.int_part, other.fraction_part, 10**len(other.fraction_part))).reduce()
        _div = (f1 / f2).reduce().format_to_mixed_number()  # И делим их, после переводим обратно в тип Double,
        # Если это возможно
        return _div if not _div.is_translatable_to_decimal() else Double.from_fraction(_div.to_decimal())

    # Деление с присваиванием
    def __itruediv__(self, other):
        self.assign(self.__truediv__(other))
        return self

    # Разделить другое число на Double
    def __rtruediv__(self, other):
        if not isinstance(other, Double):
            return self.__rtruediv__(Double.from_fraction(other))
        return other.__truediv__(self)

    # Целочисленное деление
    def __floordiv__(self, other):
        return Double.from_fraction(trunc(self / other))

    # Целочисленное деление с присваиванием
    def __ifloordiv__(self, other):
        self.assign(self.__floordiv__(other))
        return self

    # Целочисленное деление на тип Double
    def __rfloordiv__(self, other):
        return Double.from_fraction(trunc(other / self))

    def __trunc__(self):
        return Double("%s.0" % self.int_part)

    # Возведение в степень
    def __pow__(self, power):
        if isinstance(power, Fraction) or isinstance(power, Double):
            raise TypeError("'Double' does not support fractional exponentiation")

        # Переводим эту десятичную дробь в обыкновенную
        f = Fraction("%s&%s/%s" % (self.int_part, self.fraction_part, 10**len(self.fraction_part))).reduce()
        _pow = pow(f, power)
        return _pow if not _pow.is_translatable_to_decimal() else Double.from_fraction(_pow.to_decimal())

    # Возведение в степень с присваиванием
    def __ipow__(self, power):
        self.assign(self.__pow__(power))
        return self

    # Возведение в степень с показателем Double (с потерей точности в пок-теле)
    def __rpow__(self, other):
        return pow(other, float(self))

    # Остаток от деления
    def __mod__(self, other):
        return Double.from_fraction(abs(self - other*(self // other)))

    # Остаток от деления с присваиванием
    def __imod__(self, other):
        self.assign(self.__mod__(other))
        return self

    # Остаток от деления на Double
    def __rmod__(self, other):
        return Double.from_fraction(abs(other - self*(other // self)))

    # Модуль Double
    def __abs__(self):
        return Double(self.double.replace("-", ""))

    # ==
    def __eq__(self, other):
        return self.__compare(other) == 0

    # !=
    def __ne__(self, other):
        return self.__compare(other) != 0

    # <
    def __lt__(self, other):
        return self.__compare(other) < 0

    # >
    def __gt__(self, other):
        return self.__compare(other) > 0

    # <=
    def __le__(self, other):
        return self.__compare(other) <= 0

    # >=
    def __ge__(self, other):
        return self.__compare(other) >= 0

    def __ceil__(self):
        if self < 0:
            return int(self.int_part)
        elif self == 0:
            return 0
        if int(self.fraction_part) == 0:
            return int(self.int_part)
        return int(self.int_part)+1

    def __floor__(self):
        if self > 0:
            return self.int_part
        elif self == 0:
            return 0
        if int(self.fraction_part) == 0:
            return int(self.int_part)
        return int(self.int_part)-1

    def __round__(self, n=0):
        return self.round(accuracy=n)

    # Вычитаем из этой дроби другую
    # Потом сравниваем результат с нулем - это используется
    # Во всех методах, относящихся к операндам сравнения
    def __compare(self, other):
        return float(self - other)

    # Отсечь дробную часть и вернуть int
    def __int__(self):
        return self.int_part

    # Перевести Double в тип float (возможна потеря точности)
    def __float__(self):
        return float(self.double)

    # Перевести тип Fraction в тип Double
    @staticmethod
    def from_fraction(f):
        if isinstance(f, Double):
            return f
        elif isinstance(f, int):
            return Double("%s.0" % f)
        elif isinstance(f, float):
            return Double(str(f))
        elif type(f) not in (Double, Fraction, int, float):  # Нет возможности перевести этот тип
            raise TypeError("Cannot convert '%s' to 'Double'" % type(f))

        f = f.to_decimal().format_to_mixed_number()
        if f.integer_part:
            integer_part = f.integer_part
        else:
            if f < 0:  # Если дробь, которую следует перевести в Double является отрицательной без целой части
                integer_part = "-0"
                f.numerator = abs(f.numerator)  # Чтобы минус из числителя не стоял после точки в десятичной дроби
            else:
                integer_part = "0"

        # Тут подставляем число нулей после запятой до числителя, равное разности длины знаменателя, 1 и длины
        # Числителя
        return Double("%s.%s" % (integer_part, "0" *
                                 (len(str(f.denominator))-1 - len(str(f.numerator))) +
                                 str(f.numerator)))

    # Упростить знак Double
    # Если в конструктор передана десятичная дробь с четным количеством минусов,
    # То дробь будет положительной, иначе - отрицательной
    def format_sign(self):
        if not is_odd(self.double.count("-")):
            self.double = self.double.replace("-", "")
        else:
            self.double = "-"+(self.double.replace("-", ""))

    def to_decimal(self):
        return self

    # Округление дроби
    def round(self, accuracy=0):
        if accuracy < 0:  # Алгоритм округления целой части
            if int(self.int_part[::-1][abs(accuracy)-1]) >= 5:
                return Double("%s.0" % (int(self.int_part[:accuracy]+"0"*abs(accuracy))+10**abs(accuracy)))
            return Double("%s.0" % (self.int_part[:accuracy]+"0"*abs(accuracy)))
        elif accuracy > 0:  # Алгоритм округления дробной части
            if int(self.fraction_part[accuracy]) >= 5:
                return Double(self.double[:len(self.int_part)+accuracy+1]) + \
                       Double("0.%s" % ("0"*(accuracy-1)+"1"))
            return Double(self.double[:len(self.int_part)+accuracy+1])
        elif accuracy == 0:  # Алгоритм округления до единиц
            if int(self.fraction_part[0]) >= 5:
                return Double("%s.0" % (int(self.int_part)+1))
            return Double("%s.0" % self.int_part)

    # Алгоритм присваивания
    def assign(self, m):
        self.__init__(Double.from_fraction(m).double)


# Периодическая дробь
class PeriodicFraction:

    def __init__(self, fraction):
        self.fraction = fraction
        self.int_part = fraction.split(".")[0]  # Целая часть
        self.before_period = fraction.split(".")[1].split("(")[0]  # Цифры до периода
        self.period = fraction.split("(")[1].removesuffix(")")  # Цифры в периоде

    def __str__(self):
        return self.fraction

    def __repr__(self):
        return str(self.fraction)

    # Перевод в обыкновенную дробь
    def to_ordinary(self):
        k = len(self.period)
        b = int(self.before_period if not self.is_clean() else 0)
        m = len(self.before_period)
        a = int(self.before_period+self.period)

        return Fraction("%s&%s/%s" % (self.int_part, a-b, "9" * k + "0" * m)).reduce()

    # Если до периода не стоят цифры, то периодическая дробь называется чистой
    def is_clean(self):
        return not bool(self.before_period)

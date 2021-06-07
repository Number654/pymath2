# -*- coding: utf-8

from .pymath import gcd, lcm, prime_factorization, better_divmod, root, trunc


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


# Число с плавающей точкой в десятичную дробь
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
        # Если "что-то" имеет длину в 1 символ, то это знак действия
        if len(something) == 1:
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
            # Знак возведения в степень
            elif something == "**":
                expression += something
            # Просто дробь
            else:
                expression += "Fraction('%s')" % something

    return eval(expression)  # Возвращаем вычисленное выражение


# Тип данных: дробь
class Fraction:

    # Передаем в конструктор строку вида m/n
    def __init__(self, fraction):
        if isinstance(fraction, float):
            self.fraction = float2ordinary(fraction).fraction
        elif isinstance(fraction, int):
            self.fraction = int2fraction(fraction).fraction
        elif isinstance(fraction, Double):
            self.fraction = fraction.fraction  # Можно передать в конструктор экземпляр класса Double
        else:
            if fraction.isdigit():
                self.fraction = int2fraction(int(fraction)).fraction
            if isfloat(fraction):
                self.fraction = float2ordinary(float(fraction)).fraction
            else:
                self.fraction = str(fraction)

        # Проверка на смешанное число
        # Если это смешанное число, то берем и целую часть
        if self.is_mixed_number():
            self.integer_part = int(self.fraction.split('&')[0])
            # Числитель со знаменателем
            self.numerator = int(str(self.fraction.split('&')[1]).split('/')[0])
            self.denominator = int(str(self.fraction.split('&')[1]).split('/')[1])
        else:
            # Числитель со знаменателем
            self.numerator = int(self.fraction.split('/')[0])
            self.denominator = int(self.fraction.split('/')[1])
            self.integer_part = 0

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
        return a.format_to_mixed_number()

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
        return trunc(self / other)

    # Целочисленнное деление с присваиваением
    def __ifloordiv__(self, other):
        m = self.__floordiv__(other)
        self.assign(m)
        return self

    # Целочисленное деление на дробь
    def __rfloordiv__(self, other):
        return trunc(other / self)

    # Возведение в степень
    # Чтобы возвести дробь в степень, нужно возвести в степень ее числитель и знаменатель
    def __pow__(self, power):
        if isinstance(power, Fraction):
            raise TypeError("'Fraction' does not support fractional exponentiation")
        m = self.format_to_improper_fraction()
        mf = Fraction("%s/%s" % (m.numerator ** power, m.denominator ** power))
        return mf.format_to_mixed_number()

    # Возведение в степень с присваиванием
    def __ipow__(self, power):
        m = self.__pow__(power)
        self.assign(m)
        return self

    # Возведение другого числа в дробную степень
    def __rpow__(self, power):
        a = self.format_to_improper_fraction()
        return root(power**a.numerator, a.denominator)

    # Остаток от деления дроби на другое значение
    def __mod__(self, other):
        return (self / other) - (self // other)

    # Остаток от деления с присваиванием
    def __imod__(self, other):
        m = self.__mod__(other)
        self.assign(m)
        return self

    # Остаток от деления другого значения на дробь
    def __rmod__(self, other):
        return (other / self) - (other // self)

    # Отсечение дробной части
    def __trunc__(self):
        return self.integer_part

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
        if self.is_improper():
            return self
        if self.is_typical():
            return self
        # Числитель неправильной дроби: знаменатель * цел.ч + числитель (смешанного числа)
        # Возвращает новый экземпляр класса Fraction
        return Fraction('%s/%s' % (self.denominator * self.integer_part + self.numerator, self.denominator))

    # Переведение неправильной дроби в смешанное число
    def format_to_mixed_number(self):
        if self.is_mixed_number():
            return self
        if self.is_typical():
            return self
        # Иначе делим числитель на знаменатель - это целая часть, остаток от деления - числитель смеш. числа
        # Если остатка нет, то возвращаем тип int
        dvmd = better_divmod(self.numerator, self.denominator)
        if not dvmd[1]:
            return dvmd[0]
        else:
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

    # Привидение обыкновенной дроби к десятичному знаменателю
    def to_decimal(self):
        fmt = self.format_to_improper_fraction()
        den = 10
        while den % fmt.denominator != 0:
            den *= 10
        return Fraction("%s/%s" % (fmt.numerator * (int(den / fmt.denominator)), den))

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
class Double(Fraction):

    def __init__(self, double):
        # Передаем только строки.
        # Если передадаим float, то дробь округлится.
        if not isinstance(double, str):
            raise ValueError("'Double' class supports only 'str' values")

        self.double = double  # Десятичное представление
        x = double.split(".")

        # С целой частью
        if int(x[0]):
            super().__init__("%s&%s/%s" % (x[0], x[1], 10 ** len(x[1])))
        # Без целой части
        else:
            super().__init__("%s/%s" % (x[1], 10 ** len(x[1])))

    def __str__(self):
        # Дело в том, что из-за того, что данный класс основан на классе
        # Обыкновенных дробей, после выполнения арифметических действий в ответ "вылазит"
        # Обыкновенная дробь, которую нужно перевести в десятичный вид
        return Double.from_fraction(self).double

    def __repr__(self):
        return str(Double.from_fraction(self).double)

    # Поменять знак числа
    def __neg__(self):
        return Double.from_fraction(super(Double, self).__neg__())

    # Сложение
    # Просто переводим тип Fraction в тип Double
    def __add__(self, other):
        return Double.from_fraction(super(Double, self).__add__(other))

    # Сложение с присваиванием
    def __iadd__(self, other):
        self.assign(self.__add__(other))
        return self

    def __radd__(self, other):
        return self.__add__(other)

    # Вычитание
    def __sub__(self, other):
        return Double.from_fraction(super(Double, self).__sub__(other))

    # Вычитание с присваиванием
    def __isub__(self, other):
        self.assign(self.__sub__(other))
        return self

    # Вычесть из другого числа Double
    def __rsub__(self, other):
        return Double.from_fraction(super(Double, self).__rsub__(other))

    # Умножение
    def __mul__(self, other):
        return Double.from_fraction(super(Double, self).__mul__(other))

    # Умножение с присваиванием
    def __imul__(self, other):
        self.assign(self.__mul__(other))
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    # Деление
    def __truediv__(self, other):
        return Double.from_fraction(super(Double, self).__truediv__(other))

    # Деление с присваиванием
    def __itruediv__(self, other):
        self.assign(self.__truediv__(other))
        return self

    # Разделить другое число на Double
    def __rtruediv__(self, other):
        return Double.from_fraction(super(Double, self).__rtruediv__(other))

    # Возведение в степень
    def __pow__(self, power):
        return Double.from_fraction(super(Double, self).__pow__(power))

    # Возведение в степень с присваиванием
    def __ipow__(self, power):
        self.assign(self.__pow__(power))
        return self

    # Возвести число в степень типа Double
    def __rpow__(self, other):
        return Double.from_fraction(super(Double, self).__rpow__(other))

    # Остаток от деления
    def __mod__(self, other):
        return Double.from_fraction(super(Double, self).__mod__(other))

    # Остаток от деления с присваиванием
    def __imod__(self, other):
        self.assign(self.__mod__(other))
        return self

    # Остаток от деления на дробь Double
    def __rmod__(self, other):
        return Double.from_fraction(super(Double, self).__rmod__(other))

    # Модуль Double
    def __abs__(self):
        return Double.from_fraction(super(Double, self).__abs__())

    # Перевести тип Fraction в тип Double
    @staticmethod
    def from_fraction(f):
        if isinstance(f, Double):
            return f
        elif isinstance(f, int):
            return Double("%s.0" % f)
        elif isinstance(f, float):
            return Double(str(f))

        f = f.to_decimal()
        if f.integer_part:
            integer_part = f.integer_part
        else:
            integer_part = 0

        # Тут подставляем число нулей после запятой до числителя, равное разности длины знаменателя, 1 и длины
        # Числителя
        return Double("%s.%s" % (integer_part, "0" *
                                 (len(str(f.denominator))-1 - len(str(f.numerator))) +
                                 str(f.numerator)))

    def to_decimal(self):
        return self

    # Округление дроби
    def round(self, accuracy=1.0):
        decimal_fraction = self.double
        # Округление с точностью до единиц
        if accuracy == 1.0:
            intpart = int(str(decimal_fraction).split(".")[0])
            # Если первая цифра дробной части >= 5, то увеличиваем целую часть на 1
            if int(str(decimal_fraction).split(".")[1][0]) >= 5:
                intpart += 1
            # Возвращаем целую часть, дробную часть заменяем нулем
            return float(intpart)
        # Если округлять нужно не до единиц, то делаем следующее:
        else:
            # Получаем целую часть
            integer_part = str(decimal_fraction).split('.')[0]
            # Получаем дробную часть
            fraction_part = str(decimal_fraction).split('.')[1]
            # Получаем разряд, с точностью до которого нужно округлять
            digit = str(accuracy).split('.')[1]
            # И если цифра после этого разряда >= 5, то указываем, что цифра округляемого разряда
            # Должна быть увеличена на 1
            if int(fraction_part[len(digit)]) >= 5:
                add = Double(str(accuracy))
            # Иначе увеличиваем на 0.0
            else:
                add = Double("0.0")
            """
            Округлить 15.2531 с точностью до десятых.
             15.2531
            + 0.0100
            --------
             15.3"""
            # Увеличиваем!
            summa = self + add
            # Берем только цифры до округляемого разряда (вкл. сам разряд), так как все остальное - нули
            ost = str(summa).split('.')[1][:len(digit)]

            return Double('%s.' % integer_part + ost)

    # Алгоритм присваивания
    # Тут все как с обыкновенными дробями, только присваивается
    # Дополнительно десятичный вид: self.double
    def assign(self, m):
        super(Double, self).assign(m)
        self.double = m.double


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
        m = len(self.before_period)
        a = int(self.before_period+self.period)
        b = int(self.before_period) if self.is_clean() else 0  # Если дробь чиста, то ставим ноль до периода для вычисл.

        return Fraction("%s&%s/%s" % (self.int_part, a-b, "9" * k + "0" * m)).reduce()

    # Если до периода не стоят цифры, то периодическая дробь называется чистой
    def is_clean(self):
        return not bool(self.before_period)

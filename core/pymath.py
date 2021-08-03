# -*- coding: utf-8

from math import sqrt, atan, trunc, pi
from math import gcd as _gcd
from collections import Counter, OrderedDict

evens = [0, 2, 4, 6, 8]
odds = [1, 3, 5, 7, 9]
operators = ['+', '-', '*', '/']
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]


# Четное/нечетное
def is_odd(num):
    if bool(num % 2):
        return True
    else:
        return False


# Простое/составное
def is_simple(num):
    if num == 1 or num == 0:
        return
    # Если длина множества делителей > 2 (делители кроме 1 и самого себя),
    # То составное
    s = dividers(num)
    if len(s) == 2:
        return True
    return False


def is_positive(num):
    return num >= 0


def is_evil(num):
    if type(num) != float:
        if is_positive(num) and num != 0:
            return not is_odd(str(bin(num)).replace('0b', '').count('1'))
        else:
            return True
    else:
        return False


# Перемножить все числа (нужно для НОК двух чисел)
def multiply_all(_all):
    result = _all[0]
    new_all = list(_all)
    new_all.remove(new_all[0])
    for num in new_all:
        result *= num

    return result


# Кратные
# Так как кратные бесконечны, нужно указать их количество
def multiples(num, length=10):
    result = []
    thisnum = num
    for u in range(length):
        result.append(thisnum)
        thisnum += num

    return result


# Делители
def dividers(num):
    my_dividers = []
    y = 1
    while y <= sqrt(num):
        if num % y == 0:
            my_dividers.append(y)
            my_dividers.append(num / y)
        y += 1

    # Удаляем одинаковые делители (да, и такое бывает)
    my_dividers = set(my_dividers)
    # Потом превращаем множество в список (set() отличный способ избавиться от повторяющихся элемнетов)
    my_dividers = list(my_dividers)
    # Сортируем и возвращаем результат
    my_dividers.sort()
    return my_dividers


# НОК(a, b)=ab/НОД(a, b)
# НОК(a, b, c) = НОК(НОК(a, b), c)
def lcm(*args):
    if len(args) <= 2:
        m_gcd = gcd(*args)
        result = multiply_all(args) / m_gcd
        return result
    else:
        return lcm(lcm(*args[:-1]), args[-1])


# НОД
# НОД(a, b, c) = НОД(НОД(a, b), c)
def gcd(*args):
    if len(args) <= 2:
        return _gcd(int(args[0]), int(args[1]))
    else:
        return gcd(gcd(*args[:-1]), args[-1])


# Разложение на простые множители
def prime_factorization(num):
    # Если число уже простое, то просто возвращаем его
    if is_simple(num):
        return [OrderedDict({num: num}), Counter([num])]
        pass
    # Начальное число
    thisnum = num
    # Простые множители
    simple_multiples = []
    answer = OrderedDict()
    # Пока частное от деления последнего числа на последний простой множитель не будет равен 1 (пока не будет
    # завершено разложение числа на простые множители)
    while thisnum != 1:
        # Находим все делители числа thisnum
        _dividers = dividers(thisnum)
        # Выделяем из них простые множители
        simple_dividers = []
        for divider in _dividers:
            # Если делитель простое число, то добавляем его в простые делители
            if is_simple(divider):
                simple_dividers.append(divider)
            else:
                pass
        # Добавляем в ответ наибольший из простых делителей (множителей)
        answer[thisnum] = max(simple_dividers)
        # А число делим
        thisnum /= max(simple_dividers)

    # Считаем, сколько одинаковых простых множителей,
    # Чтобы потом записывать их в степени: 125 = 5*5*5 = 5^3
    count = Counter(simple_multiples)

    return answer, count


# Визуализация результата разложения на простые множители,
# Чтобы не было огромного непонятного для человека списка,
# А было как в тетрадке: справа - числа, слева - простые множители
"""
135|5
 27|3
  9|3
  3|3
  1|
135 = 3^3 * 5
"""


def visual_prime_factorization(prime_factorization_result):
    # Сюда сохраняется результат
    res = ""
    # Получаем числа и простые множителей
    source = prime_factorization_result[0]
    # Отступ (чтобы было как показано выше)
    indentation = len(str(source.keys()[0]))
    # Простые множители
    simple_multiples = []
    # Добавляем строчки к результату
    for key in source.keys():
        # Вычитаем из длины самого большого числа длину числа source[key], чтобы получить
        # Количество пробелов
        res += ' ' * (indentation - len(str(key))) + str(key) + '|' + str(source[key]) + '\n'
        # Добавляем каждый простой множитель в simple_multiples
        simple_multiples.append(source[key])
    # Сортируем простые множители
    simple_multiples.sort()
    # Добавляем единичку в конец
    res += ' ' * (indentation - 1) + '1|\n'
    # Делаем итоговую строку
    final_string = '%s = ' % source.keys()[0]
    for i in prime_factorization_result[1]:
        # Добавляем к итоговой строке множители
        # Записываем так: простой множитель^количество таких же * следующая запись
        final_string += str(i) + '^%s * ' % prime_factorization_result[1][i]
    # Убираем степени простых множителей в 1-ой степени, так как это мешает читать и совсем ненужно
    final_string.replace('^1', '')
    res += final_string

    return res


# Представление числа в виде: 3045=3*10^3+4*10+5
def tens_factorization(num):
    thisnum = list(str(num))
    result = ''
    while len(thisnum) != 1:
        if thisnum[0] == '0':
            pass
        else:
            result += thisnum[0] + ' * 10^' + str(len(thisnum[::1]) - 1) + ' + '
        thisnum.remove(thisnum[0])
    result = str(num) + ' = ' + result + thisnum[0]
    return result


# Выводит таблицу степеней в диапазоне натуральных чисел
def degree_table(degree, _range):
    _range = list(_range)
    result = 'a' + (' ' * (len(str(_range[1])) - 1)) + '|' + ' a^%s\n' % degree
    n = _range[0]
    while n <= _range[-1]:
        result += (' ' * (len(str(_range[1])) - len(str(n)))) + str(n) + '|' + ' %s' % n ** degree + '\n'
        n += 1
    return result


# Среднее арифметическое нескольких чисел
def average(nums):
    d = sum(nums)
    return d / len(nums)


# Корень n-ой степени
def root(x, n=2):
    # Подкоренное выражение возводим в дробную степень - 1/n
    return x ** (1.0 / n)


# Арккотангенс
def arcctg(x):
    return atan(-x) + pi/2


# Улучшенное деление с остатком (отсечение дробной части вместо округления)
def better_divmod(x, y):
    return trunc(x / y), abs(x - y * trunc(x / y))


# Среднее геометрическое
def geometric_mean(nums):
    length = len(nums)
    d = multiply_all(nums)
    return root(d, n=length)


# Центральное число (центральное число 3 - это 2)
# Четные числа не имеют центрального числа
def central_number(num):
    if not is_odd(num):
        raise Exception('Even numbers has not got a "central number"')
    div = num / 2 + 1
    return div

# -*- coding: utf-8 -*-


alphabet = 'IVXLCDM'
digits = {1: 'I', 10: 'X', 100: 'C', 1000: 'M'}
halves = {5: 'V', 50: 'L', 500: 'D'}

roman2arab_table = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}


def arab2roman(num):
    # Римские числа поддерживают перевод из арабских числел только в диапазоне от 1 до 3999 включительно
    if int(num) > 3999:
        raise OverflowError('Value is too large: %s > 3999' % num)
    if int(num) <= 0:
        raise ValueError('Roman numbers do not support numbers <= 0')

    result = ''
    # Число в строке, "перевернутая" последовательность от 0 до длины числа
    string_num = str(num)
    reversed_range = list(range(len(string_num))).__reversed__()
    # Разбиваем число на разряды
    for dig, number in zip(reversed_range, string_num):
        # Находим текущий разряд
        digit = 10 ** dig
        # Тут переводится числа текущего разряда по правилам римских чисел
        if number == '4':
            result += digits[digit] + halves[5 * digit]
        elif number == '9':
            result += digits[digit] + digits[digit * 10]
        elif 5 <= int(number) < 9:
            result += halves[5 * digit] + digits[digit] * (int(number)-5)
        else:
            result += digits[digit] * int(number)

    return result


def roman2arab(num):
    # Проверка на "правильность" римского числа
    if not num:
        raise ValueError
    for char in num:
        if char not in alphabet:
            raise ValueError('Invalid roman number: %s' % num)

    # Переменная с результатом
    result = 0
    # Проходимся по списку индексов римского числа
    for index in range(len(num) - 1):
        # Переводим текущее число
        converted = roman2arab_table[num[index]]
        # Переводим следующее число
        _next = roman2arab_table[num[index + 1]]
        # Если текущее число < следующего, то вычитаем из следующего числа текущее число
        if converted < _next:
            result -= converted
        # Если текущее число >= следующего, то складываем эти числа
        elif converted >= _next:
            result += converted

    # Прибавляем к переведенному числу последний знак римского числа
    # Это нужно сделать, потому что этот последний знак не учитывается после цикла
    result += roman2arab_table[num[len(num) - 1]]
    return result

# -*- coding: utf-8 -*-

from . import alphabet
from string import ascii_uppercase

latin_capital = alphabet.Alphabet(ascii_uppercase, 4)


# Заменить один элемент списка на другой
def replace(_list, value, new_value):
    n = _list
    value = value
    new_value = new_value
    value_index = n.index(value)
    n.remove(value)
    n.insert(value_index, new_value)


# Шифр Цезаря
class CaesarCipher:

    def __init__(self, data, _alphabet=latin_capital):
        self.data = data
        self.alphabet = _alphabet

    def __str__(self):
        return self.data

    def to_string(self):
        return self.data

    def encrypt(self, key):
        uppercase_data = self.data.upper()
        al = self.alphabet.get_array()
        encrypted = """"""

        for symbol in uppercase_data:
            if symbol in al:
                # Алфавит повторяем два раза, потому сдвиг может оказаться слишком большим,
                # И тогда возникнет исключение IndexError
                if key > 0:
                    encrypted += (self.alphabet.symbols_array * 2)[self.alphabet.index(symbol) + key]
                else:
                    encrypted += self.alphabet[self.alphabet.index(symbol) + key]
            else:
                encrypted += symbol

        return encrypted

    def decrypt(self, key=None):
        uppercase_data = self.data.upper()
        al = self.alphabet.get_array()
        decrypted = """"""

        # Дешифровка с ключом
        if key is not None:
            for symbol in uppercase_data:
                if symbol in al:
                    # Это чтобы не было IndexError
                    if self.alphabet.index(symbol) - key > 25:
                        decrypted += (self.alphabet.get_array() * 2)[self.alphabet.index(symbol) - key]
                    else:
                        decrypted += self.alphabet[self.alphabet.index(symbol) - key]

                else:
                    decrypted += symbol

            return decrypted

        # Дешифровка без ключа
        else:
            raw_text = ""  # Сюда бутут сохраняться все символы, использованные в зашифрованном тексте
            unique_symbols = ""
            # Сюда будут сохраняться среднее арифметическое для чисел встречаемости
            # Каждого символа в каждом слове зашифрованного текста
            average_frequency_of_symbols_in_words = {}

            # Убираем все посторонние символы из текста (включая символы \n)
            # Слова разделяем пробелами
            for sym in uppercase_data:
                if sym in al:
                    raw_text += sym
                else:
                    if sym == ' ' or sym == '\n':
                        raw_text += ' '

            # Находим все символы, использованные в зашифрованном тексте
            for sym in raw_text:
                if sym not in unique_symbols and sym != ' ':
                    unique_symbols += sym

            # Находим числа встречаемости для каждого символа в каждом слове текста
            for usym in unique_symbols:
                symbol_count = []

                for word in raw_text.split(' '):
                    symbol_count.append(word.count(usym))

                for x in symbol_count:
                    if x == 0:
                        symbol_count.remove(x)
                # Теперь находим среднее арифметическое для каждого из чисел встречаемости,
                # Принадлежащих определенному символу текста
                # И добавляем туда, куда нужно (см. выше)
                average_frequency_of_symbols_in_words[sum(symbol_count) / len(symbol_count)] = usym

            # Находим самую встречающийся символ в зашифрованном тексте
            # Но сначала - переводим все ключи словаря average_frequency_of_symbols_in_words
            # Обратно в числа - ведь они автоматически превратились в строки
            integer_keys = []
            for k in average_frequency_of_symbols_in_words.keys():
                integer_keys.append(float(k))
            most_used = average_frequency_of_symbols_in_words[max(integer_keys)]

            # Находим ключ!!!
            rotation = self.alphabet.index(most_used) - self.alphabet.most_used_symbol_index

            return CaesarCipher(self.decrypt(key=rotation).data, _alphabet=self.alphabet)


# Шифр Виженера
class VigenereCipher:

    def __init__(self, data, key, _alphabet=latin_capital):
        self.data = data.upper()
        self.alphabet = _alphabet

        self.key = key * (len(self.data) // len(key))  # Повторить ключ по длине данных
        self.key += key[:len(self.data) // len(key)]  # Если повторить нужно не целое количество раз,
        # то прибавляем остальные части ключа

        self.key = self.key.upper()

    def __str__(self):
        return self.data

    def to_string(self):
        return self.data

    def encrypt(self):
        encrypted = """"""
        al = self.alphabet.get_array()

        for key_sym, data_sym, in zip(self.key, self.data):
            if data_sym in al:
                # Шифруем с помощью шифра Цезаря, находя индекс букв повторенного ключа
                encrypted += CaesarCipher(data_sym, _alphabet=self.alphabet).encrypt(self.alphabet.index(key_sym))
            else:
                encrypted += data_sym

        return encrypted

    def decrypt(self):
        decrypted = """"""
        al = self.alphabet.get_array()

        for key_sym, data_sym in zip(self.key, self.data):
            if data_sym in al:
                # Расшифровываем шифром Цезаря по индексу букв ключа
                decrypted += CaesarCipher(data_sym, _alphabet=self.alphabet).decrypt(key=self.alphabet.index(key_sym))
            else:
                decrypted += data_sym

        return decrypted


# Шифр Атбаш
class AtbashCipher:

    def __init__(self, data, _alphabet=latin_capital):
        self.data = data
        self.alphabet = _alphabet
        self.alphabet_reversed = _alphabet.get_reversed()

    def to_string(self):
        return self.data

    def encrypt(self):
        encrypted = """"""
        al = self.alphabet.get_array()

        for symbol in self.data.upper():
            if symbol in al:
                encrypted += self.alphabet_reversed[self.alphabet.index(symbol)]
            else:
                encrypted += symbol

        return encrypted

    def decrypt(self):
        decrypted = """"""
        al = self.alphabet.get_array()

        for symbol in self.data.upper():
            if symbol in al:
                decrypted += self.alphabet[self.alphabet_reversed.index(symbol)]
            else:
                decrypted += symbol

        return decrypted


# Шифр машины "Энигма"
# Обрати внимание: сделано в Германии!
class EnigmaCipher:

    def __init__(self, data, rotor1="A", rotor2="B", rotor3="C"):
        self.data = data.upper()

        self.rotor1 = latin_capital.index(rotor1.upper())
        self.rotor2 = latin_capital.index(rotor2.upper())
        self.rotor3 = latin_capital.index(rotor3.upper())

        self.rotor1_combinations = [
            ["E", "A"],
            ["K", "B"],
            ["M", "C"],
            ["F", "D"],
            ["L", "E"],
            ["G", "F"],
            ["D", "G"],
            ["Q", "H"],
            ["V", "I"],
            ["Z", "J"],
            ["N", "K"],
            ["T", "L"],
            ["O", "M"],
            ["W", "N"],
            ["Y", "O"],
            ["H", "P"],
            ["X", "Q"],
            ["U", "R"],
            ["S", "S"],
            ["P", "T"],
            ["A", "U"],
            ["I", "V"],
            ["B", "W"],
            ["R", "X"],
            ["C", "Y"],
            ["J", "Z"]
        ]
        self.rotor2_combinations = [
            ["A", "A"],
            ["J", "B"],
            ["D", "C"],
            ["K", "D"],
            ["S", "E"],
            ["I", "F"],
            ["R", "G"],
            ["U", "H"],
            ["X", "I"],
            ["B", "J"],
            ["L", "K"],
            ["H", "L"],
            ["W", "M"],
            ["T", "N"],
            ["M", "O"],
            ["C", "P"],
            ["Q", "Q"],
            ["G", "R"],
            ["Z", "S"],
            ["N", "T"],
            ["P", "U"],
            ["Y", "V"],
            ["F", "W"],
            ["V", "X"],
            ["O", "Y"],
            ["E", "Z"]
        ]
        self.rotor3_combinations = [
            ["B", "A"],
            ["D", "B"],
            ["F", "C"],
            ["H", "D"],
            ["J", "E"],
            ["L", "F"],
            ["C", "G"],
            ["P", "H"],
            ["R", "I"],
            ["T", "J"],
            ["X", "K"],
            ["V", "L"],
            ["Z", "M"],
            ["N", "N"],
            ["Y", "O"],
            ["E", "P"],
            ["I", "Q"],
            ["W", "R"],
            ["G", "S"],
            ["A", "T"],
            ["K", "U"],
            ["M", "V"],
            ["U", "W"],
            ["S", "X"],
            ["Q", "Y"],
            ["O", "Z"]
        ]
        self.reflector_combinations = [
            ["Y", "A"],
            ["R", "B"],
            ["U", "C"],
            ["H", "D"],
            ["Q", "E"],
            ["S", "F"],
            ["L", "G"],
            ["D", "H"],
            ["P", "I"],
            ["X", "J"],
            ["N", "K"],
            ["G", "L"],
            ["O", "M"],
            ["K", "N"],
            ["M", "O"],
            ["I", "P"],
            ["E", "Q"],
            ["B", "R"],
            ["F", "S"],
            ["Z", "T"],
            ["C", "U"],
            ["W", "V"],
            ["V", "W"],
            ["J", "X"],
            ["A", "Y"],
            ["T", "Z"]
        ]

    def encrypt_decrypt(self):
        encrypted = """"""

        for symbol in self.data:
            if symbol in latin_capital.get_array():

                from_rotor1 = ""  # Данные с первого ротора
                from_rotor2 = ""  # Данные со второго ротора
                from_rotor3 = ""  # Данные с третьего ротора

                from_reflector = ""  # Данные с рефлектора
                from_rotor3_after_reflector = ""  # Данные с третьего ротора после рефлектора
                from_rotor2_after_reflector = ""  # Данные со второго ротора после рефлектора
                from_rotor1_after_reflector = ""  # Данные с первого ротора после рефлектора

                for para in self.rotor1_combinations:
                    if latin_capital.index(para[1]) == \
                            (latin_capital.index(symbol) + self.rotor1) % 26:
                        from_rotor1 = para[0]
                        break
                for para in self.rotor2_combinations:
                    if latin_capital.index(para[1]) == \
                            (latin_capital.index(from_rotor1) + (self.rotor2 - self.rotor1)) % 26:
                        from_rotor2 = para[0]
                        break
                for para in self.rotor3_combinations:
                    if latin_capital.index(para[1]) == \
                            (latin_capital.index(from_rotor2) + (self.rotor3 - self.rotor2)) % 26:
                        from_rotor3 = para[0]
                        break

                for para in self.reflector_combinations:
                    if latin_capital.index(para[1]) == \
                            (latin_capital.index(from_rotor3) - self.rotor3) % 26:
                        x = para[1]
                        for para1 in self.reflector_combinations:
                            if para1[0] == x:
                                from_reflector = para1[1]
                                break
                        del x
                        break
                for para in self.rotor3_combinations:
                    if latin_capital.index(para[0]) == \
                            (latin_capital.index(from_reflector) + self.rotor3) % 26:
                        from_rotor3_after_reflector = para[1]
                        break
                for para in self.rotor2_combinations:
                    if latin_capital.index(para[0]) == \
                            (latin_capital.index(from_rotor3_after_reflector) - (self.rotor3 - self.rotor2)) % 26:
                        from_rotor2_after_reflector = para[1]
                        break
                for para in self.rotor1_combinations:
                    if latin_capital.index(para[0]) == \
                            (latin_capital.index(from_rotor2_after_reflector) - (self.rotor2 - self.rotor1)) % 26:
                        from_rotor1_after_reflector = para[1]
                        break

                # Последний шаг шифровки символа
                encrypted += latin_capital[(latin_capital.index(from_rotor1_after_reflector) - self.rotor1) % 26]

                if self.rotor1 == 25:
                    self.rotor1 = 0  # Начинаем сначала
                    self.rotor2 += 1  # И поворачиваем средний ротор на один шаг
                else:
                    self.rotor1 += 1  # Поворачиваем правый ротор на один шаг

                if self.rotor2 == 25:
                    self.rotor2 = 0  # Начинаем сначала
                    self.rotor3 += 1  # И поворачиваем левый ротор на один шаг
                elif self.rotor2 < 25 and self.rotor1 == 0:
                    self.rotor2 += 1  # Поворачиваем средний ротор на один шаг

                if self.rotor3 == 25:
                    # Начинаем все сначала
                    self.rotor3 = 0
                    self.rotor2 = 0
                    self.rotor1 = 0
                elif self.rotor3 < 25 and self.rotor2 == 0 and self.rotor1 == 0:
                    self.rotor3 += 1  # Поворачиваем левый ротор на один шаг

            else:
                encrypted += symbol

        return encrypted

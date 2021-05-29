# -*- coding: utf-8 -*-


# Класс для создания алфавита, используемого для шифрования
class Alphabet:

    def __init__(self, symbols, most_used):
        self.symbols_array = [i.upper() for i in symbols]
        self.most_used_symbol_index = most_used
        self.length = len(self.symbols_array)

    # Получить символ из алфавита по индексу
    def __getitem__(self, item):
        return self.symbols_array[item]

    # Получить индекс символа
    def index(self, value):
        return self.symbols_array.index(value)

    # Получить массив символов алфавита
    def get_array(self):
        return self.symbols_array

    # Получить отраженную версию алфавита (используется в шифре Атбаш)
    def get_reversed(self):
        return Alphabet(self.symbols_array.__reversed__(), self.most_used_symbol_index)

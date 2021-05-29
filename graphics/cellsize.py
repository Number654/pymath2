# -*- coding: utf-8 -*-

from tkinter import Frame, Label, Toplevel, StringVar, GROOVE
from tkinter.ttk import Button, Entry


class CellSizeWidget:

    def __init__(self, master, width, height, cell_size=18.8787):
        self.master = master
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Главная рамка виджета
        self.frame = Frame(self.master, width=self.width, height=self.height, bd=2, relief=GROOVE)
        # Кнопка изменения размера клетки
        self.change_btn = Button(self.frame, text='Изменить', width=10, command=self.change_cell_size)
        self.size_label = Label(self.frame, text='Размер клетки:\n%s' % self.cell_size)

        self.change_btn.place(x=5, y=35)
        self.size_label.place(x=1, y=0)

    # Метод для размещения виджета на окне по координатам, указанным в __init__
    def place(self, x=0, y=0):
        self.x = x
        self.y = y
        self.frame.place(x=self.x, y=self.y)

    def get(self):
        return self.cell_size

    # Метод для изменения переменной self.cell_size и закрытия диалога изменения размера клетки
    def set(self, value, dlg):
        # Если пользователь НЕ ввел значение, то пропускаем следующие два шага
        # Если пользователь ввел значение, то выполняем следующее
        if value:
            self.cell_size = float(value.replace(',', '.'))
            self.size_label.config(text='Размер клетки:\n%s' % self.cell_size)
        dlg.destroy()

    # "сырая" установка значения размера клетки (без закрытия диалога)
    def raw_set(self, value):
        self.cell_size = value

    # Метод вызова диалога изменения размера клетки
    def change_cell_size(self):
        dialog = Toplevel(self.master)
        dialog.title('Размер клетки')
        # Уставнавливаем размер окна диалога и "делаем окно диалогом"
        dialog.geometry('142x62')
        dialog.resizable(0, 0)
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.focus_set()

        size_variable = StringVar()

        # Поле ввода размера клетки
        size_entry = Entry(dialog, width=10, font='Tahoma 9', textvariable=size_variable)
        size_entry.place(x=52, y=5)
        Label(dialog, text='Размер:').place(x=2, y=5)

        # Кнопки "ОК" и "Отмена"
        ok = Button(dialog, text='ОК', width=8, command=lambda: self.set(size_variable.get(), dialog))
        cancel = Button(dialog, text='Отмена', width=8, command=dialog.destroy)
        ok.place(x=22, y=37)
        cancel.place(x=81, y=37)

        # А вот тут мы не ставим "mainloop()", потому что в этом случае главное окно программы
        # Graphics прекратит отслеживание ВСЕХ событий окна

# -*- coding: utf-8 -*-

from tkinter import Frame, Listbox, Label
from tkinter.ttk import Button


class ShapeManager:

    """
    Класс, реализующий виджет для изменения
    уже нарисованных фигур на холсте.
    В список фигур этого виджета попадают все
    выбранные мышью фигуры.
    """

    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

        self.frame = Frame(self.master, width=170, height=300, bd=2,
                           relief="groove")
        self.shapes_list = Listbox(self.frame, width=25, height=10, bd=2)
        self.delete_button = Button(self.frame, text="Удалить", width=24,
                                    command=self.delete_shape)

        Label(self.frame, text="Настройка фигур").place(x=30, y=0)

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.shapes_list.place(x=4, y=30)
        self.delete_button.place(x=4, y=200)

    # Добавить в список фигуры, выбранные курсором
    def add_selected(self, sel):
        for item in sel:
            self.shapes_list.insert("end", item)

    # Очистить список при отмене выделения
    def deselect(self):
        self.shapes_list.delete(0, "end")

    # Удалить выбранную фигуру с холста и из списка
    def delete_shape(self):
        print(self.shapes_list.curselection())
        # self.canvas.canceled_objects.append()

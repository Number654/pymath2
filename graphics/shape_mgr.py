# -*- coding: utf-8 -*-

from tkinter import Frame, Listbox, Label
from tkinter.ttk import Button
from .canvas_object import CanvasObject


shape_names = {"line": "Прямая", "rectangle": "Прямоугольник",
               "circle": "Окружность", "text": "Надпись"}  # Русскоязычные названия фигур


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
        self.shapes = []

        self.frame = Frame(self.master, width=170, height=394, bd=2,
                           relief="groove")
        self.shapes_list = Listbox(self.frame, width=25, height=15, bd=2)
        self.delete_button = Button(self.frame, text="Удалить", width=24,
                                    command=lambda: self.delete(self.shapes_list.curselection()[0]))

        Label(self.frame, text="Настройка фигур").place(x=30, y=0)

        for i in range(20):
            self.add(CanvasObject("circle"))

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.shapes_list.place(x=4, y=30)
        self.delete_button.place(x=4, y=280)

    # Добавить в список фигуру
    def add(self, canvas_obj):
        self.shapes.append(canvas_obj)
        self.shapes_list.insert("end", str(len(self.shapes))+". "+shape_names[canvas_obj.figure])

    def delete(self, index):
        self.shapes_list.delete(0, "end")
        self.shapes.pop(index)
        for i, sh in enumerate(self.shapes, 1):
            self.shapes_list.insert("end", str(i)+". "+shape_names[sh.figure])

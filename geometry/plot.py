# -*- coding: utf-8 -*-

from tkinter import Frame, Canvas, Label
from math import *
from ..core import arcctg


# График
class Graph:

    def __init__(self, formula, first_x, ox_len, color="blue"):
        self.formula = formula
        self.first_x = first_x  # Начало отсчета оси OX
        self.ox_len = ox_len  # Число делений на оси OX
        self.color = color  # Цвет линии

    def create(self, canvas):
        f = self.formula.removeprefix("y=")
        first_x = self.first_x*(canvas.winfo_reqwidth()/self.ox_len)  # Начало оси OX (в пикселях)
        canvas_height = canvas.winfo_reqheight()
        for i in range(16000):
            try:
                x = first_x + i/16
                y = canvas_height-eval(f.replace("x", str(x)))
                canvas.create_oval(x, y, x+1, y+1, fill=self.color, outline=self.color)
            except ZeroDivisionError:
                pass


class Plotter:

    def __init__(self, master, width, height, ox, oy, grid=True):
        self.master = master
        self.grid = grid
        self.canvas_width = width-40
        self.canvas_height = height-40

        self.graphs = []
        self.ox = ox  # Числа для нумерации оси OX
        self.oy = oy  # Числа для нумерации оси OY
        self.ox_divisions = len(ox)  # Количество делений на оси OX
        self.oy_divisions = len(oy)  # Количество делений на оси OY

        self.frame = Frame(self.master, width=width, height=height)

        self.canvas = Canvas(self.frame, width=self.canvas_width,
                             height=self.canvas_height, bg="white", bd=-1.5)
        self.canvas.place(x=20, y=20)

        self.enumerate_oxy()
        self.draw_grid() if self.grid else None  # Отрисовываем сетку, если нужно

    # Разместить графики на окне
    def place(self, x=None, y=None):
        self.frame.place(x=x, y=y)

    # Добавить график
    def add_graph(self, o):
        self.graphs.append(o)

    # Удалить график
    def remove_graph(self, id__):
        self.graphs.pop(id__)

    # Очистить графики
    def clear(self):
        self.graphs = []

    # Пронумеровать оси
    def enumerate_oxy(self):
        for nox, ox in enumerate(self.ox, start=1):
            ox_l = Label(self.frame, text=ox)
            ox_l.place(x=20 + nox * (self.canvas_width / self.ox_divisions) - ox_l.winfo_reqwidth() / 2,
                       y=20 + self.canvas_width)
        for noy, oy in enumerate(self.oy.__reversed__(), start=0):  # Не снизу вверх, а сверху вниз
            oy_l = Label(self.frame, text=oy)
            oy_l.place(x=20 - oy_l.winfo_reqwidth(),
                       y=20 + noy * (self.canvas_height / self.oy_divisions) - oy_l.winfo_reqheight() / 2)

    # Нарисовать сетку
    def draw_grid(self):
        for x in range(self.ox_divisions):
            self.canvas.create_line(x*(self.canvas_width/self.ox_divisions),
                                    0, x*(self.canvas_width/self.ox_divisions), self.canvas_width, fill="lightgrey")
        for y in range(self.oy_divisions):
            self.canvas.create_line(0, y*(self.canvas_height/self.oy_divisions), self.canvas_height,
                                    y*(self.canvas_height/self.oy_divisions), fill="lightgrey")

    # Отрисовать все графики на холсте
    def plot(self):
        self.canvas.delete("all")  # Очистить все
        self.draw_grid() if self.grid else None  # Заново отрисовать сетку, если нужно
        for graph in self.graphs:
            graph.create(self.canvas)  # Снова отрисовать все графики

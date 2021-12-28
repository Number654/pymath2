# -*- coding: utf-8 -*-

from core import arcctg
from math import *  # Для тригонометрических функций

from tkinter import StringVar, Tk, Label, Frame
from tkinter.ttk import Entry, Button

from geometry.plot import Graph, Plotter


# Тест
if __name__ == '__main__':
    def plot(obj__, f):
        obj__.clear()  # Очистить предыдущие графики
        obj__.add_graph(Graph(f, 0, 10))  # Добавить новый график
        obj__.plot()  # Отрисовать

    root = Tk()
    root.title("Plotter Test")
    root.geometry("610x470")
    root.resizable(0, 0)
    root.config(bg="lightgrey")

    formula__ = StringVar()  # Строка с формулой

    p = Plotter(root, 450, 450, range(1, 11), range(1, 6))
    p.place(x=10, y=10)

    frame = Frame(root, width=130, height=80, bg="white")
    frame.place(x=470, y=10)
    Label(frame, text="Формула:", bg="white").place(x=35, y=0)

    formula_entry = Entry(frame, width=15, textvariable=formula__)
    formula_entry.place(x=15, y=25)
    button = Button(frame, text="Построить", width=15, command=lambda: plot(p, formula__.get()))
    button.place(x=15, y=50)

    root.mainloop()

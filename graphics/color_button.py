# -*- coding: utf-8 -*-

from tkinter import Button, StringVar
from tkinter.colorchooser import askcolor


# Вызвать диалог выбора цвета
def call(title):
    return askcolor(title=title)[1]


class ColorButton:

    """
    Кнопка, специально предназначенная для выбора цвета
    при нажатии на нее.

    Пояснение. Параметр "chooser_title" нужен для заголовка
    диалога выбора цвета, открывающенгося при нажатии на
    кнопку. Параметр "transparent_if_cancel" позволяет
    задать прозрачный цвет при нажатии конопки "Отмена" в
    диалоге выбора цвета.
    """

    def __init__(self, master, chooser_title="Цвет линии", transparent_if_cancel=False):
        self.master = master
        self.chooser_title = chooser_title
        self.transparency = transparent_if_cancel
        self.color_var = StringVar()

        self.button = Button(self.master, text="█" if not self.transparency else "□", bg="white",
                             activebackground="white", relief="flat", command=self.call_chooser)
        self.set_color("black")

    def place(self, x=0, y=0):
        self.button.place(x=x, y=y)

    def get_color(self):
        color = self.color_var.get()
        if color == "None":
            return
        return color

    def set_color(self, value=None):
        if value is None:
            if not self.transparency:
                return
            self.button.config(text="□", fg="black", activeforeground="black")
        else:
            self.button.config(text="█", fg=value, activeforeground=value)
        self.color_var.set(value)

    def call_chooser(self):
        self.set_color(call(self.chooser_title))

# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, GROOVE
from .color_button import ColorButton


class ColorWidget:

    def __init__(self, master, width, height):
        self.master = master
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

        # Главная рамка виджета
        self.frame = Frame(self.master, width=self.width,
                           height=self.height, relief=GROOVE, bd=2)

        self.label1 = Label(self.frame, text='Цвет линии:')
        self.label2 = Label(self.frame, text='Цвет заливки:')
        self.label1.place(x=5, y=0)
        self.label2.place(x=5, y=40)

        # Кнопки настройки цвета линии и заливки
        self.line_color_button = ColorButton(self.frame)
        self.fill_color_button = ColorButton(self.frame, chooser_title="Цвет заливки",
                                             transparent_if_cancel=True)
        self.fill_color_button.set_color(None)

    # Метод для размещения виджета на окне по координатам, указанным в __init__
    def place(self, x=0, y=0):
        self.x = x
        self.y = y
        self.frame.place(x=self.x, y=self.y)
        self.line_color_button.place(x=33, y=20)
        self.fill_color_button.place(x=33, y=60)

    def get_line_color(self):
        return self.line_color_button.get_color()

    def get_fill_color(self):
        return self.fill_color_button.get_color()


def main():
    tk = Tk()
    cwg = ColorWidget(tk, 91, 95)
    cwg.place(10, 10)
    tk.mainloop()


if __name__ == '__main__':
    main()

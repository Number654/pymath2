# -*- coding: utf-8 -*-

from tkinter import Frame, Radiobutton, IntVar


class ShapeSelector:

    """
    Виджет для выбора фигуры, которую нужно
    нарисовать.
    """

    def __init__(self, master):
        self.master = master
        self.choice = IntVar()
        self.choice.set(-1)

        self.frame = Frame(self.master, width=94, height=32, bd=2, relief="groove")
        self.line_btn = Radiobutton(self.frame, text="▬", indicatoron=0, font="Tahoma 10",
                                    variable=self.choice, value=0)
        self.rect_btn = Radiobutton(self.frame, text="◼", indicatoron=0, font="Tahoma 10",
                                    variable=self.choice, value=1)
        self.circle_btn = Radiobutton(self.frame, text="⬤", indicatoron=0, font="Tahoma 10",
                                      variable=self.choice, value=2)
        self.stop_btn = Radiobutton(self.frame, text="N", indicatoron=0, font="Times 10 bold",
                                    variable=self.choice, value=-1)

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.line_btn.place(x=1, y=0)
        self.rect_btn.place(x=26, y=0)
        self.circle_btn.place(x=48, y=0)
        self.stop_btn.place(x=70, y=0)

    def get(self):
        return self.choice.get()

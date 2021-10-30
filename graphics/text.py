# -*- coding: utf-8 -*-

from tkinter import Toplevel, StringVar, NW
from tkinter.ttk import Button, Entry
from tkinter.messagebox import showwarning
from time import time

from .canvas_object import CanvasObject
from core.fractions import isfloat


class TextSpawner:

    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

    # Закрыть диалог по нажатии на кнопку "OK"
    def do_spawn(self, dlg, text, coords):
        font = "Verdana 10"
        figure_name = "text@" + str(round(time()))

        # Проверка на корректность введенные координаты
        if isfloat(coords[0]) and isfloat(coords[1]):
            # Форматируем координаты. Дело в том, что в Tkinter координатный угол - верхний
            # Левый угол, а у нашего холста - нижний левый, поэтому нужно вычесть
            # Указанную координаату Y из высоты   холста.
            form_coords = [float(coords[0]), self.canvas.height - float(coords[1])]

            # Пишем текст
            self.canvas.write_text(form_coords, fill=self.canvas.color_wid.get_line_color(),
                                   text=text, font=font, anchor=NW, tag=figure_name)

            # Заносим этот текст в список объектов холста
            c_obj = CanvasObject("text", form_coords, fill=self.canvas.color_wid.get_line_color(),
                                 text=text, tag=figure_name)
            self.canvas.canvas_objects.append(c_obj)
            self.canvas.shape_manager.add(c_obj)
            self.canvas.now_figures += 1  # Увеличить число фигур - текст тоже учитывается

            dlg.destroy()
        else:
            showwarning("Ошибка", "Введите правильное десятичное число!")
            dlg.focus_set()

    # Диалог
    def spawn(self):
        dialog = Toplevel(self.master)
        dialog.transient(self.master)
        dialog.title("Вставка текста")
        dialog.geometry("180x100")
        dialog.resizable(0, 0)
        dialog.focus_set()

        entry_var = StringVar()
        x_var = StringVar()
        y_var = StringVar()

        my_entry = Entry(dialog, width=25, textvariable=entry_var)
        x_entry = Entry(dialog, width=12, textvariable=x_var)
        y_entry = Entry(dialog, width=12, textvariable=y_var)
        my_entry.place(x=10, y=10)
        x_entry.place(x=10, y=40)
        y_entry.place(x=90, y=40)

        ok_button = Button(dialog, text="OK", width=12,
                           command=lambda: self.do_spawn(dialog, entry_var.get(), [x_var.get(),
                                                                                   y_var.get()]))
        ok_button.place(x=93, y=70)

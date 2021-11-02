# -*- coding: utf-8 -*-

from tkinter import Frame, Listbox, Label, IntVar
from tkinter import Button as ColorButton
from tkinter.ttk import Button, Checkbutton


shape_names = {"line": "Отрезок", "rectangle": "Прямоугольник",
               "circle": "Окружность", "text": "Надпись"}  # Русскоязычные названия фигур


class ShapeManager:

    """
    Класс, реализующий виджет для изменения
    уже нарисованных фигур на холсте.
    В список фигур этого виджета попадают все
    выбранные мышью фигуры.
    """

    def __init__(self, master, canvas=None):
        self.master = master
        self.canvas = canvas
        self.shapes = []
        self.show_one_mode = IntVar()

        self.frame = Frame(self.master, width=170, height=425, bd=2,
                           relief="groove")
        self.shapes_list = Listbox(self.frame, width=25, height=12, bd=2, command=None)
        self.delete_button = Button(self.frame, text="Удалить", width=24,
                                    command=lambda: self.delete(self.shapes_list.curselection()[0]))
        self.show_one_mode_btn = Checkbutton(self.frame, text="Показывать по одной",
                                             variable=self.show_one_mode, command=self.show_mode)
        self.shape_wizard = Wizard(self.frame, self.canvas)

        Label(self.frame, text="Настройка фигур").place(x=30, y=0)
        self.shapes_list.bind("<<ListboxSelect>>", self.show_shape_on_canvas)

    # Так как в класс "GraphicsCanvas" нужно передать экземпляр класса "ShapeManager",
    # получается, что они ссылаются друг на друга. Поэтому, сначала в GraphicsCanvas
    # передается этот класс, а затем, с помощью этого метода, в этот класс передается
    # GraphicsCanvas. Вызов данного метода обязателен.
    def set_canvas(self, canvas):
        self.canvas = canvas
        self.shape_wizard.canvas = canvas

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.shapes_list.place(x=4, y=30)
        self.delete_button.place(x=4, y=230)
        self.show_one_mode_btn.place(x=4, y=255)
        self.shape_wizard.place(x=4, y=277)

    # Добавить в список фигуру
    def add(self, canvas_obj):
        self.shapes.append(canvas_obj)
        self.shapes_list.insert("end", str(len(self.shapes))+". "+shape_names[canvas_obj.figure])

    # Удалить фигуру с холста
    def delete(self, index):
        self.remove(index)
        self.canvas.canvas_objects.pop(index)
        self.canvas.now_figures -= 1

    # Удалить фигуру из списка
    def remove(self, index):
        self.shapes_list.delete(0, "end")
        self.shapes.pop(index)
        for i, sh in enumerate(self.shapes, 1):
            self.shapes_list.insert("end", str(i) + ". " + shape_names[sh.figure])

    def clear(self):
        self.shapes = []
        self.shapes_list.delete(0, "end")

    def show_mode(self):
        if self.show_one_mode.get():
            self.canvas.shape_selector.set(-1)
            self.canvas.shape_selector.disable()
            self.canvas.showed_now = []
            self.canvas.update()
            self.show_shape_on_canvas(None)
        else:
            self.canvas.showed_now = None
            self.canvas.shape_selector.enable()

    def show_shape_on_canvas(self, event):
        selected = self.shapes_list.curselection()
        if selected:
            if self.show_one_mode.get():
                self.canvas.showed_now = [self.canvas.canvas_objects[selected[0]]]
            self.shape_wizard.show_shape_view(selected[0])


class Wizard:

    """
    Виджет, который будет появляться в виджете
    настройки фигуры при выделении. Является
    самим настройщиком, содержит в себе все
    параметры настройки для каждого типа фигур.
    """

    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas  # Холст, на котром нарисованы все фигуры

        self.frame = Frame(self.master, width=158, height=137, bd=2, relief="groove")
        self.apply_button = Button(self.frame, width=23, text="Применить")

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.apply_button.place(x=2, y=105)

    def show_shape_view(self, sel_index):
        c_obj = self.canvas.canvas_objects[sel_index]
        if c_obj.figure == "line":
            shape_view = LineView(self.frame)
            shape_view.place(x=1, y=1)


class ShapeView:

    """
    Данный класс и его подклассы используются
    для отображения нескольких виджетов для
    настройки параметров фигур (виджет изменения
    цвета, виджет изменения размеров и координат
    и т. п.
    """

    def __init__(self, master):
        self.master = master

        self.frame = Frame(self.master, width=148, height=100)

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)

    def destroy(self):
        self.frame.destroy()


class LineView(ShapeView):

    def __init__(self, master):
        super().__init__(master)

        self.color_btn = ColorButton(self.frame, text="█", bg="white", relief="flat",
                                     activebackground="white")

        Label(self.frame, text="Цвет:").place(x=2, y=1)

    def place(self, x=0, y=0):
        super().place(x=x, y=y)
        self.color_btn.place(x=7, y=20)

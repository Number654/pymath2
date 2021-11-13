# -*- coding: utf-8 -*-

from tkinter import Frame, Listbox, Label, IntVar, StringVar
from tkinter.ttk import Button, Checkbutton, Entry
from tkinter.messagebox import showwarning

from core.pymath import better_divmod
from .color_button import ColorButton


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
        self.shape_wizard.destroy_shape_view()  # Убираем и настройщик фигуры - ведь она уже удалена

    def clear(self):
        self.shapes = []
        self.shapes_list.delete(0, "end")
        self.shape_wizard.destroy_shape_view()

    # Режим показа фиугы на холсте при выделении ее в списке
    def show_mode(self):
        if self.show_one_mode.get():  # Если флажок выделен, то
            self.canvas.shape_selector.set(-1)  # Отключаем рисование фигур
            self.canvas.shape_selector.disable()  # И отключаем сам виджет
            self.canvas.showed_now = []  # Подготавливаем переменную показа на холсте
            self.canvas.update()  # Обновляем холст, тем самым временно стрирая все остальные фигуры
            self.show_shape_on_canvas(None)  # Показываем выдеоенную сейчас фигуру
        else:  # Иначе делаем все наоборот: включаем виджет рисования фигур и т. д.
            self.canvas.showed_now = None
            self.canvas.shape_selector.enable()

    # Показать фигуру на холсте при выделении ее в списке
    def show_shape_on_canvas(self, event):
        selected = self.shapes_list.curselection()
        if selected:  # Если фигура выделена
            if self.show_one_mode.get():  # Если включен режим показа по одной фигуре,
                self.canvas.showed_now = [self.canvas.canvas_objects[selected[0]]]  # То отмечаем выделенную фигуру
            self.shape_wizard.show_shape_view(selected[0])  # Показываем настройщик для выделенной фигуры
        return event


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
        self.shape_view = ShapeView(self.frame)  # Фрейм с виджетами настройки выделенной фигуры

        self.apply_button = Button(self.frame, width=23, text="Применить", state="disabled")

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.apply_button.place(x=2, y=105)

    def show_shape_view(self, sel_index):
        if self.shape_view is not None:
            self.shape_view.destroy()

        c_obj = self.canvas.canvas_objects[sel_index]
        if c_obj.figure == "line":
            self.shape_view = LineView(self.frame, self.canvas, sel_index)
        elif c_obj.figure == "rectangle":
            self.shape_view = RectView(self.frame, self.canvas, sel_index)
        elif c_obj.figure == "circle":
            self.shape_view = CircleView(self.frame, self.canvas, sel_index)
        elif c_obj.figure == "text":
            self.shape_view = TextView(self.frame, self.canvas, sel_index)
        else:
            raise RuntimeError("Unknown shape type: %s." % c_obj.figure)

        self.shape_view.place(x=1, y=1)
        self.shape_view.set()
        self.apply_button.config(command=self.shape_view.apply, state="normal")

    def destroy_shape_view(self):
        self.shape_view.destroy()
        self.apply_button.config(command=None, state="disabled")


class SuperShapeView:

    """
    Данный класс и его подклассы используются
    для отображения нескольких виджетов для
    настройки параметров фигур (виджет изменения
    цвета, виджет изменения размеров и координат
    и т. п.
    """

    def __init__(self, master, canvas=None, index=None):
        self.master = master
        self.canvas = canvas
        self.index = index

        self.x1 = StringVar()
        self.y1 = StringVar()

        self.frame = Frame(self.master, width=148, height=100)

        self.x1_entry = Entry(self.frame, textvariable=self.x1, width=3)
        self.y1_entry = Entry(self.frame, textvariable=self.y1, width=3)

    def place(self, x=0, y=0):
        self.frame.place(x=x, y=y)
        self.x1_entry.place(x=2, y=75)
        self.y1_entry.place(x=42, y=75)

    def destroy(self):
        self.frame.destroy()

    def get_cell_size(self):
        if not self.canvas.pixel_mode_flag.get():
            return self.canvas.cell_size_wid.get()
        return 1

    def set(self):
        cell_size = self.get_cell_size()

        self.x1.set(str(better_divmod(self.canvas.canvas_objects[self.index].args[0][0], cell_size)[0]))
        self.y1.set(str(better_divmod(self.canvas.height - self.canvas.canvas_objects[self.index].args[0][1],
                                      cell_size)[0]))

    def apply(self):
        cell_size = self.get_cell_size()
        self.canvas.canvas_objects[self.index].args = (float(self.x1.get().replace(",", ".")) * cell_size,
                                                       (self.canvas.height // cell_size - float(
                                                        self.y1.get().replace(",", "."))) * cell_size,
                                                       )


class ShapeView(SuperShapeView):

    def __init__(self, master, canvas=None, index=None):
        super().__init__(master, canvas=canvas, index=index)
        self.line_width = StringVar()
        self.x2 = StringVar()
        self.y2 = StringVar()

        self.line_width_entry = Entry(self.frame, textvariable=self.line_width, width=7)
        self.x2_entry = Entry(self.frame, textvariable=self.x2, width=3)
        self.y2_entry = Entry(self.frame, textvariable=self.y2, width=3)

    def place(self, x=0, y=0):
        super().place(x=x, y=y)
        self.line_width_entry.place(x=100, y=26)
        self.x2_entry.place(x=82, y=75)
        self.y2_entry.place(x=122, y=75)

    def set(self):
        super().set()
        cell_size = self.get_cell_size()

        self.line_width.set(str(self.canvas.canvas_objects[self.index].kwargs["width"]))
        self.x2.set(str(better_divmod(self.canvas.canvas_objects[self.index].args[0][2], cell_size)[0]))
        self.y2.set(str(better_divmod(self.canvas.height - self.canvas.canvas_objects[self.index].args[0][3],
                                      cell_size)[0]))

    def apply(self):
        cell_size = self.get_cell_size()
        self.canvas.canvas_objects[self.index].args = ((float(self.x1.get().replace(",", ".")) * cell_size,
                                                        (self.canvas.height // cell_size - float(
                                                            self.y1.get().replace(",", "."))) * cell_size,
                                                        float(self.x2.get().replace(",", ".")) * cell_size,
                                                        (self.canvas.height // cell_size - float(
                                                            self.y2.get().replace(",", "."))) * cell_size),
                                                       )


class LineView(ShapeView):

    def __init__(self, master, canvas, index):
        super().__init__(master, canvas=canvas, index=index)
        self.color_btn = ColorButton(self.frame)

        Label(self.frame, text="Цвет:").place(x=2, y=1)
        Label(self.frame, text="Толщина:").place(x=50, y=1)
        Label(self.frame, text="X1:").place(x=2, y=50)
        Label(self.frame, text="Y1:").place(x=42, y=50)
        Label(self.frame, text="X2:").place(x=82, y=50)
        Label(self.frame, text="Y2:").place(x=122, y=50)

    def set(self):
        super().set()
        self.color_btn.set_color(self.canvas.canvas_objects[self.index].kwargs["outline"])

    def place(self, x=0, y=0):
        super().place(x=x, y=y)
        self.color_btn.place(x=7, y=22)
        self.line_width_entry.place(x=55, y=22)

    def apply(self):
        super().apply()
        self.canvas.canvas_objects[self.index].kwargs = {"outline": self.color_btn.get_color(),
                                                         "width": float(self.line_width.get()),
                                                         "name": self.canvas.canvas_objects[self.index].kwargs["name"]}


class RectView(ShapeView):

    def __init__(self, master, canvas, index):
        super().__init__(master, canvas=canvas, index=index)
        self.outline_color_button = ColorButton(self.frame)
        self.fill_color_button = ColorButton(self.frame, chooser_title="Цвет заливки",
                                             transparent_if_cancel=True)

        Label(self.frame, text="Цвет\nлинии:", font="Tahoma 8").place(x=-1, y=-4)
        Label(self.frame, text="Цвет\nзаливки:", font="Tahoma 8").place(x=45, y=-4)
        Label(self.frame, text="Толщина:", font="Tahoma 8").place(x=97, y=1)
        Label(self.frame, text="X1:").place(x=2, y=50)
        Label(self.frame, text="Y1:").place(x=42, y=50)
        Label(self.frame, text="X2:").place(x=82, y=50)
        Label(self.frame, text="Y2:").place(x=122, y=50)

    def place(self, x=0, y=0):
        super().place(x=x, y=y)
        self.outline_color_button.place(x=7, y=26)
        self.fill_color_button.place(x=59, y=26)

    def set(self):
        super().set()
        self.outline_color_button.set_color(self.canvas.canvas_objects[self.index].kwargs["outline"])
        self.fill_color_button.set_color(self.canvas.canvas_objects[self.index].kwargs["fill"])

    def apply(self):
        super().apply()
        self.canvas.canvas_objects[self.index].kwargs = {"outline": self.outline_color_button.get_color(),
                                                         "fill": self.fill_color_button.get_color(),
                                                         "width": float(self.line_width.get()),
                                                         "name": self.canvas.canvas_objects[self.index].kwargs["name"]}


class CircleView(RectView):
    pass


class TextView(SuperShapeView):

    def __init__(self, master, canvas, index):
        super().__init__(master, canvas=canvas, index=index)
        self.text_var = StringVar()

        self.color_btn = ColorButton(self.frame)
        self.text_entry = Entry(self.frame, width=10, textvariable=self.text_var)

    def place(self, x=0, y=0):
        super().place(x=x, y=y)
        self.text_entry.place(x=97, y=75)

    def set(self):
        super().set()
        self.color_btn.set_color(self.canvas.canvas_objects[self.index].kwargs["fill"])

    def apply(self):
        super().apply()
        self.canvas.canvas_objects[self.index].kwargs = {"fill": self.color_btn.get_color(),
                                                         "name": self.canvas.canvas_objects[self.index].kwargs["name"]}

# -*- coding: utf-8 -*-

from tkinter import Canvas, ALL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showwarning
from random import randint
from copy import deepcopy
from os.path import splitext

from .mouse import post_cell
from .xml_engine import *


figure_codes = ["line", "rectangle", "circle"]


class GeometryCanvas:

    def __init__(self, master, width, height, *args):
        self.master = master
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.cell_size_wid = args[1]  # Виджет изменения размера клетки
        self.color_wid = args[0]  # Виджет изменения цветов
        self.undo_btn = args[2]  # Кнопка "Отменить" действие
        self.redo_btn = args[3]  # Кнопка "Повторить" действие
        self.pixel_mode_flag = args[4]  # Флажок "Рисовать по пикселям или клеткам"
        self.shape_manager = args[5]  # Виджет настройки и управления фигурами

        self.begin_x = None
        self.begin_y = None

        self.is_running = True

        self.canvas_objects = []
        self.canceled_objects = []
        self.now_figures = 0  # Сколько сейчас фигур нарисовано?

        self.canvas = Canvas(master, width=self.width, height=self.height, bg="#ffffff",
                             cursor="tcross")

        # Привязываем действие к кнопке "отмены рисования последней фигуры"
        # И к кнопке "аовтора рисования отмененной фигуры"
        self.undo_btn['command'] = self.undo
        self.redo_btn['command'] = self.redo

    # Разместить GeometryCanvas на окне
    def place(self, x=0, y=0):
        self.x = x
        self.y = y
        self.canvas.place(x=self.x, y=self.y)

    # Обновить холст
    def update(self):
        self.canvas.delete(ALL)

    def clear_all(self):
        self.canvas_objects = []
        self.update()
        self.now_figures = 0

    # Команда для нажатия на кнопку "Очистить"
    # Отдельная команда с сохранением стертых фигур, чтобы можно было отменить очистку
    def clear_all_command(self):
        self.canceled_objects = deepcopy(self.canvas_objects)
        self.clear_all()

    # Нарисовать сетку
    def draw_net(self):
        cell_size = self.cell_size_wid.get()
        x = 0
        y = 0

        # Рисуем линии столбцов
        for col in range(round(self.width / cell_size)):
            self.canvas.create_line(x, 0, x, self.height, fill='lightblue')
            x += cell_size

        # Рисуем линии рядов
        # И у нас получаются клетки!
        for row in range(round(self.height / cell_size)):
            self.canvas.create_line(0, y, self.width, y, fill='lightblue')
            y += cell_size

    # Рисование разных фигур
    def draw_rectangle(self, *args, **kwargs):
        self.canvas.create_rectangle(args, kwargs)

    def draw_line(self, *args, **kwargs):
        self.canvas.create_line(args, kwargs)

    def draw_circle(self, *args, **kwargs):
        self.canvas.create_oval(args, kwargs)

    def write_text(self, *args, **kwargs):
        self.canvas.create_text(args, kwargs)

    # Получить координаты места начала зажатия левой кнопки мыши
    def start_drawing_by_mouse(self, event, figure):
        if figure != -1 and not ((event.x < self.x or event.x > self.x+self.width) or
                                 (event.y < self.y or event.y > self.y+self.height)):
            self.begin_x = event.x
            self.begin_y = event.y

    # Занести нарисованную фигуру в список всех фигур
    def stop_drawing_by_mouse(self, event, figure):
        figure_name = str(hex(randint(2, 2**50)))
        cell_size = self.cell_size_wid.get()

        if figure != -1 and not ((event.x < self.x or event.x > self.x+self.width) or
                                 (event.y < self.y or event.y > self.y+self.height)):
            try:
                # Если режим рисования с точностью до пикселей включен, то
                # Просто ссылаемся на координаты, не вызывая метода post_cell()
                if self.pixel_mode_flag.get() and (self.begin_x is not None and self.begin_y is not None):
                    begin_x_posted = self.begin_x
                    begin_y_posted = self.begin_y
                    x_posted = event.x
                    y_posted = event.y
                # Если режим рисования с точностью до пикселей выключен, то вызываем
                # Метод post_cell(), который просчитывает координаты по клеткам
                else:
                    begin_x_posted = post_cell(self.begin_x, cellsize=cell_size)
                    begin_y_posted = post_cell(self.begin_y, cellsize=cell_size)
                    x_posted = post_cell(event.x, cellsize=cell_size)
                    y_posted = post_cell(event.y, cellsize=cell_size)

                self.canvas_objects.append(CanvasObject(figure_codes[figure],
                                                        (begin_x_posted, begin_y_posted,
                                                         x_posted, y_posted),
                                                        outline=self.color_wid.get_line_color(),
                                                        fill=self.color_wid.get_fill_color(), name=figure_name))
                self.now_figures += 1  # Увеличиваем количество фигур
            except TypeError:
                pass
            self.begin_x, self.begin_y = (None, None)

    def get_mouse_pos(self):
        return [self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                self.canvas.winfo_pointery() - self.canvas.winfo_rooty()]

    def load(self):
        filename = askopenfilename(title='Импорт', filetypes=(('Geometry Drawing', '*.gd'),))

        # Если пользователь НЕ нажал кнопку отмена, то продолжаем:
        if filename != '':
            # Отделяем расширение от имени файла
            extension = splitext(filename)[1].lower()
            # Импортировать, к сожалению, можно только .gd файлы
            if extension != '.gd':
                showwarning(u'Ошибка', u'Неподдерживаемое расширение: %s' % extension)
            else:
                # Если файл поврежден или содержит неправильные типы фигур, кидаем ошибку
                try:
                    data = get_figures(filename)
                except (GeometryDrawingError, ParseError, ValueError) as err:
                    showwarning(u'Ошибка', u'Файл "%s", который Вы пытаетесь открыть, поврежден,'
                                           u'\nили имеет неподдерживаемые типы фигур.\n\n'
                                           u'Python-исключение: %s' % (filename, err))
                # Если все хорошо, то продолжем:
                else:
                    figures = data[0]
                    self.cell_size_wid.raw_set(data[1])
                    # Стираем все с холса
                    self.clear_all()
                    # Добавляем загруженные фигуры в canvas_objects
                    for figure in figures:
                        self.canvas_objects.append(figure)
                        self.now_figures += 1
                    # Добавляем в заголовок имя импортированного файла
                    self.master.title('GraphX - %s' % filename)

    def save(self):
        canvas = self

        def _get_all_figures():
            # Получаем все фигуры: их имена, типы, координаты, цвета
            figures = []
            for canvas_object in canvas.canvas_objects:
                if canvas_object.figure == "text":
                    figures.append(canvas_object)
                    continue

                if 'outline' not in canvas_object.kwargs.keys():
                    if canvas_object.kwargs['fill'] is None:
                        figures.append(CanvasObject(canvas_object.figure, canvas_object.args[0],
                                                    fill='',
                                                    tag=canvas_object.kwargs['name']))
                    else:
                        figures.append(CanvasObject(canvas_object.figure, canvas_object.args[0],
                                                    fill=canvas_object.kwargs['fill'],
                                                    tag=canvas_object.kwargs['name']))
                else:
                    if canvas_object.kwargs['fill'] is None:
                        figures.append(CanvasObject(canvas_object.figure, canvas_object.args[0],
                                                    fill='', outline=canvas_object.kwargs['outline'],
                                                    tag=canvas_object.kwargs['name']))
                    else:
                        figures.append(CanvasObject(canvas_object.figure, canvas_object.args[0],
                                                    fill=canvas_object.kwargs['fill'],
                                                    outline=canvas_object.kwargs['outline'],
                                                    tag=canvas_object.kwargs['name']))
            return figures

        filename = asksaveasfilename(title='Экспорт',
                                     filetypes=(('Portable Network Graphics', '*.png'), ('Geometry Drawing', '*.gd')))
        # Если пользователь НЕ нажал кнопку отмена, то продолжаем:
        if filename != '':
            # Отделяем расширение от имени файла
            extension = splitext(filename)[1].lower()
            # Если сохранить нужно в формате PNG-изображения, то:
            if extension == '.png':
                # Получаем все фигуры, переводим список этих фигур в PNG
                figures2png(_get_all_figures(), filename)
            # Если сохранить нужно в формате Geometry Drawing, то:
            if extension == '.gd':
                # Записываем все в указанный пользователем файл
                xml = save_figures(_get_all_figures(), self.cell_size_wid.get())
                write_to_file(xml, filename)
            # Если пользователь указал неверное расширение (формат файла), то кидаем ошибку
            if extension != '.png' and extension != '.gd':
                showwarning(u'Ошибка', u'Неподдерживаемое расширение: %s' % extension)

    # Отменить последнее действие
    def undo(self):
        self.canceled_objects.append(self.canvas_objects[-1])
        self.canvas_objects.pop(-1)
        self.now_figures -= 1  # Отменить рисование фигуры - уменьшаем к-во фигур

    # Повторить отмененное действие
    def redo(self):
        self.canvas_objects.append(self.canceled_objects[-1])
        self.canceled_objects.pop(-1)
        self.now_figures += 1  # Повтороить отмененную фигуру - снова увеличиваем число фигур

    def quit(self):
        self.is_running = False

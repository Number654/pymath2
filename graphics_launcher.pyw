# -*- coding: utf-8 -*-

from tkinter.ttk import Radiobutton
from time import sleep
from graphics.graphics_canvas import *
from graphics.cellsize import *
from graphics.color import *
from graphics.text import *
from graphics.shape_mgr import *
from graphics.shape_selector import ShapeSelector

WAIT_TIME = 0.0044


# Окно
tk = Tk()
tk.title('GraphX')
tk.geometry("910x460")

# Переменная для установки режима рисования с точностью до пикселей
pixel_mode = IntVar()

csw = CellSizeWidget(tk, 94, 68)
cwg = ColorWidget(tk, 94, 95)

shape_selector = ShapeSelector(tk)
shape_selector.place(x=625, y=413)

undo_redo_frame = Frame(tk, width=94, height=83, relief=GROOVE, bd=2)
undo_redo_frame.place(x=625, y=194)

shape_mgr = ShapeManager(tk)
shape_mgr.place(730, 20)

canvas = GeometryCanvas(tk, 596, 394, cwg, csw, pixel_mode, shape_mgr, shape_selector)
canvas.place(x=19, y=20)
canvas.draw_net()

shape_mgr.set_canvas(canvas)  # Задаем холст для виджета управления фигурами
csw.set_canvas(canvas)

cwg.place(x=625, y=21)
csw.place(x=625, y=121)

# Кнопки экспорта, импорта, сохраниния изменений рисунка
export_image_button = Button(tk, text='Экспорт...', width=12, command=canvas.save)
import_image_button = Button(tk, text='Импорт...', width=12, command=canvas.load)
export_image_button.place(x=536, y=420)
import_image_button.place(x=450, y=420)


# Выбор режимов рисования: по пикселям или по клеточкам
drawing_accuracy_frame = Frame(tk, width=94, height=66, relief=GROOVE, bd=2)
drawing_accuracy_frame.place(x=625, y=282)
Label(drawing_accuracy_frame, text="Рисование по:").place(x=0, y=0)

# Для режима рисования по клеткам
cell_accuracy_mode_radiobtn = Radiobutton(drawing_accuracy_frame, text="Клеткам", variable=pixel_mode, value=0)
cell_accuracy_mode_radiobtn.place(x=7, y=20)

# Для режима рисования по пикселям
pixel_accuracy_mode_radiobtn = Radiobutton(drawing_accuracy_frame, text="Пикселям", variable=pixel_mode, value=1)
pixel_accuracy_mode_radiobtn.place(x=7, y=40)


two_buttons_frame = Frame(tk, width=94, height=55, bd=2, relief="groove")
two_buttons_frame.place(x=625, y=353)

# Кнопка очистки холста
clear_canvas_button = Button(two_buttons_frame, text="Очистить", width=13, command=canvas.clear_all)
clear_canvas_button.place(x=1, y=0)

# Кнопка для всавки текста
tsr = TextSpawner(tk, canvas)
spawn_text_button = Button(two_buttons_frame, text='Вставка текста', width=13, command=tsr.spawn)
spawn_text_button.place(x=1, y=25)


# Текст для отображения текущего положения курсора
coordinates_text = Label(tk)
coordinates_text.place(x=19, y=420)

tk.bind_all("<ButtonPress-1>", lambda event: canvas.start_drawing_by_mouse(event, shape_selector.get()))
tk.bind_all("<ButtonRelease-1>", lambda event: canvas.stop_drawing_by_mouse(event, shape_selector.get()))
tk.bind_all("<KeyPress-Shift_L>", lambda event: canvas.set_attr("shift", True))
tk.bind_all("<KeyRelease-Shift_L>", lambda event: canvas.set_attr("shift", False))

tk.protocol("WM_DELETE_WINDOW", canvas.quit)

while canvas.is_running:
    canvas.update()
    canvas.draw_net()

    # Выводим на экран текущую позицию курсора мыши в пикселях и клетках
    pointer = canvas.abs_mouse_pos()
    coordinates_text['text'] = "X: %s Y: %s  |  X: %s кл. Y: %s кл.  |  %s shapes total" % \
                               (pointer[0], pointer[1],
                                int(better_divmod(pointer[0], canvas.cell_size_wid.get())[0]),
                                int(better_divmod(canvas.height - pointer[1], canvas.cell_size_wid.get())[0]),
                                canvas.now_figures)
    drawing_now = shape_selector.get()

    # Отрисовываем ранее созданные фигуры
    for i in canvas.canvas_objects if canvas.showed_now is None else canvas.showed_now:
        if i.figure == "line":
            canvas.draw_line(*i.args, fill=i.kwargs["outline"], width=i.kwargs["width"], tag=i.kwargs["name"])
        if i.figure == "rectangle":
            canvas.draw_rectangle(*i.args, fill=i.kwargs["fill"], width=i.kwargs["width"], outline=i.kwargs["outline"],
                                  tag=i.kwargs["name"])
        if i.figure == "circle":
            canvas.draw_circle(*i.args, fill=i.kwargs["fill"], width=i.kwargs["width"], outline=i.kwargs["outline"],
                               tag=i.kwargs["name"])
        if i.figure == "text":
            font = "Verdana " + str(i.kwargs["size"])
            if i.kwargs["bold"]:
                font += " bold"
            if i.kwargs["italic"]:
                font += " italic"
            if i.kwargs["underline"]:
                font += " underline"

            canvas.write_text(*i.args, fill=i.kwargs["fill"], text=i.kwargs["text"],
                              font=font,
                              tag=i.kwargs["name"], anchor=NW)

    # Процесс рисования фигуры продолжается до отпускания левой кнопки мыши:
    if drawing_now != -1 and not \
            ((pointer[0] > canvas.x+canvas.width) or (pointer[1] > canvas.y+canvas.height)) and \
            (canvas.begin_x is not None and canvas.begin_y is not None):
        mouse_pos = canvas.canvas_mouse_pos()  # Получаем позицию курсора относительно холста для отрисовки
        cell_size = csw.get()

        # Если режим рисования с точностью до пикселей включен, то
        # Просто ссылаемся на координаты, не вызывая метода post_cell()
        if pixel_mode.get():
            begin_x_posted = canvas.begin_x
            begin_y_posted = canvas.begin_y
            x_posted = mouse_pos[0]
            y_posted = mouse_pos[1]
        # Если режим рисования с точностью до пикселей выключен, то вызываем
        # Метод post_cell(), который просчитывает координаты по клеткам
        else:
            begin_x_posted = post_cell(canvas.begin_x, cellsize=cell_size)
            begin_y_posted = post_cell(canvas.begin_y, cellsize=cell_size)
            x_posted = post_cell(mouse_pos[0], cellsize=cell_size)
            y_posted = post_cell(mouse_pos[1], cellsize=cell_size)

        if canvas.shift and drawing_now != 0:
            width = x_posted - begin_x_posted
            y_posted = begin_y_posted+width

        if drawing_now == 0:
            canvas.draw_line(begin_x_posted, begin_y_posted, x_posted, y_posted,
                             fill=canvas.color_wid.get_line_color(), width=1)

        if drawing_now == 1:
            canvas.draw_rectangle(begin_x_posted, begin_y_posted, x_posted, y_posted,
                                  fill=canvas.color_wid.get_fill_color(),
                                  outline=canvas.color_wid.get_line_color(), width=1)

        if drawing_now == 2:
            canvas.draw_circle(begin_x_posted, begin_y_posted, x_posted, y_posted,
                               fill=canvas.color_wid.get_fill_color(),
                               outline=canvas.color_wid.get_line_color(), width=1)
        del mouse_pos

    sleep(WAIT_TIME)
    tk.update_idletasks()
    tk.update()

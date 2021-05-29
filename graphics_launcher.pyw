# -*- coding: utf-8 -*-

from tkinter import IntVar, TclError
from tkinter.ttk import Radiobutton
from time import sleep
from graphics.graphics_canvas import *
from graphics.cellsize import *
from graphics.color import *
from graphics.text import *

# Окно
tk = Tk()
tk.title('Graphics')
tk.geometry("730x460")
tk.resizable(0, 0)

# Переменная для установки режима рисования с точностью до пикселей
pixel_mode = IntVar()

csw = CellSizeWidget(tk, 94, 68)
cwg = ColorWidget(tk, 94, 95)

undo_redo_frame = Frame(tk, width=94, height=55, relief=GROOVE, bd=2)
undo_redo_frame.place(x=625, y=194)
#
undo_button = Button(undo_redo_frame, text='Отмена', state=DISABLED)
redo_button = Button(undo_redo_frame, text='Повтор', state=DISABLED)
undo_button.place(x=7, y=0)
redo_button.place(x=7, y=25)

canvas = GeometryCanvas(tk, cwg, csw, undo_button, redo_button, pixel_mode, 596, 394)
canvas.place(x=19, y=20)
canvas.draw_net()

cwg.place(x=625, y=21)
cwg.enable_fill()

csw.place(x=625, y=121)

tsr = TextSpawner(tk, canvas)
spawn_text_button = Button(tk, text='Вставка текста', width=14, command=tsr.spawn)
spawn_text_button.place(x=625, y=323)

# Кнопки экспорта, импорта, сохраниния изменений рисунка
export_image_button = Button(tk, text='Экспорт...', width=12, command=canvas.save)
import_image_button = Button(tk, text='Импорт...', width=12, command=canvas.load)
export_image_button.place(x=536, y=420)
import_image_button.place(x=450, y=420)


# Выбор режимов рисования: по пикселям или по клеточкам
drawing_accuracy_frame = Frame(tk, width=94, height=66, relief=GROOVE, bd=2)
drawing_accuracy_frame.place(x=625, y=254)
Label(drawing_accuracy_frame, text="Рисование по:").place(x=0, y=0)

# Для режима рисования по клеткам
cell_accuracy_mode_radiobtn = Radiobutton(drawing_accuracy_frame, text="Клеткам", variable=pixel_mode, value=0)
cell_accuracy_mode_radiobtn.place(x=7, y=20)

# Для режима рисования по пикселям
pixel_accuracy_mode_radiobtn = Radiobutton(drawing_accuracy_frame, text="Пикселям", variable=pixel_mode, value=1)
pixel_accuracy_mode_radiobtn.place(x=7, y=40)

# Кнопка очистки холста
clear_canvas_button = Button(tk, text="Очистить", width=14, command=canvas.clear_all_command)
clear_canvas_button.place(x=625, y=350)


# Текст для отображения текущего положения курсора
coordinates_text = Label(tk)
coordinates_text.place(x=19, y=420)

tk.bind_all("<KeyPress-Control_L>", lambda event: canvas.set_drawing_by_mouse(event, "line"))
tk.bind_all("<KeyRelease-Control_L>", canvas.unset_drawing_by_mouse)

tk.bind_all("<KeyPress-Shift_L>", lambda event: canvas.set_drawing_by_mouse(event, "rectangle"))
tk.bind_all("<KeyRelease-Shift_L>", canvas.unset_drawing_by_mouse)

tk.bind_all("<KeyPress-Alt_L>", lambda event: canvas.set_drawing_by_mouse(event, "circle"))
tk.bind_all("<KeyRelease-Alt_L>", canvas.unset_drawing_by_mouse)

tk.bind_all("<Button-1>", canvas.start_drawing_by_mouse)
tk.bind_all("<ButtonRelease-1>", canvas.stop_drawing_by_mouse)

tk.protocol("WM_DELETE_WINDOW", canvas.quit)

while canvas.is_running:
    canvas.update()
    canvas.draw_net()

    # Выводим на экран текущую позицию курсора мыши в пикселях и клетках
    pointer = canvas.get_mouse_pos()
    coordinates_text['text'] = "X: %s Y: %s  |  X: %s кл. Y: %s кл." % \
                               (pointer[0], pointer[1],
                                int(divmod(pointer[0], canvas.cell_size_wid.get())[0]),
                                int(divmod(canvas.height - pointer[1], canvas.cell_size_wid.get())[0]))

    # Если количество фигур на холсте больше нуля, то включаем
    # Кнопку "отмена", ведь теперь можно убрать последнюю нарисованную
    # Фигуру
    if len(canvas.canvas_objects) > 0:
        undo_button['state'] = 'normal'
    else:
        undo_button['state'] = 'disabled'

    # Если количесво "отмененных" фигур больше нуля,
    # То включаем кнопку "повтор"
    if len(canvas.canceled_objects) > 0:
        redo_button['state'] = 'normal'
    else:
        redo_button['state'] = 'disabled'

    # Отрисовываем ранее созданные фигуры
    for i in canvas.canvas_objects:
        if i.figure == "line":
            canvas.draw_line(i.args, fill=i.kwargs["outline"], tag=i.kwargs["name"])
        if i.figure == "rectangle":
            canvas.draw_rectangle(i.args, fill=i.kwargs["fill"], outline=i.kwargs["outline"],
                                  tag=i.kwargs["name"])
        if i.figure == "circle":
            canvas.draw_circle(i.args, fill=i.kwargs["fill"], outline=i.kwargs["outline"],
                               tag=i.kwargs["name"])
        if i.figure == "text":
            canvas.write_text(i.args, fill=i.kwargs["fill"], text=i.kwargs["text"],
                              font="Verdana 10", anchor=NW)

    # Процесс рисования фигуры продолжается до отпускания левой кнопки мыши:
    if canvas.is_drawing_now:
        mouse_pos = canvas.get_mouse_pos()
        cell_size = csw.get()

        try:
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

            if canvas.is_drawing_now == "line":
                canvas.draw_line(begin_x_posted, begin_y_posted, x_posted, y_posted,
                                 fill=canvas.color_wid.get_line_color())

            if canvas.is_drawing_now == "rectangle":
                canvas.draw_rectangle(begin_x_posted, begin_y_posted, x_posted, y_posted,
                                      fill=canvas.color_wid.get_fill_color(),
                                      outline=canvas.color_wid.get_line_color())

            if canvas.is_drawing_now == "circle":
                canvas.draw_circle(begin_x_posted, begin_y_posted, x_posted, y_posted,
                                   fill=canvas.color_wid.get_fill_color(),
                                   outline=canvas.color_wid.get_line_color())
        # Тут убираются ошибки о том, что в качестве аргументов для вычисления
        # Координат в функцию передается мусор
        except (TypeError, TclError):
            pass
        del mouse_pos

    sleep(0.01)
    tk.update_idletasks()
    tk.update()

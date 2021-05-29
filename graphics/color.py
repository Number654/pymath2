# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, Button, StringVar, GROOVE, FLAT, DISABLED, NORMAL
from tkinter.colorchooser import askcolor


def choose_color(title):
    return askcolor(title=title)[1]


class ColorWidget:

    def __init__(self, master, width, height):
        self.master = master
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.line_color = StringVar()
        self.fill_color = StringVar()

        self.line_color.set("black")
        self.fill_color.set(None)

        # Главная рамка виджета
        self.frame = Frame(self.master, width=self.width,
                           height=self.height, relief=GROOVE, bd=2)

        self.label1 = Label(self.frame, text='Цвет линии:')
        self.label2 = Label(self.frame, text='Цвет заливки:', state=DISABLED)
        self.label1.place(x=5, y=0)
        self.label2.place(x=5, y=40)

        # Кнопки настройки цвета линии и заливки
        self.line_color_button = Button(self.frame, text='█', fg=self.get_line_color(),
                                        activeforeground=self.get_line_color(),
                                        bg='white',
                                        activebackground='white', relief=FLAT,
                                        command=self.set_line_color)
        self.fill_color_button = Button(self.frame, text='□', fg=self.get_fill_color(),
                                        activeforeground=self.get_fill_color(),
                                        disabledforeground=self.get_fill_color(),
                                        state=DISABLED, relief=FLAT, bg='white',
                                        activebackground='white',
                                        command=self.set_fill_color)
        self.line_color_button.place(x=35, y=20)
        self.fill_color_button.place(x=35, y=60)

    # Метод для размещения виджета на окне по координатам, указанным в __init__
    def place(self, x=0, y=0):
        self.x = x
        self.y = y
        self.frame.place(x=self.x, y=self.y)

    def enable_fill(self):
        self.label2.config(state=NORMAL)
        self.fill_color_button.config(state=NORMAL)
        # Если нет заливки, то отображаем пустой квадратик на кнопке заливки
        if self.get_fill_color() is None:
            self.fill_color_button.config(text='□')
        else:
            self.fill_color_button.config(text='█')

    def disable_fill(self):
        self.label2.config(state=DISABLED)
        self.fill_color_button.config(state=DISABLED)
        # Если нет заливки, то отображаем пустой квадратик на кнопке заливки
        if self.get_fill_color() is None:
            self.fill_color_button.config(text='□')
        else:
            self.fill_color_button.config(text='█')

    def set_line_color(self):
        c = choose_color('Цвет линии')
        # Цвет линии не может быть прозрачным, поэтому делаем его черным
        if c is None:
            self.line_color.set('black')
        else:
            self.line_color.set(c)
        # Отображаем выбранный цвет на кнопке
        self.line_color_button.config(fg=self.get_line_color(),
                                      activeforeground=self.get_line_color())

    def set_fill_color(self):
        c = choose_color('Цвет заливки')
        # Здесь, если выбрана прозрачная заливка, то делаем цвет теста кнопки черным, но показываем
        # Пустым квадратиком, что заливка прозрачная.
        if c is None:
            self.fill_color.set('None')
            self.fill_color_button.config(fg='black',
                                          activeforeground='black', text='□')
        # Иначе, делаем текст кнопки выбранного цвета и ставим заполненный квадратик
        else:
            self.fill_color.set(c)
            self.fill_color_button.config(fg=self.get_fill_color(),
                                          activeforeground=self.get_fill_color(), text='█')

    def get_line_color(self):
        if self.line_color.get() == 'None':
            return None
        return self.line_color.get()

    def get_fill_color(self):
        if self.fill_color.get() == 'None':
            return None
        return self.fill_color.get()


def main():
    tk = Tk()

    cwg = ColorWidget(tk, 10, 10, 88, 95)
    cwg.place()
    cwg.enable_fill()

    tk.mainloop()


if __name__ == '__main__':
    main()

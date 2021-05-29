# -*- coding: utf-8 -*-

from tkinter import ttk, Tk, Canvas, Label
from math import pi, cos, sin
import time


def circle_point(radius, angle):
    return radius*cos(angle), radius*sin(angle)


class Clock:
    saved_time = None

    def __init__(self):
        self.tk = Tk()
        # self.tk.geometry("350x340")
        self.tk.resizable(0, 0)
        self.tk.title("Clock")

        self.time_text = Label(self.tk, text="", font=("Helvetica", 19))
        self.time_text.pack(side="top")

        self.canvas = Canvas(self.tk, width=350, height=270)
        self.canvas.pack()

        self.overclock_button = ttk.Button(self.tk, text="OVERCLOCK", width=20, command=self.overclock)
        self.overclock_button.pack(pady=10)

        self.tk.after_idle(self.time_process)  # Запустить процесс хода часов

        self.canvas.create_oval(75, 50, 275, 250)  # Круг циферблата (радиус=100)

        for x in range(1, 13):
            b = circle_point(100, (x * 30 - 90) * pi / 180)  # Для точек на циферблате
            v = circle_point(112, (x * 30 - 90) * pi / 180)  # Для цифр

            self.canvas.create_oval(175 + b[0] - 2, 150 + b[1] - 2,
                                    175 + b[0] + 2, 150 + b[1] + 2, fill="black")  # Ставим точки на циферблате
            self.canvas.create_text(175 + v[0], 150 + v[1], text=x)  # Ставим цифры

        # Заглушки для первичной отрисовки стрелок
        self.s_point = 0
        self.m_point = 0
        self.h_point = 0
        self.s_arrow = self.canvas.create_line(0, 0, 0, 0)
        self.m_arrow = self.canvas.create_line(0, 0, 0, 0)
        self.h_arrow = self.canvas.create_line(0, 0, 0, 0)

        self.tk.mainloop()

    def set_time(self, setting_time):
        split = setting_time.split(":")  # Разделяем время на часы, миинуты и секунды
        self.time_text["text"] = setting_time  # Выводим время на экран в цифровом формате
        h = int(split[0])
        m = int(split[1])
        s = int(split[2])

        # Обновляем стрелки
        self.canvas.delete(self.s_arrow)
        self.canvas.delete(self.m_arrow)
        self.canvas.delete(self.h_arrow)

        # Получаем точки концов стрелок в зависимости от времени
        self.s_point = circle_point(90, (s * 6 - 90) * pi / 180)
        self.m_point = circle_point(70, ((m + s / 60) * 6 - 90) * pi / 180)  # (Минуты + секунды) / 60
        self.h_point = circle_point(30, ((h + m / 60) * 30 - 90) * pi / 180)  # (Часы + минуты) / 60

        # Отрисовыыаем стрелки
        self.s_arrow = self.canvas.create_line((175, 150), self.s_point[0] + 175,
                                               self.s_point[1] + 150, width=1, arrow="last")
        self.m_arrow = self.canvas.create_line((175, 150), self.m_point[0] + 175,
                                               self.m_point[1] + 150, width=2, arrow="last")
        self.h_arrow = self.canvas.create_line((175, 150), self.h_point[0] + 175,
                                               self.h_point[1] + 150, width=3, arrow="last")

    # Запустить процесс хода разогнанных часов
    def overclock(self):
        # Теперь разогнать часы нельзя, и нужно перезагрузить приложение, чтобы вернуться в обычный режим
        self.overclock_button.config(text="RESTART TO VIEW REAL TIME", state="disabled", width=28)
        self.tk.after_cancel(self.tk.after_id)  # Остановить процесс хода обычных часов
        self.tk.after_idle(self.overclock_process)
        self.saved_time = [int(v) for v in time.strftime("%H:%M:%S").split(":")]  # Получаем текущее время и сохраняем

    # Процесс хода разогнанных часов
    def overclock_process(self):
        self.saved_time[2] += 1

        if self.saved_time[2] == 60:
            self.saved_time[2] = 0
            self.saved_time[1] += 1

        if self.saved_time[1] == 60:
            self.saved_time[1] = 0
            self.saved_time[0] += 1

        if self.saved_time[0] == 24:
            self.saved_time[0] = 0

        self.tk.after(15, self.overclock_process)  # Минута идет со скоростью секунды
        self.set_time("%.2d:%.2d:%.2d" % tuple(self.saved_time))

    # Процесс хода часов
    def time_process(self):
        t = time.strftime("%H:%M:%S")  # Получаем текущее время
        self.tk.after_id = self.tk.after(1000, self.time_process)  # Ход стрелки через каждую секунду
        self.set_time(t)  # Устанавливаем полученное текущее время


if __name__ == '__main__':
    clock = Clock()

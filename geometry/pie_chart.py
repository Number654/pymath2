# -*- coding: utf-8 -*-

from tkinter import Tk
from tkinter import Canvas, Frame


class LegendLabel:

    def __init__(self, canvas, text, point_color="lightblue"):
        self.canvas = canvas
        self.text = text
        self.p_color = point_color

    def draw(self, x, y):
        self.canvas.create_rectangle(x, y-2.5, x+5, y+5, fill=self.p_color,
                                     outline="black" if self.p_color == "white" else self.p_color)
        self.canvas.create_text(x+10, y, text=self.text, anchor="w")


class PieChart:

    def __init__(self, width, radius, values, colors, master):
        self.w = width  # Ширина области диаграммы
        self.radius = radius  # Радиус круга диаграммы
        self.values = values  # Словарь значений
        self.colors = colors  # Словарь цветов для каждого сектора
        self.degrees_per_1 = 360/sum(values[key] for key in values)  # Градусов на единицу общего количества значерий
        self.percentage = {key: str(round(values[key]/(sum(values[key] for key in values))*100, 2))+"%"
                           for key in values}  # Отношение каждого значения к их сумме, %. Округление до 0.01%

        self.master = master

        self.main_frame = Frame(self.master, width=self.w, height=self.radius*2)
        self.chart_canvas = Canvas(self.main_frame, width=self.radius*2, height=self.radius*2,
                                   bg="white", bd=-2)
        self.legend_canvas = Canvas(self.main_frame, width=self.w-self.radius*2, height=self.radius*2,
                                    bd=-2)

    def draw(self, x, y):
        start_angle = 0  # Угол, с которого следует начинать рисовать следующий угол (сумма всех предыдущих углов)
        for val in self.values:
            new_angle = self.degrees_per_1*self.values[val]
            self.chart_canvas.create_arc(0, 0, self.radius*2, self.radius*2, start=start_angle, extent=new_angle,
                                         fill=self.colors[val])
            start_angle += new_angle

        # Пишем легенду диаграммы
        for i, name in enumerate(self.colors):
            # Y - через каждые 18 пкс, от верхнего края 5 пкс
            LegendLabel(self.legend_canvas, name+" (%s)" % self.percentage[name],
                        point_color=self.colors[name]).draw(5, 10+i*18)

        self.chart_canvas.place(x=0, y=0)
        self.legend_canvas.place(x=self.radius*2, y=0)
        self.main_frame.place(x=x, y=y)


if __name__ == '__main__':
    tk = Tk()
    tk.geometry("540x380")

    pc = PieChart(380, 100, {"От 2 до 5 ч.": 15, "От 1 до 2 ч.": 4, "Менее 1 ч.": 1},
                  {"От 2 до 5 ч.": "red", "От 1 до 2 ч.": "blue", "Менее 1 ч.": "green"}, tk)
    pc.draw(30, 30)

    tk.mainloop()

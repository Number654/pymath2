# -*- coding: utf-8 -*-

import turtle
from math import sqrt


if not __name__ == '__main__':
    raise RuntimeError('There is no way to import it now, but in future ...')

# Подготовка к рисованию
scr = turtle.Screen()
scr.setup(410, 470)
scr.title('Не смотри!')
pen = turtle.Pen(shape='circle')
pen.shapesize(0.09)
pen.speed(250)
pen.hideturtle()
pen.up()
pen.backward(190)
pen.left(90)
pen.forward(220)
pen.right(90)
pen.down()

# Рисование
# Рисуем рамку
pen.color(0, 0, 1)
pen.forward(260)
pen.right(90)
pen.forward(390)
pen.right(90)
pen.forward(260)
pen.right(90)
pen.forward(390)
# Столбцы
pen.up()
pen.right(90)
pen.forward(10)
pen.down()
for col in range(25):
    pen.up()
    pen.right(90)
    pen.down()
    pen.forward(390)
    pen.up()
    pen.backward(390)
    pen.left(90)
    pen.forward(10)
    pen.down()
# Строки
pen.up()
pen.right(90)
pen.forward(10)
pen.left(90)
pen.backward(260)
for row in range(38):
    pen.down()
    pen.forward(260)
    pen.up()
    pen.backward(260)
    pen.right(90)
    pen.forward(10)
    pen.left(90)
# Первые диагонали
pen.left(90)
pen.forward(10)
pen.right(90)
pen.color(0, 1, 0)
c = 1
is_short = False
for one in range(1, 40):
    pen.down()
    pen.right(45)
    if one == 27:
        is_short = True
    if one >= 27:
        pen.forward((10 * sqrt(2)) * (one-c))
        pen.up()
        pen.backward((10 * sqrt(2)) * (one-c))
    else:
        pen.forward((10 * sqrt(2)) * one)
        pen.up()
        pen.backward((10 * sqrt(2)) * one)
    if is_short:
        c += 1
    pen.up()
    pen.left(45)
    pen.left(90)
    pen.forward(10)
    pen.right(90)
del c, is_short
pen.up()
pen.left(90)
pen.backward(10)
pen.right(90)
pen.forward(10)
rng = list(range(1, 27))
rng.reverse()
for one1 in rng:
    pen.down()
    pen.right(45)
    pen.forward((10*sqrt(2)) * (one1-1))
    pen.up()
    pen.backward((10*sqrt(2)) * (one1-1))
    pen.left(45)
    pen.forward(10)
del rng
# Вторые диагонали
pen.color(1, 0, 0)
pen.up()
pen.left(90)
pen.backward(390)
pen.left(90)
pen.forward(20)
pen.right(90)
for two in range(1, 27):
    pen.down()
    pen.right(45)
    pen.forward((10 * sqrt(2)) * two)
    pen.up()
    pen.backward((10 * sqrt(2)) * two)
    pen.left(45)
    pen.left(90)
    pen.forward(10)
    pen.right(90)
pen.up()
pen.left(90)
pen.backward(10)
pen.right(90)
pen.forward(10)
d = 1
for two1 in range(1, 14):
    pen.down()
    pen.right(45)
    pen.forward((10 * sqrt(2)) * 26)
    pen.up()
    pen.backward((10 * sqrt(2)) * 26)
    pen.left(45)
    pen.forward(10)
pen.up()
pen.forward(240)
pen.right(90)
for two2 in range(1, 27):
    pen.down()
    pen.left(45)
    pen.forward((10*sqrt(2)) * two2)
    pen.up()
    pen.backward((10 * sqrt(2)) * two2)
    pen.left(45)
    pen.backward(10)
    pen.right(90)

# Математика - это интересно!
pen.color(0, 0, 0)
pen.up()
pen.right(90)
pen.forward(160)
pen.write('Математика — это интересно!', font='Times 22')

turtle.mainloop()

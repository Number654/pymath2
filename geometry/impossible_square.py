# -*- coding: utf-8 -*-

from tkinter import Canvas, Tk


class ImpossibleSquare:
    POLYGONS = 4

    def __init__(self, canvas, coordinates, size=(300, 300, 50), colors=('grey', 'lightgrey', '#3b3b3b', 'white')):

        self.canvas = canvas
        self.coordinates = coordinates
        self.size = size
        self.colors = colors

    def draw(self):
        # Polygon 1
        self.canvas.create_polygon(((self.coordinates[0] + self.size[2], self.coordinates[1]),

                                   (self.coordinates[0], self.coordinates[1] + self.size[2]),

                                   (self.coordinates[0], self.size[1] + self.coordinates[1]),

                                   (self.coordinates[0] + self.size[0] - self.size[2],
                                    self.coordinates[1] + self.size[1]),

                                   (self.coordinates[0] + self.size[0] - self.size[2],
                                    self.coordinates[1] + self.size[2]),

                                   (self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                    self.coordinates[1] + self.size[2] * 2),

                                   (self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                    self.coordinates[1] + self.size[1] - self.size[2]),

                                   (self.coordinates[0] + self.size[2],
                                    self.coordinates[1] + self.size[1] - self.size[2]),

                                   (self.coordinates[0] + self.size[2], self.coordinates[1])),
                                   outline=self.colors[3], fill=self.colors[0])
        # Polygon 2
        self.canvas.create_polygon(((self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                     self.coordinates[1] + self.size[1] - self.size[2]),

                                    (self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                     self.coordinates[1] + self.size[1] - self.size[2] * 2),

                                    (self.coordinates[0] + self.size[2] * 2,
                                     self.coordinates[1] + self.size[1] - self.size[2] * 2),

                                    (self.coordinates[0] + self.size[2],
                                     self.coordinates[1] + self.size[1] - self.size[2]),

                                    (self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                     self.coordinates[1] + self.size[1] - self.size[2])
                                    ),
                                   outline=self.colors[3], fill=self.colors[2])
        # Polygon 3
        self.canvas.create_polygon(((self.coordinates[0] + self.size[2] * 2,
                                     self.coordinates[1] + self.size[2]),

                                    (self.coordinates[0] + self.size[0] - self.size[2],
                                     self.coordinates[1] + self.size[2]),

                                    (self.coordinates[0] + self.size[0] - self.size[2] * 2,
                                     self.coordinates[1] + self.size[2] * 2),

                                    (self.coordinates[0] + self.size[2] * 2,
                                     self.coordinates[1] + self.size[2] * 2)),
                                   outline=self.colors[3], fill=self.colors[2])
        # Polygon 4
        self.canvas.create_polygon(((self.coordinates[0] + self.size[0] - self.size[2],
                                     self.coordinates[1] + self.size[1]),

                                    (self.coordinates[0] + self.size[0] - self.size[2],
                                     self.coordinates[1] + self.size[2]),

                                    (self.coordinates[0] + self.size[2] * 2,
                                     self.coordinates[1] + self.size[2]),

                                    (self.coordinates[0] + self.size[2] * 2,
                                     self.coordinates[1] + self.size[1] - self.size[2] * 2),

                                    (self.coordinates[0] + self.size[2],
                                     self.coordinates[1] + self.size[1] - self.size[2]),

                                    (self.coordinates[0] + self.size[2], self.coordinates[1]),

                                    (self.coordinates[0] + self.size[0], self.coordinates[1]),

                                    (self.coordinates[0] + self.size[0],
                                     self.coordinates[1] + self.size[1] - self.size[2])
                                    ), outline=self.colors[3], fill=self.colors[1])


# Тест 1
def test1():
    """
    Рисуем большой невозможный квадрат (280х280х50) на черном холсте,
    размером 290х290. Цвета квадрата: стандартные.
    """
    tk = Tk()
    ucanvas = Canvas(tk, width=290, height=290, bg='black')
    ucanvas.pack()

    s = ImpossibleSquare(ucanvas, (5, 5), size=(280, 280, 50))
    s.draw()
    print("Big square, total polygons: 1*%s = %s" % (ImpossibleSquare.POLYGONS, ImpossibleSquare.POLYGONS))

    tk.mainloop()


# Тест 2
def test2():
    """
    Рисуем много (3844) маленьких (размер 16х16х3) невозможных квадратов на черном холсте,
    размером 1000х1000. Цвета квадратов: стандартные.
    ВНИМАНИЕ! Может загружаться долго на компьютерах с низкой производительностью.
    """
    tk = Tk()
    ucanvas = Canvas(tk, width=1000, height=1000, bg='black')
    ucanvas.pack()

    for row in range(int(1000/16)):
        for col in range(int(1000/16)):
            s = ImpossibleSquare(ucanvas, (3 + 16 * col, 3 + 16 * row), size=(16, 16, 3))
            s.draw()
    print("3844 small squares, total polygons: 3844*%s = %s" % (ImpossibleSquare.POLYGONS,
                                                                3844*ImpossibleSquare.POLYGONS))

    tk.mainloop()


if __name__ == '__main__':
    test1()
    test2()

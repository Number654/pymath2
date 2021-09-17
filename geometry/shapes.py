# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from math import pi, sin, cos, sqrt

from core.pymath import average


class Shape(ABC):
    name = "shape"

    def __init__(self, width, height):
        self.w = width
        self.h = height

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.name)

    @classmethod
    @abstractmethod
    def area(cls):
        pass

    @classmethod
    @abstractmethod
    def perimeter(cls):
        pass


class Angle:
    name = "angle"

    def __init__(self, angle):
        self.angle = angle

        if 0 < self.angle < 90:
            self.type = "sharp"
        if self.angle == 90:
            self.type = "right"
        if 90 < self.angle < 180:
            self.type = "obtuse"
        if self.angle == 180:
            self.type = "straight"
        if 180 < self.angle < 360:
            self.type = "concave"
        if self.angle >= 360:
            self.type = "full"

    def __str__(self):
        return "Angle %s degrees, %s" % (self.angle, self.type)

    def __repr__(self):
        return str(self.__str__())

    def change_angle(self, new_angle):
        self.__init__(new_angle)


class Line:
    name = "line"

    def __init__(self, points=None):
        if points is None:
            points = {}
        self.points = points

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return str(self.name.capitalize())

    def add_point(self, letter, x):
        self.points[letter] = x

    def remove_point(self, letter):
        self.points.pop(letter)


class Segment:
    name = "segment"

    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return self.name.capitalize() + " at X1: %s; X2: %s; Y1: %s; Y2: %s" % (self.x1, self.x2,
                                                                                self.y1, self.y2)

    def __repr__(self):
        return str(self.__str__())

    def get_length(self):
        return sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

    def get_center(self):
        return average([(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2])


class Ray:
    name = "ray"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.name.capitalize() + ", start point: %s; %s" % (self.x, self.y)

    def __repr__(self):
        return str(self.__str__())


class Ellipse(Shape, ABC):
    name = "ellipse"

    def area(self):
        return pi * self.w * self.h

    def perimeter(self):
        return pi * (self.w + self.h)

    # Найти координаты точки на окружности
    # Примечание: угол следует указывать В РАДИАНАХ
    # x = w * cos(fi)
    # y = h * sin(fi)
    def point(self, angle):
        return self.w * cos(angle), self.h * sin(angle)


class Circle(Ellipse):

    def __init__(self, d):
        super().__init__(d, d)
        self.radius = d / 2

    def chord(self, angle):
        return self.w * sin(angle / 2)  # self.w = диаметр


class RegularPolygon(Shape, ABC):
    name = "regular_polygon"

    def __init__(self, side_length, sides):
        self.sides = sides
        self.side_length = side_length
        self.circle_radius = self.side_length / (2 * sin(pi / self.sides))
        self.angle = (180 * (self.sides-2)) / self.sides

        super().__init__(self.circle_radius, self.circle_radius)

    # S = 1/2 * R**2 * n * sin(360/n)
    def area(self):
        return 1/2 * self.circle_radius**2 * self.sides * sin(360/self.sides)

    def perimeter(self):
        return self.side_length * self.sides


class IrregularPolygon(Shape, ABC):
    name = "irregular_polygon"

    def __init__(self, points):
        self.points = [Segment(v[0], points[i+1][0],
                               v[1],
                               points[i+1][1]) for i, v in enumerate(points[:-1])]
        self.points.append(Segment(points[-2][0], points[-1][0],
                                   points[-2][1], points[-1][1]))
        super().__init__(None, None)

    def area(self):
        pass

    def perimeter(self):
        return sum((seg.get_length() for seg in self.points))

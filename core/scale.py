# -*- coding: utf-8 -*-

from .fractions import Fraction
from .numeric_system import Length, convert  # Ни в коем случае не удалять эту строку!


DISTANCE_ABBREVIATIONS = {"nanometers": "nm", "micrometers": "um",
                          "microns": "um", "millimeters": "mm",
                          "centimeters": "cm", "decimeters": "dm",
                          "meters": "m", "kilometers": "km",
                          "yards": "yd", "foots": "ft",
                          "inches": "IN", "miles": "mi"}


class Scale:

    def __init__(self, scale):
        self.scale = scale
        self.on_image = self.scale.split(":")[0]  # Размер на изображении
        self.real = self.scale.split(":")[1]  # Размер в действительности

    def __str__(self):
        return self.scale

    def __repr__(self):
        return str(self.scale)

    # Перевести отношение расстояние на изображении к расстоянию в действительности в виде
    # дроби в тип Scale
    @staticmethod
    def from_ratio(on_image, real):
        f = Fraction("%s/%s" % (on_image, real)).format_to_improper_fraction().reduce()
        return Scale("%s:%s" % (f.numerator, f.denominator))

    # Перевести масштаб в обыкновенную дробь
    def to_fraction(self):
        return Fraction("%s/%s" % (self.on_image, self.real))

    # Масштаб вида m:n в удобный для чтения строковый вид: in  m  centimeters  n  kilometers
    def to_string(self, real_distance_unit):
        convert_method = "convert(Length.CENTIMETERS_TO_%s, %s)" % (real_distance_unit.upper(), self.real)
        abbreviated_real_distance_unit = DISTANCE_ABBREVIATIONS[real_distance_unit]
        return "in 1 cm %s %s" % (eval(convert_method), abbreviated_real_distance_unit)

    # Расстояние на изображении по известному расстоянию в действительности
    def get_on_image(self, real_distance):
        # Расстояние нужно дать в сантиметрах. После вычислений
        # результата будет дан в этой же единице измерения
        return real_distance * self.to_fraction()

    # Расстояние в действительности по известному расстоянию на изображении
    def get_real(self, distance_on_image):
        # Расстояние нужно дать в сантиметрах. После вычислений
        # результата будет дан в этой же единице измерения
        return Fraction(distance_on_image) / self.to_fraction()

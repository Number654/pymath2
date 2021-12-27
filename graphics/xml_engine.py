# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree, Element, SubElement, ParseError
from PIL import Image, ImageDraw, ImageFont, ImageColor
from .canvas_object import CanvasObject

# Допустимые типы фигур: прямоугольник, линия, круг (эллипс)
acceptable_figure_types = ['rectangle', 'line', 'circle', 'text']


class GeometryDrawingError(Exception):
    pass


# Функция действует как enumerate, только если аргумент не итерируется, то возвращает его с номером 0.
def new_enumerate(iterable):
    return [(0, iterable)] if not hasattr(iterable, "__iter__") else enumerate(iterable)


def draw_text(draw, coords, text, fill=(0, 0, 0, 0), size=10, bold=False, italic=False, underline=False):
    name = "verdana%s.ttf" % ("b" if bold and not italic else ("i" if italic and not bold else
                                                               (
                                                                 "z" if bold and italic else "")))  # Имя файла шрифта
    font_obj = ImageFont.truetype(font=name, size=size)
    if underline:
        w, h = draw.textsize(text, font=font_obj)
        lx, ly = coords[0], coords[1] + h
        draw.line((lx, ly, lx+w, ly), fill=fill, width=2)

    draw.text(coords, text=text, font=font_obj, fill=fill)


def get_figures(source):
    # Открываем .gd файл (Geometry Drawing)
    f = ElementTree(file=source)
    # Получаем корневую секцию
    root = f.getroot()
    # Получаем все фигуры
    root_children = list(list(root)[1])
    cell_size = float(list(root)[0].attrib["cellsize"])
    # Сюда будут сохраняться данные о фигруах из файла
    # В виде объектов CanvasObject
    figures = []
    # Проходимся по фигурам
    for figure in root_children:
        # Получаем атрибуты фигуры: ее имя и тип
        figure_options = figure.attrib
        # Если тип фигуры, указанный в .gd файле не соотвествует допустимым типам, то кидаем ошибку
        if figure_options['type'].lower() not in acceptable_figure_types:
            raise GeometryDrawingError('An error in .gd file: unacceptable figure type: "%s"' % figure_options['type'])
        # Сюда будут сохраняться координаты точек фигуры
        figure_coords = []
        for coord in list(figure):
            figure_coords.append(float(coord.text))
        # Создаем объект CanvasObject, передаем в него все данные фигуры
        canvas_obj = CanvasObject(figure_options['type'], figure_coords)
        canvas_obj.kwargs = figure_options
        # Добавляем в список данных о фигурах объект CanvasObject
        figures.append(canvas_obj)
    return figures, cell_size


def save_figures(figures, cell_size):
    
    # Создаем корень .gd файла
    root = Element('content')
    # Метаданные (содержат размер клеток)
    metadata = SubElement(root, 'meta', attrib={"cellsize": str(cell_size)})
    # Подэлемент, содержащий все фигуры
    drawing = SubElement(root, 'drawing')

    # Проходимся по всем фигурам для сохранения
    for figure in figures:
        # Формируем словарь "правильных" аттрибутов
        valid_attributes = {'type': figure.figure, 'name': figure.kwargs['name'],
                            'fill': figure.kwargs['fill'], "width": str(figure.kwargs["width"])}
        if 'outline' in figure.kwargs.keys():
            valid_attributes['outline'] = figure.kwargs['outline']
        # Если фигура - текст:
        if figure.figure == "text":
            valid_attributes["text"] = figure.kwargs["text"]
            valid_attributes["font"] = figure.kwargs["font"]
            valid_attributes["size"] = str(figure.kwargs["size"])
            valid_attributes["bold"] = str(figure.kwargs["bold"])
            valid_attributes["italic"] = str(figure.kwargs["italic"])
            valid_attributes["underline"] = str(figure.kwargs["underline"])
        # Создаем подэлемент, указываем имя, тип фигуры, цвет линии и цвет заливки
        sub = SubElement(drawing, 'figure', attrib=valid_attributes)
        for n, coord in new_enumerate(figure.args[0]):
            coord_elem = SubElement(sub, 'coord%s' % n)
            coord_elem.text = str(coord)
            n += 1

    # Возвращаем XML-код в виде объекта Element
    return root


# Список фигур (и их атрибутов) в PNG-изображение
def figures2png(figures, path):
    # Создаем PNG-файл
    image = Image.new("RGBA", (586, 394), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Проходимя по фигурам
    for figure in figures:
        # Если у фигуры нет заливки (заливка прозрачная), то ставим полную прозрачность
        if not figure.kwargs['fill']:
            fill = (0, 0, 0, 0)
        # Иначе, ставим нужную заливку
        else:
            fill = ImageColor.getcolor(figure.kwargs['fill'], "RGBA")

        outline = figure.kwargs['outline']
        # Если линия, рисуем линию по координатам
        # figure.args - это координаты
        # figure.figure - это тип фигуры
        if figure.figure == "line":
            draw.line(xy=figure.args[0], fill=figure.kwargs["outline"], width=round(figure.kwargs["width"]))
        # Если прямоугольник, то рисуем прямоугольник без заливки по координатам
        if figure.figure == "rectangle":
            draw.rectangle(xy=figure.args[0], fill=fill, outline=outline, width=round(figure.kwargs["width"]))
        if figure.figure == "circle":
            draw.ellipse(xy=figure.args[0], fill=fill, outline=outline, width=round(figure.kwargs["width"]))
        if figure.figure == "text":
            draw_text(draw, figure.args[0], figure.kwargs["text"], fill=fill, size=figure.kwargs["size"],
                      bold=figure.kwargs["bold"], italic=figure.kwargs["italic"],
                      underline=figure.kwargs["underline"])
    # Сохраняем изображение
    del draw
    image.save(path, "PNG")


# Запись XML в файл
def write_to_file(xml, to_file):
    # Создаем файл, записываем в него то, что получилось
    my_tree = ElementTree(xml)
    my_tree.write(to_file)

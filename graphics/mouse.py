# -*- coding: utf-8 -*-


def post_cell(x, cellsize=18.8787):
    # Половина клетки
    half_of_cell = cellsize / 2.0
    cells_and_pixels = divmod(x, cellsize)

    if cells_and_pixels[1] >= half_of_cell:
        return (cells_and_pixels[0] + 1) * cellsize
    else:
        return cells_and_pixels[0] * cellsize

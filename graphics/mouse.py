# -*- coding: utf-8 -*-

from core.pymath import better_divmod


def post_cell(x, cellsize=18.8787):
    # Половина клетки
    half_of_cell = cellsize / 2.0
    cells_and_pixels = better_divmod(x, cellsize)

    if cells_and_pixels[1] > half_of_cell:
        return (cells_and_pixels[0] + 1) * cellsize
    return cells_and_pixels[0] * cellsize

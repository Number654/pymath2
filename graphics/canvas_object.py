# -*- coding: utf-8 -*-


class CanvasObject:

    def __init__(self, figure, *args, **kwargs):
        self.figure = figure
        self.args = args
        self.kwargs = kwargs

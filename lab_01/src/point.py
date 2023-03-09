from errors import *


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.x

    def rotate(self, rotate_centre, angle) -> int:
        """Угол angle представляется в радианах"""

        if len(rotate_centre) != 2:
            return ERR

        self.x = x_c + (self.x - x_c) * cos(angle) + (self.y - y_c) * sin(angle)
        self.y = y_c - (self.x - x_c) * sin(angle) + (self.y - y_c) * cos(angle)

        return SUCCESS

    def scale(self, scale_centre, coef_data) -> int:
        """Кортеж coef_data задается двумя элементами kx и ky"""

        if len(coef_data) != 2:
            return

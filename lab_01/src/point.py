from errors import *
from math import *


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def set_x(self, x) -> None:
        self.x = x

    def set_y(self, y) -> None:
        self.y = y

    # def rotate(self, rotate_centre, angle) -> int:
    #     """Угол angle представляется в радианах"""
    #
    #     if len(rotate_centre) != 2:
    #         return ERR_TUPLE_LEN
    #
    #     x_c = rotate_centre[0]
    #     y_c = rotate_centre[1]
    #
    #     self.x = x_c + (self.x - x_c) * cos(angle) + (self.y - y_c) * sin(angle)
    #     self.y = y_c - (self.x - x_c) * sin(angle) + (self.y - y_c) * cos(angle)
    #
    #     return SUCCESS
    #
    # def scale(self, scale_centre, coef_data) -> int:
    #     """Кортеж coef_data задается двумя элементами kx и ky"""
    #
    #     if len(coef_data) != 2:
    #         return ERR_TUPLE_LEN
    #
    #     k_x = coef_data[0]
    #     k_y = coef_data[1]
    #
    #     if k_x == 0 or k_y == 0:
    #         return ERR_SCALE_COEF
    #
    #     x_c = scale_centre[0]
    #     y_c = scale_centre[1]
    #
    #     self.x = k_x * self.x + x_c * (1 - k_x)
    #     self.y = k_y * self.y + y_c * (1 - k_y)
    #
    #     return SUCCESS
    #
    # def shift(self, dx, dy) -> None:
    #     self.x = self.x + dx
    #     self.y = self.y + dy


if __name__ == '__main__':
    exit(0)

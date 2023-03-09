from errors import *
from line import Line, get_line_by_points
from math import *
from point import Point


def get_points_distance(point_1, point_2) -> float:
    """Получение расстояния между двумя точками (теорема Пифагора)."""

    return sqrt((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2)


def get_line_concurrence_point(conc_point, line_1, line_2) -> int:
    """Получение точки пересечения двух прямых, заданных общими уравнениями,
    путем решения системы из 2-ух уравнений."""

    a_1 = line_1.x_coef
    b_1 = line_1.x_coef
    c_1 = line_1.const_term

    a_2 = line_2.x_coef
    b_2 = line_2.x_coef
    c_2 = line_2.const_term

    if a_1 == 0:
        return ERR_LINE_COEF

    if b_2 - b_1 / a_1 * a_2 == 0:
        return ERR_NO_CONCUR

    conc_y = (c_2 - c_1 / a_1 * a_2) / (b_2 - b_1 / a_1 * a_2)
    conc_x = c_1 / a_1 - (b_1 / a_1) * conc_y

    conc_point.set_x(conc_x)
    conc_point.set_y(conc_y)

    return SUCCESS


def get_normal_scalar(line):
    return sqrt(line.x_coef ** 2 + line.y_coef ** 2)


def get_angle_between_lines(line_1, line_2):
    """Получение угла между двумя прямыми (в градусах)."""

    norm_1 = get_normal_scalar(line_1)
    norm_2 = get_normal_scalar(line_2)

    angle_cos = (line_1.x_coef * line_2.x_coef + line_1.y_coef * line_2.y_coef) / (norm_1 * norm_2)

    return degrees(acos(angle_cos))


def get_angle_between_lines_by_points(angular_point_0, point_1, point_2):
    """Получение угла между двумя прямыми с вершиной в точке angular_point_0."""

    line_1 = get_line_by_points(angular_point_0, point_1)
    line_2 = get_line_by_points(angular_point_0, point_2)

    return get_angle_between_lines(line_1, line_2)

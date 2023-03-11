from linalg import *
from line import Line, get_line_by_points
from point import Point


class Triangle(object):
    """Вершины A, B, C; особый угол в градусах"""

    def __init__(self, point_a, point_b, point_c):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.unique_angle = 0.
        self.unique_angle_point = Point(0, 0)
        self.median_point = Point(0, 0)
        self.bisector_point = Point(0, 0)

    def set_min_angle_unique_data(self):
        abc_median_p = get_median_point(self.point_a, self.point_c)  # self.point_b,
        cab_median_p = get_median_point(self.point_b, self.point_c)  # self.point_a,
        bca_median_p = get_median_point(self.point_b, self.point_a)  # self.point_c,

        abc_bisect_p = get_bisector_point(self.point_b, self.point_a, self.point_c)
        cab_bisect_p = get_bisector_point(self.point_a, self.point_b, self.point_c)
        bca_bisect_p = get_bisector_point(self.point_c, self.point_b, self.point_a)

        abc_unique_angle = get_angle_between_lines_by_points(self.point_b, abc_median_p, abc_bisect_p)
        cab_unique_angle = get_angle_between_lines_by_points(self.point_b, cab_median_p, cab_bisect_p)
        bca_unique_angle = get_angle_between_lines_by_points(self.point_b, bca_median_p, bca_bisect_p)

        if abc_unique_angle <= cab_unique_angle:
            if abc_unique_angle <= bca_unique_angle:
                self.unique_angle = abc_unique_angle
                self.set_bisect_point(abc_bisect_p)
                self.set_median_point(abc_median_p)
                self.unique_angle_point = self.point_b

        if cab_unique_angle <= abc_unique_angle:
            if cab_unique_angle <= bca_unique_angle:
                self.unique_angle = cab_unique_angle
                self.set_bisect_point(cab_bisect_p)
                self.set_median_point(cab_median_p)
                self.unique_angle_point = self.point_a

        if bca_unique_angle <= cab_unique_angle:
            if bca_unique_angle <= abc_unique_angle:
                self.unique_angle = bca_unique_angle
                self.set_bisect_point(bca_bisect_p)
                self.set_median_point(bca_median_p)
                self.unique_angle_point = self.point_c

    def get_bisector_line(self):
        return get_line_by_points(self.unique_angle_point, self.bisector_point)

    def get_median_line(self):
        return get_line_by_points(self.unique_angle_point, self.median_point)

    def set_median_point(self, point):
        self.median_point.set_x(point.get_x())
        self.median_point.set_y(point.get_y())

    def set_bisect_point(self, point):
        self.bisector_point.set_x(point.get_x())
        self.bisector_point.set_y(point.get_y())

    def get_bisector_point(self):
        return self.bisector_point

    def get_median_point(self):
        return self.median_point

    def get_unique_angle(self):
        return self.unique_angle


def is_triangle(point_a, point_b, point_c) -> bool:
    """Проверка трех точек на составление треугольника."""

    side_ab = get_points_distance(point_a, point_b)
    side_bc = get_points_distance(point_b, point_c)
    side_ac = get_points_distance(point_a, point_c)

    sum_ab_bc = side_ab + side_bc
    sum_ab_ac = side_ab + side_ac
    sum_bc_ac = side_bc + side_ac

    if side_ac > sum_ab_bc or side_bc > sum_ab_ac or side_ab > sum_bc_ac:
        return False

    return True


def get_bisector_point(angular_point_0, point_1, point_2) -> Point:
    # """Получение координат основания биссектрисы треугольника, исходящей из точки angular_point_0."""
    #
    # # Прямые, сод. точки 0 и 1, 0 и 2
    # line_0_1 = get_line_by_points(angular_point_0, point_1)
    # line_0_2 = get_line_by_points(angular_point_0, point_2)
    #
    # # Модули векторов нормалей к прямым, сод. точки 0 и 1, 0 и 2
    # scalar_norm_0_1 = get_normal_scalar(line_0_1)
    # scalar_norm_0_2 = get_normal_scalar(line_0_2)
    #
    # # Коэффициенты в общем уравнении прямой, содержащей биссектрису (вывод из уравнения биссектрисы)
    # bisec_x_coef = scalar_norm_0_2 * line_0_1.x_coef - scalar_norm_0_1 * line_0_2.x_coef
    # bisec_y_coef = scalar_norm_0_2 * line_0_1.y_coef - scalar_norm_0_1 * line_0_2.y_coef
    # bisec_const_term = scalar_norm_0_2 * line_0_1.const_term - scalar_norm_0_1 * line_0_2.const_term
    # bisector_line = Line((bisec_x_coef, bisec_y_coef, bisec_const_term))
    #
    # # Координата точки биссектрисы, лежащей напротив вершины угла
    # line_1_2 = get_line_by_points(point_1, point_2)
    #
    # bisec_point = Point(0, 0)
    # rc = get_line_concurrence_point(bisec_point, bisector_line, line_1_2)
    #
    # if rc != SUCCESS:
    #     return angular_point_0

    # Тогда, так как биссектриса внутреннего угла треугольника делит противоположную сторону в отношении,
    # равном отношению двух прилежащих сторон (теорема о биссектрисе),

    return bisec_point


# def get_height_point(angular_point_0, point_1, point_2) -> Point:
#     """Получение координат основания высоты треугольника, исходящей из точки angular_point_0."""
#
#     line_1_2 = get_line_by_points(point_1, point_2)
#     height_line_const_term = -angular_point_0.x * line_1_2.x_coef - angular_point_0.y * line_1_2.y_coef
#     height_line = Line((line_1_2.x_coef, line_1_2.y_coef, height_line_const_term))
#
#     height_point = Point(0, 0)
#     rc = get_line_concurrence_point(height_point, height_line, line_1_2)
#
#     if rc != SUCCESS:
#         return angular_point_0
#
#     return height_point

def get_median_point(point_1, point_2):
    x_med = (point_1.get_x() + point_2.get_x()) / 2
    y_med = (point_1.get_y() + point_2.get_y()) / 2

    return Point(x_med, y_med)

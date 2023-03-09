class Line(object):
    """Информация о прямой, заданной уравнением: Ax + By + C = 0."""

    def __init__(self, tuple_of_coef):
        self.x_coef = tuple_of_coef[0]
        self.y_coef = tuple_of_coef[1]
        self.const_term = tuple_of_coef[2]


def get_line_by_points(point_1, point_2) -> Line:
    """Создание объекта Line по координатам двух точек."""

    x_coef = point_2.y - point_1.y
    y_coef = point_1.x - point_2.x
    const_term = point_1.y * point_2.x - point_1.x * point_2.y

    return Line((x_coef, y_coef, const_term))


if __name__ == '__main__':
    exit(0)

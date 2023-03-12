from tkinter import *
from tkinter import Menu, Label, Entry, Button, messagebox, Listbox, Frame, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from point import Point
from random import uniform
from triangle import *

INCHES_CONST = 96


def show_info():
    messagebox.showinfo(title="Информация о задаче 33",
                        message="[33]\nНа плоскости дано множество точек.\n"
                                "Найти такой треугольник с вершинами в этих точках, у которого угол,"
                                " образовавнный медианой и биссектрисой, исходящими из этой вершины, минимален."
                                "\nВывести изображение в графическом режиме")


class MyTriangle(Triangle):

    def __init__(self, points, indexes):
        super(MyTriangle, self).__init__(points[0], points[1], points[2])
        self.indexes = indexes


class Root(Tk):
    """Main window"""

    def __init__(self):
        super(Root, self).__init__()

        # Variables
        self.height = 600
        self.width = 1750
        self.points = []
        self.canvas, self.axis = None, None
        self.x_coord_var, self.y_coord_var, self.del_index_var = StringVar(), StringVar(), StringVar()
        self.status_contents = StringVar()
        self.padding = {'padx': 15, 'pady': 3}
        self.last_action = {'action': "", 'point_index': -1, 'point': Point(0, 0)}
        self.result_triangle = None
        self.result_var = StringVar()

        # Font
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Courier", size=15)

        # Window
        self.set_window_settings()

        # Frames
        self.frames = {}
        self.set_frames()

        # Fields
        self.fields = {}
        self.set_fields()

        self.pack_frames()

    def set_fields(self):
        self.set_matplotlib_canvas()
        self.set_point_entries()
        self.set_index_entry()
        self.set_points_listbox()
        self.set_buttons()
        self.set_decoration_labels()
        self.set_result_label()
        self.set_status_label()
        self.canvas_draw()
        self.reset_last_action()
        self.set_menubar()

    def set_window_settings(self):
        self.title("Computer Graphics: Lab #01")
        self.minsize(self.width, self.height)
        self.resizable(width=False, height=False)

    def set_frames(self):
        self.frames['action_frame'] = Frame(self)
        self.frames['add_frame'] = Frame(self.frames['action_frame'])
        self.frames['del_frame'] = Frame(self.frames['action_frame'])
        self.frames['extra_frame'] = Frame(self.frames['action_frame'])
        self.frames['res_frame'] = Frame(self.frames['action_frame'])
        self.frames['canvas_frame'] = Frame(self)
        self.frames['listbox_frame'] = Frame(self)

    def exit_app_choice(self):
        self.update_status_label("Выход из приложения...")
        answer = messagebox.askokcancel("Подтверждение выхода", "Завершить работу приложения?")

        if answer is None:
            self.destroy()
        else:
            self.update_status_label("Выход отменен")

    def set_menubar(self):
        self.fields['menubar'] = Menu(self)
        self.config(menu=self.fields['menubar'])

        self.fields['menubar'].add_command(label="Инфо о задаче", command=lambda: show_info())
        self.fields['menubar'].add_command(label="Выход", command=lambda: self.exit_app_choice())

    def set_matplotlib_canvas(self):
        """Настройка поля отрисовки"""

        figure = plt.Figure(figsize=(5.5, 5.5), dpi=100)
        axis = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, self.frames['canvas_frame'])
        self.fields['canvas'] = canvas.get_tk_widget()
        self.canvas = canvas
        self.axis = axis

    def draw_axis(self):
        """Отрисовка осей"""

        self.axis.spines['left'].set_position('zero')
        self.axis.spines['right'].set_visible(False)
        self.axis.spines['bottom'].set_position('zero')
        self.axis.spines['top'].set_visible(False)

        self.axis.xaxis.set_ticks_position('bottom')
        self.axis.yaxis.set_ticks_position('left')
        self.axis.plot(1, 0, ls="", marker=">", ms=10, color="k",
                       transform=self.axis.get_yaxis_transform(), clip_on=False)
        self.axis.plot(0, 1, ls="", marker="^", ms=10, color="k",
                       transform=self.axis.get_xaxis_transform(), clip_on=False)

    def draw_points(self):
        """Отрисовка точек с подписями"""

        if len(self.points) > 0:
            self.axis.scatter([p.get_x() for p in self.points], [p.get_y() for p in self.points], c="black")
            self.axis.scatter(self.points[len(self.points) - 1].get_x(),
                              self.points[len(self.points) - 1].get_y(), c="red")

            i = 0

            for p in self.points:
                i += 1
                text_x, text_y = p.x, p.y  # self.get_random_near_point(p.x, p.y, 0.01)
                self.axis.text(text_x, text_y, f"{i}: ({p.get_x():.3f};{p.get_y():.3f})\n", va='center', ha='center')

    def draw_result_triangle(self):
        x = [self.result_triangle.point_a.get_x(),
             self.result_triangle.point_b.get_x(),
             self.result_triangle.point_c.get_x()]
        y = [self.result_triangle.point_a.get_y(),
             self.result_triangle.point_b.get_y(),
             self.result_triangle.point_c.get_y()]

        unique_x = [self.result_triangle.unique_angle_point.get_x(),
                    self.result_triangle.median_point.get_x(),
                    self.result_triangle.bisector_point.get_x()]
        unique_y = [self.result_triangle.unique_angle_point.get_y(),
                    self.result_triangle.median_point.get_y(),
                    self.result_triangle.bisector_point.get_y()]

        self.axis.scatter(x, y, c="black")
        self.axis.scatter(unique_x, unique_y, c="red")

        # triangle
        self.axis.plot([x[0], x[1]], [y[0], y[1]], c="black")
        self.axis.plot([x[1], x[2]], [y[1], y[2]], c="black")
        self.axis.plot([x[0], x[2]], [y[0], y[2]], c="black")

        # median
        self.axis.plot([unique_x[0], unique_x[1]], [unique_y[0], unique_y[1]], c="blue")

        # Bisector
        self.axis.plot([unique_x[0], unique_x[2]], [unique_y[0], unique_y[2]], c="green")

        for i in range(len(x)):
            self.axis.text(x[i], y[i], f"{self.result_triangle.indexes[i] + 1}: "
                                       f"({x[i]:.3f};{y[i]:.3f})\n", va='center', ha='center')

        self.axis.text(unique_x[1], unique_y[1], f"M: ({unique_x[1]:.3f};{unique_y[1]:.3f})",
                       va='top', ha='center')
        self.axis.text(unique_x[2], unique_y[2], f"D: ({unique_x[2]:.3f};{unique_y[2]:.3f})",
                       va='top', ha='center')

        self.set_triangle_canvas_scaling(x, y)

    def set_triangle_canvas_scaling(self, new_x, new_y):
        self.axis.set_aspect('auto')
        x_shift = (max(new_x) - min(new_x)) / 4
        y_shift = (max(new_y) - min(new_y)) / 4

        self.axis.set_xlim(min(new_x) - x_shift, max(new_x) + x_shift)
        self.axis.set_ylim(min(new_y) - y_shift, max(new_y) + y_shift)

    def canvas_draw(self, draw_points=True, draw_triangle=False):
        """Отрисовка объектов"""

        self.axis.clear()

        if draw_points:
            self.draw_points()

        if draw_triangle:
            self.draw_result_triangle()

        self.axis.grid()
        self.draw_axis()
        self.canvas.draw()

    def check_point_entries(self):
        if self.fields['x_entry'].index("end") == 0 or self.fields['y_entry'].index("end") == 0:
            return False

        x = self.fields['x_entry'].get()
        y = self.fields['y_entry'].get()

        try:
            float(x)
        except ValueError:
            return False

        try:
            float(y)
        except ValueError:
            return False

        return True

    def clear_point_entries(self):
        self.fields['x_entry'].delete(0, END)
        self.fields['y_entry'].delete(0, END)

    def clear_index_entry(self):
        self.fields['ind_entry'].delete(0, END)

    def add_point_by_index(self, index, new_point):
        self.points.append(Point(0, 0))

        for i in range(len(self.points) - 1, index, -1):
            self.points[i].set_x(self.points[i - 1].get_x())
            self.points[i].set_y(self.points[i - 1].get_y())

        self.points[index].set_x(new_point.get_x())
        self.points[index].set_y(new_point.get_y())

        self.update_points_listbox()
        self.canvas_draw()

    def add_point(self):
        """Добавление точки в список, тектовое окно, отрисовка"""

        if not self.check_point_entries():
            messagebox.showerror("Ошибка ввода", "Координатами должны быть вещественные числа")
            self.clear_point_entries()
            return

        new_point = Point(float(self.fields['x_entry'].get()), float(self.fields['y_entry'].get()))
        self.add_point_by_index(len(self.points), new_point)
        self.update_last_action("add", len(self.points) - 1, new_point)
        self.update_status_label(f"Добавлена точка: ({new_point.x:.3f}; {new_point.y:.3f})")

    def set_buttons(self):
        """Создание кнопок"""

        self.fields['add_button'] = Button(self.frames['add_frame'], text="+ Добавить",
                                           command=lambda: self.add_point())
        self.fields['del_button'] = Button(self.frames['del_frame'], text="- Удалить №",
                                           command=lambda: self.delete_point())
        self.fields['del_last_button'] = Button(self.frames['del_frame'], text="- Послед.",
                                                command=lambda: self.delete_point(last=True))
        self.fields['cancel_button'] = Button(self.frames['extra_frame'], text="Отменить",
                                              command=lambda: self.undo_last_action())
        self.fields['clear_button'] = Button(self.frames['extra_frame'], text="Очистить",
                                             command=lambda: self.delete_all_points())
        self.fields['res_button'] = Button(self.frames['res_frame'], text="Получить результат",
                                           command=lambda: self.get_result_triangle())

    def insert_listbox_separator(self):
        self.fields['listbox'].insert(END, f"|-----|-----|-----|")

    def insert_listbox_heading(self):
        self.fields['listbox'].insert(END, "|- № -|- x -|- y -|")
        self.insert_listbox_separator()

    def insert_listbox_info(self, i, x, y):
        self.fields['listbox'].insert(END, f"|{i:^5}|{x:^5.3f}|{y:^5.3f}|")

    def set_points_listbox(self):
        """Настройка текстового списка точек"""

        self.fields['listbox'] = Listbox(self.frames['listbox_frame'])
        self.insert_listbox_heading()

    def update_points_listbox(self):
        """Обновление текстового списка точек"""

        self.fields['listbox'].delete(first=0, last=END)
        self.insert_listbox_heading()

        for i in range(len(self.points)):
            curr_x = self.points[i].get_x()
            curr_y = self.points[i].get_y()
            self.insert_listbox_info(i + 1, curr_x, curr_y)
            self.insert_listbox_separator()

    def delete_point_by_index(self, index) -> tuple:
        deleted = Point(self.points[index].get_x(), (self.points[index].get_y()))

        for i in range(index, len(self.points) - 1):
            self.points[i].set_x(self.points[i + 1].get_x())
            self.points[i].set_y(self.points[i + 1].get_y())

        self.points.pop()
        self.update_points_listbox()
        self.canvas_draw()

        return deleted.get_x(), deleted.get_y()

    def check_index_entry(self):
        if self.fields['ind_entry'].get() == "":
            return False

        i = self.fields['ind_entry'].get()

        try:
            int(i)
        except ValueError:
            return False

        return True

    def delete_all_points(self):
        if len(self.points) == 0:
            messagebox.showerror("Ошибка удаления", "Список точек пуст")
            return

        while len(self.points) != 0:
            self.delete_point(last=True)

        self.update_status_label("Удаление всех точек")

    def delete_point(self, last=False):
        """Удаление точки из списка, текстового списка, отрисовка"""

        if len(self.points) == 0:
            messagebox.showerror("Ошибка удаления", "Список точек пуст")
            return

        index = len(self.points) - 1

        if not last:
            if not self.check_index_entry():
                messagebox.showerror("Ошибка удаления", "Индексом должно быть целое число")
                self.clear_index_entry()
                return

            index = int(self.fields['ind_entry'].get())

            if index <= 0 or index > len(self.points):
                messagebox.showerror("Ошибка удаления", "Индекс выходит за границы списка")
                return

            index -= 1

        x, y = self.delete_point_by_index(index)
        deleted = Point(x, y)
        self.update_last_action("del", index, deleted)
        self.update_status_label(f"Удалена точка: {index + 1} ({deleted.x:.3f}; {deleted.y:.3f})")

    def set_point_entries(self):
        self.fields['x_entry'] = Entry(self.frames['add_frame'], textvariable=self.x_coord_var,
                                       font=self.defaultFont, justify=RIGHT)
        self.fields['y_entry'] = Entry(self.frames['add_frame'], textvariable=self.y_coord_var,
                                       font=self.defaultFont, justify=RIGHT)

    def set_index_entry(self):
        self.fields['ind_entry'] = Entry(self.frames['del_frame'], textvariable=self.del_index_var,
                                         font=self.defaultFont, justify=RIGHT)

    def set_status_label(self):
        self.fields['status_label'] = Label(self.frames['canvas_frame'])
        self.fields['status_label']['textvariable'] = self.status_contents
        self.update_status_label("Ожидание...")

    def update_status_label(self, text):
        self.status_contents.set(text)

    def update_last_action(self, action_type, index, point):
        self.last_action['action'] = action_type
        self.last_action['point_index'] = index
        self.last_action['point'].set_x(point.x)
        self.last_action['point'].set_y(point.y)

    def reset_last_action(self):
        self.update_last_action("", -1, Point(0, 0))

    def set_result_label(self):
        self.fields['res_label'] = Label(self.frames['res_frame'], borderwidth=2, relief="solid", justify=LEFT)
        self.fields['res_label']['textvariable'] = self.result_var
        self.result_var.set("Тут появится результат вычислений")

    def update_result_label(self, text):
        self.result_var.set(text)

    def undo_last_action(self):
        if self.last_action['action'] == "":
            messagebox.showerror("Ошибка отмены", "Возможна отмена ровно одного совершенного добавления или удаления")
            return

        if self.last_action['action'] == "add":
            self.delete_point_by_index(self.last_action['point_index'])
            self.update_status_label("Отмена добавления точки")

        if self.last_action['action'] == "del":
            self.add_point_by_index(self.last_action['point_index'], self.last_action['point'])
            self.update_status_label("Отмена удаления точки")

        self.reset_last_action()

    def set_decoration_labels(self):
        self.fields['x_label'] = Label(self.frames['add_frame'], text="X:", justify=RIGHT)
        self.fields['y_label'] = Label(self.frames['add_frame'], text="Y:", justify=RIGHT)
        self.fields['ind_label'] = Label(self.frames['del_frame'], text="№:", justify=RIGHT)

    def pack_add_frame(self):
        self.fields['x_label'].pack(**self.padding, side="left", expand=True, fill=X)
        self.fields['x_entry'].pack(**self.padding, side="left")
        self.fields['y_label'].pack(**self.padding, side="left", expand=True, fill=X)
        self.fields['y_entry'].pack(**self.padding, side="left")
        self.fields['add_button'].pack(**self.padding, side="left", expand=True, fill=X)

    def pack_del_frame(self):
        self.fields['ind_label'].pack(**self.padding, side="left", fill=X)
        self.fields['ind_entry'].pack(**self.padding, side="left")
        self.fields['del_button'].pack(**self.padding, side="left", expand=True, fill=X)
        self.fields['del_last_button'].pack(**self.padding, side="left", expand=True, fill=X)

    def pack_extra_frame(self):
        self.fields['cancel_button'].pack(**self.padding, side="left", fill=X, expand=True)
        self.fields['clear_button'].pack(**self.padding, side="left", fill=X, expand=True)

    def pack_res_frame(self):
        self.fields['res_button'].pack(**self.padding, side="left", fill=BOTH)
        self.fields['res_label'].pack(**self.padding, side="left", fill=BOTH, expand=True)

    def pack_canvas_frame(self):
        self.fields['canvas'].pack(**self.padding, fill=BOTH, expand=True)
        self.fields['status_label'].pack(**self.padding, fill=BOTH, expand=True)

    def pack_listbox_frame(self):
        self.fields['listbox'].pack(**self.padding, expand=True, fill=BOTH)

    def pack_action_frame(self):
        self.pack_add_frame()
        self.pack_del_frame()
        self.pack_extra_frame()
        self.pack_res_frame()

        self.frames['add_frame'].pack(fill=BOTH)
        self.frames['del_frame'].pack(fill=BOTH)
        self.frames['extra_frame'].pack(fill=BOTH)
        self.frames['res_frame'].pack(fill=BOTH, expand=True)

    def pack_frames(self):
        self.pack_action_frame()
        self.pack_canvas_frame()
        self.pack_listbox_frame()

        self.frames['action_frame'].pack(side="left", fill=BOTH)
        self.frames['canvas_frame'].pack(side="left", fill=BOTH)
        self.frames['listbox_frame'].pack(side="left", expand=True, fill=BOTH)

    #  РЕШЕНИЕ ЗАДАЧИ
    def get_all_triangles(self, triangles):
        n = len(self.points)

        for point_1_ind in range(n):
            point_1 = self.points[point_1_ind]

            for point_2_ind in range(point_1_ind + 1, n):
                point_2 = self.points[point_2_ind]

                for point_3_ind in range(point_2_ind + 1, n):
                    point_3 = self.points[point_3_ind]

                    if is_triangle(point_1, point_2, point_3):
                        triangles.append(MyTriangle([point_1, point_2, point_3],
                                                    [point_1_ind, point_2_ind, point_3_ind]))
                        triangles[len(triangles) - 1].set_min_angle_unique_data()

    def get_result_triangle(self):
        if len(self.points) < 3:
            self.update_result_label("Невозможно получить решение")
            messagebox.showerror(title="Ошибка решения",
                                 message="Невозможно получить решение - НЕДОСТАТОЧНО ТОЧЕК")
            return

        all_triangles = []
        self.get_all_triangles(all_triangles)

        if len(all_triangles) == 0:
            self.update_result_label("Невозможно получить решение")
            messagebox.showerror(title="Ошибка решения",
                                 message="Невозможно получить решение - ВЫРОЖДЕННЫЙ СЛУЧАЙ")
            return

        min_angle = all_triangles[0].unique_angle
        self.result_triangle = all_triangles[0]

        for triangle in all_triangles:
            if triangle.unique_angle < min_angle:
                min_angle = triangle.unique_angle
                self.result_triangle = triangle

        self.canvas_draw(draw_points=True, draw_triangle=True)
        self.update_result_label(f"Найденный треугольник состоит из вершин:\n"
                                 f"\t{self.result_triangle.indexes[0] + 1}, "
                                 f"{self.result_triangle.indexes[1] + 1}, "
                                 f"{self.result_triangle.indexes[2] + 1}\n"
                                 f"Угол между высотой и биссектрисой:\n"
                                 f"\t> {self.result_triangle.unique_angle:.3f} град.\n"
                                 f"Координаты:\n"
                                 f"\t> основания медианы M: ({self.result_triangle.median_point.get_x():.3f};"
                                 f" {self.result_triangle.median_point.get_y():.3f})\n"
                                 f"\t> основания биссектрисы D: ({self.result_triangle.bisector_point.get_x():.3f}"
                                 f"; {self.result_triangle.bisector_point.get_y():.3f})\n"
                                 f"\t> вершины угла - ({self.result_triangle.unique_angle_point.get_x():.3f};"
                                 f" {self.result_triangle.unique_angle_point.get_y():.3f})\n")


def main():
    root = Root()
    root.mainloop()


if __name__ == '__main__':
    main()

from tkinter import *
from tkinter import messagebox, filedialog, Label, Entry, Button, messagebox, LAST, Listbox, Frame, font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from point import Point
from time import sleep

INCHES_CONST = 100


class Root(Tk):
    """Main window"""

    def __init__(self):
        super(Root, self).__init__()

        # Font
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Courier",
                                   size=15)

        self.title("Computer Graphics: Lab #01")

        self.height = 800
        self.width = 1600

        self.minsize(self.width, self.height)
        self.resizable(width=False, height=False)

        self.content = Frame(self)
        self.frame = Frame(self.content, borderwidth=5, relief="ridge",
                           width=self.width, height=self.height)

        self.cols = 8
        self.rows = 15

        self.last_action = ["", -1, Point(0, 0)]

        self.points = []
        self.points_listbox = None
        self.set_points_listbox()

        self.buttons = []
        self.set_buttons()
        self.canvas, self.axis = self.set_matplotlib_canvas()

        self.x_coord_var, self.y_coord_var, self.del_index = StringVar(), StringVar(), StringVar()
        self.entries = []
        self.set_point_entries()
        self.set_index_entry()

        self.status_label = None
        self.status_contents = StringVar()
        self.set_status_label()
        self.update_status_label("Ожидание...")

        self.set_grid_configures()

        self.canvas_draw()

    def set_matplotlib_canvas(self):
        """Настройка поля отрисовки"""

        figure = Figure(figsize=(self.width // (2 * INCHES_CONST),
                                 self.height // (2 * INCHES_CONST)), dpi=100)
        axis = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(row=0, column=4, sticky=NSEW, columnspan=self.cols // 2, rowspan=self.rows)

        return canvas, axis

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
            self.axis.scatter([p.x for p in self.points], [p.y for p in self.points], c="purple")
            self.axis.scatter(self.points[len(self.points) - 1].x,
                              self.points[len(self.points) - 1].y, c="pink")

            i = 0

            for p in self.points:
                i += 1
                self.axis.text(p.x, p.y, f"{i}\n", va='bottom', ha='center')

    def canvas_draw(self, draw_points=True, draw_triangle=False):
        """Отрисовка объектов"""

        self.axis.clear()

        if draw_points:
            self.draw_points()

        self.axis.grid()
        self.draw_axis()
        self.axis.autoscale()
        self.canvas.draw()

    def entries_have_numbers(self):
        if self.entries[0].index("end") == 0 or self.entries[1].index("end") == 0:
            return False

        x = self.entries[0].get()
        y = self.entries[1].get()

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
        self.entries[0].delete(0, END)
        self.entries[1].delete(0, END)

    def clear_index_entry(self):
        self.entries[2].delete(0, END)

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

        if not self.entries_have_numbers():
            messagebox.showerror("Ошибка ввода", "Координатами должны быть вещественные числа")
            self.clear_point_entries()
            return

        new_point = Point(float(self.entries[0].get()), float(self.entries[1].get()))
        self.add_point_by_index(len(self.points), new_point)
        self.update_last_action("add", len(self.points) - 1, new_point)
        self.update_status_label(f"Добавлена точка: ({new_point.x}; {new_point.y})")

    def set_buttons(self):
        """Настройка кнопок"""

        self.buttons.append(Button(self, text="Добавить",
                            command=lambda: self.add_point()))
        self.buttons.append(Button(self, text="Удалить по индексу",
                                   command=lambda: self.delete_point()))
        self.buttons.append(Button(self, text="Отмена",
                                   command=lambda: self.undo_last_action()))
        self.buttons.append(Button(self, text="Удалить последнюю",
                            command=lambda: self.delete_point(last=True)))
        self.buttons.append(Button(self, text="Получить результат",
                                   command=lambda: print("")))

        self.buttons[0].grid(row=1, column=0, sticky=NSEW, columnspan=2, padx=15, pady=15)
        self.buttons[1].grid(row=2, column=0, sticky=NSEW, columnspan=1, padx=15, pady=15)
        self.buttons[2].grid(row=3, column=0, sticky=NSEW, columnspan=1, padx=15, pady=15)
        self.buttons[3].grid(row=3, column=1, sticky=NSEW, columnspan=1, padx=15, pady=15)
        self.buttons[4].grid(row=4, column=0, sticky=NSEW, columnspan=2, padx=15, pady=15)

    def set_grid_configures(self):
        """Настройка разметки окна"""

        self.columnconfigure(0, weight=1)

        for col in range(0, self.cols // 2):
            self.columnconfigure(col, weight=1)
            self.columnconfigure(col + self.cols // 2, weight=1)

        for row in range(self.rows):
            self.grid_rowconfigure(row, weight=1)

    def set_points_listbox(self):
        """Настройка текстового списка точек"""

        self.points_listbox = Listbox(self)
        self.points_listbox.grid(row=0, column=2, columnspan=self.cols // 4, rowspan=self.rows,
                                 sticky=NSEW, padx=10, pady=10)
        self.points_listbox.insert(END, "|- № -|- x -|- y -|")
        self.points_listbox.insert(END, f"|-----|-----|-----|")

    def update_points_listbox(self):
        """Обновление текстового списка точек"""

        self.points_listbox.delete(first=0, last=END)
        self.points_listbox.insert(END, "|- № -|- x -|- y -|")
        self.points_listbox.insert(END, f"|-----|-----|-----|")

        for i in range(len(self.points)):
            self.points_listbox.insert(END, f"|{i + 1:^5}|{self.points[i].get_x():^5}|{self.points[i].get_y():^5}|")
            self.points_listbox.insert(END, f"|-----|-----|-----|")

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
        if self.entries[2].get() == "":
            return False

        i = self.entries[0].get()

        try:
            int(i)
        except ValueError:
            return False

        return True

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

            index = int(self.entries[2].get())

            if index <= 0 or index > len(self.points):
                messagebox.showerror("Ошибка удаления", "Индекс выходит за границы списка")
                return

            index -= 1

        x, y = self.delete_point_by_index(index)
        deleted = Point(x, y)
        self.update_last_action("del", index, deleted)
        self.update_status_label(f"Удалена точка: {index + 1} ({deleted.x}; {deleted.y})")

    def set_point_entries(self):
        self.entries.append(Entry(self, textvariable=self.x_coord_var, font=("Courier", 18), justify=RIGHT))
        self.entries.append(Entry(self, textvariable=self.y_coord_var, font=("Courier", 18), justify=RIGHT))

        self.entries[0].grid(row=0, column=0, sticky=NSEW, padx=15, pady=15, rowspan=1, columnspan=1)
        self.entries[1].grid(row=0, column=1, sticky=NSEW, padx=15, pady=15, rowspan=1, columnspan=1)

    def set_index_entry(self):
        self.entries.append(Entry(self, textvariable=self.del_index, font=("Courier", 18), justify=RIGHT))
        self.entries[2].grid(row=2, column=1, sticky=NSEW, padx=15, pady=15, rowspan=1, columnspan=1)

    def set_status_label(self):
        self.status_label = Label(self)
        self.status_label['textvariable'] = self.status_contents
        self.status_label.grid(row=5, column=0, sticky=NSEW, padx=5, pady=5, rowspan=3, columnspan=2)

    def update_status_label(self, text):
        self.status_contents.set(text)

    def update_last_action(self, action_type, index, point):
        self.last_action[0] = action_type
        self.last_action[1] = index
        self.last_action[2].set_x(point.x)
        self.last_action[2].set_y(point.y)

    def undo_last_action(self):
        if self.last_action[0] == "":
            messagebox.showerror("Ошибка отмены", "Возможна отмена ровно одного совершенного действия")
            return

        if self.last_action[0] == "add":
            self.delete_point_by_index(self.last_action[1])
            self.update_status_label("Отмена добавления точки")

        if self.last_action[0] == "del":
            self.add_point_by_index(self.last_action[1], self.last_action[2])
            self.update_status_label("Отмена удаления точки")

        self.last_action[0] = ""
        self.last_action[1] = -1
        self.last_action[2].set_x(0)
        self.last_action[2].set_y(0)


if __name__ == '__main__':
    root = Root()
    root.mainloop()

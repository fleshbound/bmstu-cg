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
        self.rows = 8

        self.points = []
        self.points_listbox = None
        self.set_points_listbox()

        self.buttons = []
        self.set_buttons()
        self.canvas, self.axis = self.set_matplotlib_canvas()

        self.set_grid_configures()

        self.canvas_draw()

    def set_matplotlib_canvas(self):
        """Настройка поля отрисовки"""

        figure = Figure(figsize=(self.width // (2 * INCHES_CONST),
                                 self.height // (2 * INCHES_CONST)), dpi=100)
        axis = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, self)
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # canvas._tkcanvas.grid(row=1, column=0, sticky=NSEW, columnspan=4)
        canvas.get_tk_widget().grid(row=0, column=4, sticky=NSEW, columnspan=4, rowspan=8)

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

    def add_point(self):
        """Добавление точки в список, тектовое окно, отрисовка"""
        self.points.append(Point((10 - len(self.points)) * 20, (5 - len(self.points)) * 20))
        self.update_points_listbox()
        self.canvas_draw()

    def set_buttons(self):
        """Настройка кнопок"""

        self.buttons.append(Button(self, text="Test Button!",
                            command=lambda: self.add_point()).grid(row=0, column=0, sticky=EW))
        self.buttons.append(Button(self, text="Test Button!",
                            command=lambda: self.delete_point(len(self.points) - 1)).grid(row=7,
                                                                                          column=1, sticky=EW))
        #
        # for i in range(len(buttons)):
        #     buttons[i].grid(row=i, column=i, sticky=EW)

    def set_grid_configures(self):
        """Настройка разметки окна"""

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        for col in range(0, self.cols // 2):
            self.columnconfigure(col, weight=1)
            self.columnconfigure(col + self.cols // 2, weight=1)

        for row in range(self.rows):
            self.content.grid_rowconfigure(row, weight=1)

    def set_points_listbox(self):
        """Настройка текстового списка точек"""

        self.points_listbox = Listbox(self)
        self.points_listbox.grid(row=0, column=2, columnspan=2, rowspan=8,
                                 sticky=NSEW, padx=10, pady=10)
        self.points_listbox.insert(END, "|- № -|- x -|- y -|")
        self.points_listbox.insert(END, f"|-----|-----|-----|")

    def update_points_listbox(self):
        """Обновление текстового списка точек"""

        self.points_listbox.delete(first=0, last=END)
        self.points_listbox.insert(END, "|- № -|- x -|- y -|")
        self.points_listbox.insert(END, f"|-----|-----|-----|")

        for i in range(len(self.points)):
            self.points_listbox.insert(END, f"|{i + 1:^5}|{self.points[i].x:^5}|{self.points[i].y:^5}|")
            self.points_listbox.insert(END, f"|-----|-----|-----|")

    def delete_point(self, index):
        if len(self.points) == 0:
            messagebox.showerror("Ошибка удаления", "Список точек пуст")
            return

        for i in range(index, len(self.points) - 1):
            self.points[i].set_x(self.points[i + 1].get_x)
            self.points[i].set_y(self.points[i + 1].get_y)

        self.points.pop()
        self.update_points_listbox()
        self.canvas_draw()


if __name__ == '__main__':
    root = Root()
    root.mainloop()

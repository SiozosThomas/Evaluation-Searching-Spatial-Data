import sys

class Selection_Queries():

    def __init__(self):
        if len(sys.argv) != 5:
            print("Something wrong with command line arguments!")
            exit()
        self.x_low = float(sys.argv[1])
        self.x_high = float(sys.argv[2])
        self.y_low = float(sys.argv[3])
        self.y_high = float(sys.argv[4])
        if self.x_low > self.x_high:
            print("x_low should be smaller or equal than x_high. Try Again!")
            exit()
        if self.y_low > self.y_high:
            print("y_low should be smaller or equal than y_high. Try Again!")
            exit()
        self.cells = []
        self.x_axis_cells = []
        self.y_axis_cells = []
        print("Give me path for grid(dir): ")
        path = input()
        self.read_grid_dir(path)
        self.count = 0

    def read_grid_dir(self, path):
        first_line = True
        new_lines = 0
        with open(path, encoding = "utf8") as file:
            for line in file:
                line_split = line.split()
                if first_line:
                    x_min = float(line_split[0])
                    x_max = float(line_split[1])
                    y_min = float(line_split[2])
                    y_max = float(line_split[3])
                    first_line = False
                else:
                    self.cells.append({"x": float(line_split[0]),\
                                    "y": float(line_split[1]),\
                                    "start": float(line_split[2]),\
                                    "length": float(line_split[3]),\
                                    "new_lines": int(new_lines)})
                    new_lines += int(float(line_split[3]))
        self.create_grid(x_min, x_max, y_min, y_max)

    def create_grid(self, x_min, x_max, y_min, y_max):
        x_cell = x_max - x_min
        y_cell = y_max - y_min
        for i in range(0, 11):
            self.x_axis_cells.append(round(x_min + i * x_cell / 10, 6))
            self.y_axis_cells.append(round(y_min + i * y_cell / 10, 6))
        print(self.x_axis_cells)
        print(self.y_axis_cells)
        self.show_window()

    def show_window(self):
        x_low_border, x_high_border, y_low_border, y_high_border =\
                                self.get_windows_borders()
        grid_grd = open("grid.grd", "r")
        window = open("window.txt", "w", encoding = "utf-8")
        if x_low_border == -1: x_low_border = 0
        if x_high_border == 11: x_high_border = 10
        if y_low_border == -1: y_low_border = 0
        if y_high_border == 11: y_high_border = 10
        for i in range(x_low_border, x_high_border + 1):
            for j in range(y_low_border, y_high_border + 1):
                find = self.find_which_cell(i, j)
                if find != -1:
                    if i == x_low_border:
                        self.x_low_edge(grid_grd, find, j, y_high_border,
                                                                    window)
                    elif i == x_high_border:
                        self.x_high_edge(grid_grd, find, j, y_high_border,
                                                                    window)
                    else:
                        if j == y_low_border:
                            self.y_low_edge(grid_grd, find, i, x_high_border,
                                                                    window)
                        elif j == y_high_border:
                            self.y_high_edge(grid_grd, find, i, x_high_border,
                                                                    window)
                        else:
                            self.inside_window(grid_grd, find, window)
        window.close()
        grid_grd.close()

    def get_windows_borders(self):
        x_low_border = self.get_window_low_border(self.x_low, self.x_axis_cells)
        if x_low_border != -2:
            x_high_border = self.get_window_high_border(self.x_high,
                                                            self.x_axis_cells)
        else:
            print("Window(x axis) out of grid limits!")
            exit()
        y_low_border = self.get_window_low_border(self.y_low, self.y_axis_cells)
        if y_low_border != -2:
            y_high_border = self.get_window_high_border(self.y_high,
                                                            self.y_axis_cells)
        else:
            print("Window(y axis) out of grid limits!")
            exit()
        return x_low_border, x_high_border, y_low_border, y_high_border

    def get_window_low_border(self, low, axis):
        for i in range(0, 10):
            if low >= axis[i] and low < axis[i+1]:
                return i
        if low <= axis[0]:
            return -1
        return -2

    def get_window_high_border(self, high, axis):
        for i in range(0, 10):
            if high >= axis[i] and high < axis[i+1]:
                return i
        if high >= axis[10]:
            return 11
        return -2

    def find_which_cell(self, x, y):
        for i in range(0, len(self.cells)):
            if x == self.cells[i]["x"] and y == self.cells[i]["y"]:
                return i
        return -1

    def x_low_edge(self, grid_grd, find, j, y_high_border, window):
        grid_grd.seek(int(self.cells[find]["start"]) +\
                                self.cells[find]["new_lines"])
        for i in range(0, int(self.cells[find]["length"])):
            line = grid_grd.readline()
            coordinates = line.split()
            print(coordinates)
            if float(coordinates[1]) >= self.x_low and\
                float(coordinates[2]) >= self.y_low:
                if j == y_high_border:
                    if float(coordinates[2]) <= self.y_high:
                        window.write(line)
                else:
                    window.write(line)

    def x_high_edge(self, grid_grd, find, j, y_high_border, window):
        grid_grd.seek(int(self.cells[find]["start"]) +\
                                self.cells[find]["new_lines"])
        for i in range(0, int(self.cells[find]["length"])):
            line = grid_grd.readline()
            coordinates = line.split()
            if float(coordinates[1]) <= self.x_high and\
                float(coordinates[2]) >= self.y_low:
                if j == y_high_border:
                    if float(coordinates[2]) <= self.y_high:
                        window.write(line)
                else:
                    window.write(line)

    def y_low_edge(self, grid_grd, find, i, x_high_border, window):
        grid_grd.seek(int(self.cells[find]["start"]) +\
                                self.cells[find]["new_lines"])
        for i in range(0, int(self.cells[find]["length"])):
            line = grid_grd.readline()
            coordinates = line.split()
            if float(coordinates[1]) >= self.x_low and\
                float(coordinates[2]) >= self.y_low:
                if i == x_high_border:
                    if float(coordinates[1]) <= self.x_high:
                        window.write(line)
                else:
                    window.write(line)

    def y_high_edge(self, grid_grd, find, i, x_high_border, window):
        grid_grd.seek(int(self.cells[find]["start"]) +\
                                self.cells[find]["new_lines"])
        for i in range(0, int(self.cells[find]["length"])):
            line = grid_grd.readline()
            coordinates = line.split()
            if float(coordinates[1]) >= self.x_low and\
                float(coordinates[2]) <= self.y_high:
                if i == x_high_border:
                    if float(coordinates[1]) <= self.x_high:
                        window.write(line)
                else:
                    window.write(line)

    def inside_window(self, grid_grd, find, window):
        grid_grd.seek(int(self.cells[find]["start"]) +\
                        self.cells[find]["new_lines"])
        for k in range(0, int(self.cells[find]["length"])):
            window.write(grid_grd.readline())

select = Selection_Queries()

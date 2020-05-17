import sys
import math

class NN_Search():

    def __init__(self):
        if len(sys.argv) != 4:
            print("Something wrong with command line arguments!")
            exit()
        self.q = {"x": float(sys.argv[1]), "y": float(sys.argv[2])}
        self.k = int(sys.argv[3])
        self.cells = []
        self.previous_cells = []
        self.x_axis_cells = []
        self.y_axis_cells = []
        self.queue = []
        print("Give me path for grid(dir): ")
        path = input()
        cells_information = Cells_Information(path)
        self.cells = cells_information.get_cells()
        self.x_axis_cells = cells_information.get_x_axis_cells()
        self.y_axis_cells = cells_information.get_y_axis_cells()
        if not self.x_axis_cells[0] <= self.q["x"] <=\
                self.x_axis_cells[len(self.x_axis_cells) - 1]:
            print("Point not in grid. Try again!")
            exit()
        if not self.y_axis_cells[0] <= self.q["y"] <=\
                self.y_axis_cells[len(self.y_axis_cells) - 1]:
            print("Point not in grid. Try again!")
            exit()

    def get_k(self):
        return self.k

    def show_k_nearest_points(self):
        count = 0
        cell = self.find_which_cell(self.q)
        self.insert_arround_cells_in_queue(cell)
        points_on_cell = self.open_cell(cell)
        sorted_points_on_cell = self.sort_points_by_distance(points_on_cell)
        for i in range(0, len(sorted_points_on_cell)):
            self.process_queue(sorted_points_on_cell[i])
        while count < self.k:
            self.sort_queue()
            if self.check_cell_or_point(self.queue[0]) == 0:
                self.insert_arround_cells_in_queue(self.queue[0])
                points_on_cell = self.open_cell(self.queue[0])
                sorted_points_on_cell =\
                        self.sort_points_by_distance(points_on_cell)
                self.process_queue(0)
                for i in range(0, len(sorted_points_on_cell)):
                    self.process_queue(sorted_points_on_cell[i])
            elif self.check_cell_or_point(self.queue[0]) == 1:
                point = self.queue[0]
                self.process_queue(0)
                self.k += 1
                yield point

    def find_which_cell(self, point):
        find_i = -1
        find_j = -1
        for i in range(0, 10):
            for j in range(0, 10):
                if self.x_axis_cells[i] <= point["x"] < self.x_axis_cells[i+1]:
                    if self.y_axis_cells[j] <= point["y"]\
                                            < self.y_axis_cells[j+1]:
                        find_j = j
                        break
            if find_j != -1:
                find_i = i
                break
        self.previous_cells.append({"x": find_i, "y": find_j})
        return {"x": find_i, "y": find_j}

    def insert_arround_cells_in_queue(self, cell):
        x = cell["x"]
        y = cell ["y"]
        x_minus_one = False
        x_plus_one = False
        if x - 1 >= 0:
            x_minus_one = True
        if x + 1 >= 0:
            x_plus_one = True
        if y - 1 >= 0:
            cell = {"x": x, "y": y - 1}
            if not self.check_same_cells(cell):
                self.previous_cells.append(cell)
                self.process_queue(cell)
            if x_minus_one:
                for i in range(y - 1, y + 1):
                    cell = {"x": x - 1, "y": i}
                    if not self.check_same_cells(cell):
                        self.process_queue(cell)
                        self.previous_cells.append(cell)
            if x_plus_one:
                for i in range(y - 1, y + 1):
                    cell = {"x": x + 1, "y": i}
                    if not self.check_same_cells(cell):
                        self.process_queue(cell)
                        self.previous_cells.append(cell)
        if y + 1 < 10:
            cell = {"x": x, "y": y + 1}
            if not self.check_same_cells(cell):
                self.process_queue(cell)
                self.previous_cells.append(cell)
            if x_minus_one:
                cell = {"x": x - 1, "y": y + 1}
                if not self.check_same_cells(cell):
                    self.process_queue(cell)
                    self.previous_cells.append(cell)
            if x_plus_one:
                cell = {"x": x + 1, "y": y + 1}
                if not self.check_same_cells(cell):
                    self.process_queue(cell)
                    self.previous_cells.append(cell)

    def open_cell(self, cell):
        grid_grd = open("grid.grd", "r", encoding = "utf-8")
        find = -1
        for i in range(0, len(self.cells)):
            if cell["x"] == self.cells[i]["x"] and\
                cell["y"] == self.cells[i]["y"]:
                find = i
                break
        points_on_cell = []
        if find != -1:
            grid_grd.seek(int(self.cells[find]["start"]) +\
                                self.cells[find]["new_lines"])
            for i in range(0, int(self.cells[find]["length"])):
                line = grid_grd.readline()
                coordinates = line.split()
                points_on_cell.append({"identifier": coordinates[0],\
                                "x": float(coordinates[1]),\
                                "y": float(coordinates[2])})
        else:
            print("Didn't find cell to open!")
            grid_grd.close()
            exit()
        grid_grd.close()
        return points_on_cell

    def sort_points_by_distance(self, points_on_cell):
        for i in range(0, len(points_on_cell)):
            points_on_cell[i]["distance"] =\
                            self.get_euclidean_distance(points_on_cell[i])
        points_on_cell = sorted(points_on_cell, key = lambda k: k['distance'])
        return points_on_cell

    def process_queue(self, x):
        if x == 0:
            self.queue.pop(0)
        else:
            self.queue.append(x)

    def sort_queue(self):
        for i in range(0, len(self.queue)):
            if self.check_cell_or_point(self.queue[i]) == 0:
                if len(self.queue[i]) == 2:
                    cell = self.queue[i]
                    points_on_cell = self.open_cell(cell)
                    sorted_points_on_cell =\
                                self.sort_points_by_distance(points_on_cell)
                    self.queue[i]["distance"] =\
                            float(sorted_points_on_cell[0]['distance'])
        self.queue = sorted(self.queue, key = lambda k: k['distance'])

    def check_cell_or_point(self, x):
        if len(x) in (2, 3):
            return 0
        elif len(x) == 4:
            return 1
        return -1

    def check_same_cells(self, cell):
        for i in range(0, len(self.previous_cells)):
            if self.previous_cells[i]["x"] == cell["x"] and\
                        self.previous_cells[i]["y"] == cell["y"]:
                return True
        return False

    def get_euclidean_distance(self, point):
        return math.sqrt((float(self.q["x"]) - float(point["x"])) ** 2 +\
                            (float(self.q["y"]) - float(point["y"])) ** 2)

class Cells_Information():

    def __init__(self, path):
        self.cells = []
        self.x_axis_cells = []
        self.y_axis_cells = []
        self.read_grid_dir(path)

    def get_cells(self):
        return self.cells

    def get_x_axis_cells(self):
        return self.x_axis_cells

    def get_y_axis_cells(self):
        return self.y_axis_cells

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

nn_search = NN_Search()
gen = nn_search.show_k_nearest_points()
k = nn_search.get_k()
output = open(str(k) + "nearest_points.txt", "w", encoding = "utf-8")
for i in range(0, k):
    point = next(gen)
    output.write(str(point))
    output.write("\n")
output.close()

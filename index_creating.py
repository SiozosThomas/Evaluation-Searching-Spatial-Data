class Index_creating():

    def __init__(self):
        print("Give me the path of data file: ")
        path = input()
        self.path = path
        self.identifiers = []
        self.sorted_points = []
        self.x_min = 100.0
        self.x_max = 0.0
        self.y_min = 200.0
        self.y_max = 0.0
        self.x_axis_cells = []
        self.y_axis_cells = []

    def create_the_index(self):
        self.read_data_file()
        self.create_grid()
        self.sorting_points()

    def read_data_file(self):
        identifier = 0
        with open(self.path, encoding = "utf8") as file:
            for line in file:
                coordinates = line.split()
                if len(coordinates) > 1:
                    self.set_identifiers(identifier, coordinates)
                    self.x_min = self.find_min(float(coordinates[0]),
                                                                self.x_min)
                    self.x_max = self.find_max(float(coordinates[0]),
                                                                self.x_max)
                    self.y_min = self.find_min(float(coordinates[1]),
                                                                self.y_min)
                    self.y_max = self.find_max(float(coordinates[1]),
                                                                self.y_max)
                identifier += 1

    def set_identifiers(self, identifier, coordinates):
        self.identifiers.append({ "identifier": identifier,\
                                    "x": float(coordinates[0]),\
                                    "y": float(coordinates[1])})

    def find_min(self, point, old_min):
        if point < old_min:
            return point
        return old_min

    def find_max(self, point, old_max):
        if point > old_max:
            return point
        return old_max

    def create_grid(self):
        x_cell = self.x_max - self.x_min
        y_cell = self.y_max - self.y_min
        for i in range(0, 11):
            self.x_axis_cells.append(self.x_min + i * x_cell / 10)
            self.y_axis_cells.append(self.y_min + i * y_cell / 10)

    def sorting_points(self):
        points_on_cells = {}
        check = 0
        for i in range(0, 10):
            for j in range(0, 10):
                points_on_cells["(" + str(i) + "," + str(j) + ")"] = ""
        for i in range(0, len(self.identifiers)):
            for j in range(0, len(self.x_axis_cells) - 1):
                if self.check_if_point_is_on_cell(self.identifiers[i]["x"],\
                    self.x_axis_cells[j], self.x_axis_cells[j+1]):
                    for k in range(0, len(self.y_axis_cells) - 1):
                        if self.check_if_point_is_on_cell\
                            (self.identifiers[i]["y"], self.y_axis_cells[k],\
                            self.y_axis_cells[k+1]):
                            points_on_cells["(" + str(j) + "," + str(k) +\
                                ")"] += " " +\
                                str(self.identifiers[i]["identifier"]) + " " +\
                                str("%.6f" % self.identifiers[i]["x"]) + " " +\
                                str("%.6f" % self.identifiers[i]["y"])
                            check = 1
                            break
                if check == 1:
                    check = 0
                    break
        self.write_grid_dir_file(points_on_cells)
        self.fill_sorted_points_list(points_on_cells)
        self.write_grid_grd_file()

    def check_if_point_is_on_cell(self, point, low, high):
        if point >= low and point < high:
            return True
        return False

    def write_grid_dir_file(self, points_on_cells):
        grid_dir = open("grid.dir", "w", encoding = "utf-8")
        grid_dir.write(" ".join([str("%.6f" % self.x_min),\
                            str("%.6f" % self.x_max),\
                            str("%.6f" % self.y_min),\
                            str("%.6f" % self.y_max)]) + "\n")
        chars = 0
        for i in range(0, 10):
            for j in range(0, 10):
                if len(points_on_cells["(" + str(i) + "," + str(j) +\
                        ")"]) != 0.0:
                    grid_dir.write(" ".join([str(i), str(j), str(chars),\
                                str(len(points_on_cells["(" + str(i) + ","\
                                + str(j) + ")"].split()) / 3)]) + "\n")
                    chars += len(points_on_cells["(" + str(i) + "," +\
                                        str(j) + ")"])
        grid_dir.close()

    def fill_sorted_points_list(self, points_on_cells):
        coor_list = []
        for i in range(0, 10):
            for j in range(0, 10):
                coordinates = points_on_cells["(" + str(i) +\
                                            "," + str(j) + ")"].split()
                for k in range(0, len(coordinates) - 2, 3):
                    coor_list.append({"identifier": int(coordinates[k]),\
                                "x": float(coordinates[k+1]),\
                                "y": float(coordinates[k+2])})
                for k in range(0, len(coor_list)):
                    self.sorted_points.append(coor_list[k])
                coor_list.clear()

    def write_grid_grd_file(self):
        grid_grd = open("grid.grd", "w", encoding = "utf-8")
        for i in range(0, len(self.sorted_points)):
            grid_grd.write(str(self.sorted_points[i]["identifier"]) + " ")
            grid_grd.write(str("%.6f" % self.sorted_points[i]["x"]) + " ")
            grid_grd.write(str("%.6f" % self.sorted_points[i]["y"]) + "\n")
        grid_grd.close()

index = Index_creating()
index.create_the_index()

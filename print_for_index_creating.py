    def print(self):
        print("X axis(min ---- max): ")
        print(str(self.x_min) + " ---- " + str(self.x_max))
        print("Y axis(min ---- max): ")
        print(str(self.y_min) + " ---- " + str(self.y_max))
        print(self.x_axis_cells)
        print(self.y_axis_cells)
        cells = open("cells.txt", "w", encoding = "utf-8")
        for i in range(0, len(self.x_axis_cells) - 1):
            for j in range(0, len(self.y_axis_cells) - 1):
                cells.write("(" + str(i) + "," + str(j) + ")\n")
                cells.write("Cell: \n(x_start ---- x_end)\n(y_start ---- y_end)\n")
                cells.write(str(self.x_axis_cells[i]) + " ---- " + str(self.x_axis_cells[i+1]) + "\n")
                cells.write(str(self.y_axis_cells[j]) + " ---- " + str(self.y_axis_cells[j+1]) + "\n")
        cells.close()
        identifiers = open("identifiers.txt", "w", encoding = "utf-8")
        for i in range(0, len(self.identifiers)):
            identifiers.write(str(i) + " " + str(self.identifiers[i]["x"]) + " " + str(self.identifiers[i]["y"]) + "\n")
        identifiers.close()
        grid_grd = open("grid.grd", "w", encoding = "utf-8")
        for i in range(0, len(self.sorted_points)):
            grid_grd.write(str(self.sorted_points[i]["identifier"]) + " ")
            grid_grd.write(str(self.sorted_points[i]["x"]) + " ")
            grid_grd.write(str(self.sorted_points[i]["y"]) + "\n")
        grid_grd.close()

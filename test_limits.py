min_x = 39.68009
max_x = 39.7300721
min_y = 116.070466
max_y = 116.1354169
path = input()
count = 0
line_count = 0
chars = 0
with open(path, encoding = 'utf8') as file:
    for line in file:
        coor = line.split()
        if float(coor[1]) >= min_x and float(coor[1]) < max_x:
            if float(coor[2]) >= min_y and float(coor[2]) < max_y:
                count += 1
                chars += len(line)
        if line_count == 108: break
        line_count += 1
print(count)
print(chars)

"""
FILE: sol.py
Solution to day 14 problems (27 & 28) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
VISUALISE = False
data = [x for x in open("Day 14/data.txt", "r").read().split("\n")]

##### Problem 27 #####
def change_grid(grid, coord, shift, symbol="#"):
    grid[coord[0] - shift[0]][coord[1] - shift[1]] = symbol

def get_grid(grid, coord, shift):
    return grid[coord[0] - shift[0]][coord[1] - shift[1]]

def out_of_bounds(coord, shift, maxpos):
    return coord[0] > maxpos[0] or coord[1] < shift[1] or coord[1] > maxpos[1]

data = [[(int(y.split(",")[1]), int(y.split(",")[0])) for y in x.split("->")] for x in data]
min_w = max_w = 500
min_h = max_h = 0
for path in data:
    for coord in path:
        min_w, max_w = min(min_w, coord[1]), max(max_w, coord[1])
        min_h, max_h = min(min_h, coord[0]), max(max_h, coord[0])
shift, maxpos = (min_h, min_w), (max_h, max_w)
size = (max_h - min_h + 1, max_w - min_w + 1)
grid = [['.'] * size[1] for i in range(size[0])]
for path in data:
    if len(path) == 1:
        change_grid(grid, (path[0][0], path[0][1]), shift)
        continue
    for i in range(len(path) - 1):
        prev, cur = path[i], path[i+1]
        for j in range(prev[0], cur[0], 1 if cur[0] > prev[0] else -1):
            change_grid(grid, (j, prev[1]), shift)
        for j in range(prev[1], cur[1], 1 if cur[1] > prev[1] else -1):
            change_grid(grid, (prev[0], j), shift)
        change_grid(grid, cur, shift)
copied = [[char for char in row] for row in grid]
rested = True
rest_count = 0
below = lambda coord: (coord[0]+1, coord[1])
belowleft = lambda coord: (coord[0]+1, coord[1]-1)
belowright = lambda coord: (coord[0]+1, coord[1]+1)
while rested: 
    rested = False
    sand_pos = (0, 500)
    while not (get_grid(grid, sand_pos, shift) == "O"):
        if out_of_bounds(below(sand_pos), shift, maxpos) or get_grid(grid, below(sand_pos), shift) == ".":
            sand_pos = below(sand_pos)
        elif out_of_bounds(belowleft(sand_pos), shift, maxpos) or get_grid(grid, belowleft(sand_pos), shift) == ".":
            sand_pos = belowleft(sand_pos)
        elif out_of_bounds(belowright(sand_pos), shift, maxpos) or get_grid(grid, belowright(sand_pos), shift) == ".":
            sand_pos = belowright(sand_pos)
        else:
            rested = True
            rest_count += 1
            change_grid(grid, sand_pos, shift, symbol="O")
        if out_of_bounds(sand_pos, shift, maxpos):
            rested = False
            break
if VISUALISE:
    print("\n".join(["".join(row) for row in grid]))
print("Problem 27:", rest_count)

##### Problem 28 ######

# TODO could improve runtime and eliminate board size increase complexity by making a hashmap of positions?
grid = copied + [['.'] * size[1],['#'] * size[1]]
size = (size[0] + 2, size[1])
maxpos = (maxpos[0] + 2, maxpos[1])
rested = True
rest_count = 0
while rested: 
    rested = False
    sand_pos = (0, 500)
    while not (get_grid(grid, sand_pos, shift) == "O"):
        if get_grid(grid, below(sand_pos), shift) == ".":
            sand_pos = below(sand_pos)
        elif sand_pos[0]+1 < maxpos[0] and (out_of_bounds(belowleft(sand_pos), shift, maxpos) or get_grid(grid, belowleft(sand_pos), shift) == "."):
            sand_pos = belowleft(sand_pos)
        elif sand_pos[0]+1 < maxpos[0] and (out_of_bounds(belowright(sand_pos), shift, maxpos) or get_grid(grid, belowright(sand_pos), shift) == "."):
            sand_pos = belowright(sand_pos)
        else:
            rested = True
            rest_count += 1
            change_grid(grid, sand_pos, shift, symbol="O")
        if out_of_bounds(sand_pos, shift, maxpos):
            sand_pos = (min(sand_pos[0], maxpos[0]-1), sand_pos[1])
            if sand_pos[1] < shift[1]:
                grid = [['.'] + row for row in grid]
                grid[-1][0] = '#'
                size = (size[0], size[1] + 1)
                shift = (shift[0], shift[1] - 1)
            elif sand_pos[1] > maxpos[1]:
                grid = [row + ['.'] for row in grid]
                grid[-1][-1] = '#'
                size = (size[0], size[1] + 1)
                maxpos = (maxpos[0], maxpos[1] + 1)
if VISUALISE:
    print("\n".join(["".join(row) for row in grid]))
print("Problem 28:", rest_count)

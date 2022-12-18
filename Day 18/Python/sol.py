"""
FILE: sol.py
Solution to day 18 problems (35 & 36) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = set([tuple([int(n) for n in x.strip().split(",")]) for x in open("Day 18/data.txt", "r").read().split("\n")])

##### Problem 35 #####
dirs = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
vec_sum = lambda xs, ys: (xs[0]+ys[0], xs[1]+ys[1], xs[2] + ys[2])
get_sa = lambda xs, ys, f: len([1 for c in xs for d in ys if f(vec_sum(c,d))])

print("Problem 35:", get_sa(data, dirs, lambda pos: pos not in data))

##### Problem 36 ######
# Find dimensions of bounding box for cubes, and FLOOD_FILL from a corner
end = (max([x[0] for x in data]) + 1, max([y[1] for y in data]) + 1, max([z[2] for z in data]) + 1)
start = (min([x[0] for x in data]) - 1, min([y[1] for y in data]) - 1, min([z[2] for z in data]) - 1)
vec_in_range = lambda xs, low, high: all([low[i] <= xs[i] <= high[i] for i in range(0,3)])
frontier, explored = [start], set([start])
while len(frontier) > 0:
    new_frontier = []
    for cube in frontier:
        for dir in dirs:
            check = vec_sum(cube, dir)
            if vec_in_range(check, start, end) and check not in explored and check not in data:
                new_frontier.append(check)
                explored.add(check)
    frontier = new_frontier
# Count only faces that touch flooded air blocks
print("Problem 36:", get_sa(data, dirs, lambda pos: pos in explored))

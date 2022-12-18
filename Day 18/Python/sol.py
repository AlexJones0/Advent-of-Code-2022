"""
FILE: sol.py
Solution to day 18 problems (35 & 36) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = set([tuple([int(n) for n in x.strip().split(",")]) for x in open("Day 18/data.txt", "r").read().split("\n")])

##### Problem 35 #####
dirs = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
vec_sum = lambda xs, ys: tuple([sum(x) for x in zip(xs,ys)])
print("Problem 35:", len([1 for c in data for d in dirs if vec_sum(c,d) not in data]))

##### Problem 36 ######s
end = (max([x[0] for x in data]) + 1, max([y[1] for y in data]) + 1, max([z[2] for z in data]) + 1)
start = (min([x[0] for x in data]) - 1, min([y[1] for y in data]) - 1, min([z[2] for z in data]) - 1)
frontier, new_frontier, explored, sa = [start], [], set([start]), 0
while len(frontier) > 0: # Flood fill in bounding box to find SA
    for (cube, dir) in ((c, d) for c in frontier for d in dirs):
        check = vec_sum(cube, dir)
        if all([start[i] <= check[i] <= end[i] for i in range(0,3)]) and check not in explored:
            if check in data:
                sa += 1; continue
            new_frontier.append(check)
            explored.add(check)
    frontier, new_frontier = new_frontier, []
print("Problem 36:", sa)

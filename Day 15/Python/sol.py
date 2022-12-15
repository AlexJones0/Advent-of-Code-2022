"""
FILE: sol.py
Solution to day 15 problems (29 & 30) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [(int(x.split("x=")[1].split(",")[0]),
         int(x.split("y=")[1].split(":")[0]),
         int(x.split("x=")[2].split(",")[0]),
         int(x.split("y=")[2].split("\n")[0])
        ) for x in open("Day 15/data.txt", "r").read().split("\n")]

##### Problem 29 #####
manhattan = lambda x1, y1, x2, y2: abs(x2-x1) + abs(y2-y1)
y_row = 2000000
s_range = {}
beacons = set()
for sensor_x, sensor_y, beacon_x, beacon_y in data:
    s_range[(sensor_x, sensor_y)] = manhattan(sensor_x, sensor_y, beacon_x, beacon_y)
    beacons.add((beacon_x, beacon_y))
count = 0
coverage = []
for sens_x, sens_y in s_range:
    dist = s_range[(sens_x, sens_y)] - abs(sens_y - y_row)
    if dist > -1:
        coverage.append((sens_x - dist, sens_x + dist))
coverage = sorted(coverage, key = lambda range: range[0])
solved_coverage = []
for i in range(len(coverage) - 1):
    if coverage[i][1] > coverage[i+1][1]:
        coverage[i+1] = coverage[i]
    elif coverage[i][1] >= coverage[i+1][0]:
        coverage[i+1] = (coverage[i][0], coverage[i+1][1])
    else:
        solved_coverage.append(coverage[i])
solved_coverage.append(coverage[-1])
for beacon_x, beacon_y in beacons:
    if beacon_y == y_row:
        for i, cover in enumerate(solved_coverage): # TODO could binary search to make this faster
            if cover[0] == beacon_x and cover[1] == beacon_x:
                solved_coverage = solved_coverage[:i] + solved_coverage[i+1:]
            elif cover[0] == beacon_x:
                solved_coverage[i] = (cover[0]+1, cover[1])
            elif cover[1] == beacon_x:
                solved_coverage[i] = (cover[0], cover[1]+1)
            elif cover[0] < beacon_x < cover[1]:
                solved_coverage = solved_coverage[:i] + [(cover[0], beacon_x-1), (beacon_x+1, cover[1])] + solved_coverage[i+1:]
            else:
                continue
            break
print("Problem 29:", sum([c[1] - c[0] + 1 for c in solved_coverage]))

##### Problem 30 ######
tuning_freq = lambda x, y: x * 4000000 + y
up_intercepts = set()
down_intercepts = set()
for x, y in s_range:
    range_ = s_range[(x,y)]
    up_intercepts.add(y+x+range_+1)
    up_intercepts.add(y+x-range_-1)
    down_intercepts.add(y-x+range_+1)
    down_intercepts.add(y-x-range_-1)
lower_bound = 0
upper_bound = 4000000
solution = (0, 0)
for c1 in up_intercepts:
    for c2 in down_intercepts:
        p = ((c1-c2)//2, (c1+c2)//2)
        if lower_bound <= p[0] <= upper_bound and lower_bound <= p[1] <= upper_bound and \
            len([1 for x, y in s_range if manhattan(p[0], p[1], x, y) <= s_range[(x,y)]]) == 0:
                solution = p
                break
print("Problem 30:", tuning_freq(*solution))

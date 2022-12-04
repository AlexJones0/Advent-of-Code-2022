"""
FILE: sol.py
Solution to day 4 problems (7 & 8) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 4/data.txt", "r").read().split("\n")]

##### Problem 7 #####

y = [(x.split(",")[0].split("-"), x.split(",")[1].split("-")) for x in data]
z = [x for x in y if int(x[0][0]) <= int(x[1][0]) and int(x[0][1]) >= int(x[1][1]) or \
                     int(x[1][0]) <= int(x[0][0]) and int(x[1][1]) >= int(x[0][1])]
print("Problem 7:", len(z))

##### Problem 8 #####
z = [x for x in y if int(x[0][0]) <= int(x[1][0]) and int(x[0][1]) >= int(x[1][0]) or \
                     int(x[1][0]) <= int(x[0][0]) and int(x[1][1]) >= int(x[0][0])]
print("Problem 8:", len(z))
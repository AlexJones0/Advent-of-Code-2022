"""
FILE: sol.py
Solution to day 1 problems (1 & 2) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 01/data.txt", "r").read().split("\n")]

##### Problem 1 #####

count = 0
max_ = 0
for item in data:
    if len(item) == 0:
        max_ = max(max_, count)
        count = 0
    else:
        count += int(item)
print("Problem 1:", max_)


##### Problem 2 #####

calcount = [0]
for item in data:
    if len(item) == 0:
        calcount.append(0)
    else:
        calcount[-1] += int(item)

print("Problem 2:", sum(sorted(calcount, reverse=True)[:3]))
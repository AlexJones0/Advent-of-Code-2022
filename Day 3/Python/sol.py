"""
FILE: sol.py
Solution to day 3 problems (5 & 6) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 3/data.txt", "r").read().split("\n")]

##### Problem 5 #####
x = [set(l[:len(l)//2]).intersection(set(l[len(l)//2:])) for l in data]
y = lambda x: sum(ord(c.lower()) - ord('a') + (27 if c.isupper() else 1) for (c,) in x)
print("Problem 5:", y(x))

##### Problem 6 #####
x = [set(data[i]).intersection(data[i+1]).intersection(data[i+2]) for i in range(0, len(data), 3)]
print("Problem 6:", y(x))
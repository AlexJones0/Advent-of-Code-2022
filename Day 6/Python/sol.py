"""
FILE: sol.py
Solution to day 6 problems (11 & 12) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 6/data.txt", "r").read().split("\n")][0]

##### Problem 11 #####
def f(n):
    prev = data[:(n-1)]
    for i, char in enumerate(data[(n-1):]):
        if char not in prev and len(set(list(prev))) == (n-1):
            y = i + n
            return y
        prev = prev[1:] + char

print("Problem 11:", f(4))

##### Problem 12 ######
print("Problem 12:", f(14))
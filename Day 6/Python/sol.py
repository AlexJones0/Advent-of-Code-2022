"""
FILE: sol.py
Solution to day 6 problems (11 & 12) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 6/data.txt", "r").read().split("\n")][0]

##### Problem 11 #####
def f(n):
    for i in range(0,len(data)-n+1):
        if len(set(data[i:i+n])) == n:
            return i+n-1

print("Problem 11:", f(4))

##### Problem 12 ######
print("Problem 12:", f(14))

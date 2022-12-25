"""
FILE: sol.py
Solution to day 25 problems (49 & 50) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 25/data.txt", "r").read().split("\n")]        

##### Problem 49 #####
# Horrible and janky left folding using summation and exponentiation
sum_, snafu = sum([sum([(['=','-','0','1','2'].index(item[len(item)-1-i]) - 2) * 5**i for i in range(len(item))]) for item in data]), ""
while sum_ > 0:
    snafu += ['0','1','2','=','-'][sum_ % 5]
    sum_ = sum_ // 5 + (1 if (sum_ % 5) > 2 else 0)
print("Problem 49:", snafu[::-1])

##### Problem 50 ######
print("Problem 50:", "Freebie :)")
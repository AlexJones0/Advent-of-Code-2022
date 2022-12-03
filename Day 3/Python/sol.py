"""
FILE: sol.py
Solution to day 3 problems (5 & 6) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 3/data.txt", "r").read().split("\n")]

##### Problem 5 #####
sum_ = 0
for line in data:
    c1, c2 = line[:len(line) // 2], line[len(line) // 2:]
    for char in c1:
        if char in c2:
            if char == char.lower():
                sum_ += ord(char) - ord('a') + 1
            else:
                sum_ += ord(char) - ord('A') + 27
            break

print("Problem 5:", sum_)


##### Problem 6 #####
sum_ = 0
for i in range(0, len(data), 3):
    group_data = data[i:i+3]
    for char in group_data[0]:
        if char in group_data[1] and char in group_data[2]:
            if char == char.lower():
                sum_ += ord(char) - ord('a') + 1
            else:
                sum_ += ord(char) - ord('A') + 27
            break

print("Problem 6:", sum_)
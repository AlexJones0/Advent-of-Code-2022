"""
FILE: sol.py
Solution to day 2 problems (3 & 4) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.split(" ") for x in open("Day 2/data.txt", "r").read().split("\n")]

##### Problem 3 #####

victories = [('A','C'), ('B','A'), ('C','B')]
x = [ord(x[1]) - ord('X') + 1 for x in data]
y = [(x[0], chr(ord('A') + ord(x[1]) - ord('X'))) for x in data]
z = [0 if game in victories else (3 if game[0] == game[1] else 6) for game in y]
print("Problem 3:", sum(x) + sum(z))


##### Problem 4 #####

lose_strategy = {'A':'Z', 'B':'X', 'C':'Y'}
win_strategy = {'A':'Y', 'B':'Z', 'C':'X'}

choose = [(x[0], lose_strategy[x[0]] if x[1] == 'X' else (win_strategy[x[0]] if x[1] == 'Z' else chr(ord('X') + ord(x[0]) - ord('A')))) for x in data]
x = [ord(x[1]) - ord('X') + 1 for x in choose]
y = [(x[0], chr(ord('A') + ord(x[1]) - ord('X'))) for x in choose]
z = [0 if game in victories else (3 if game[0] == game[1] else 6) for game in y]
print("Problem 4:", sum(x) + sum(z))
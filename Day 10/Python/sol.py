"""
FILE: sol.py
Solution to day 10 problems (19 & 20) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.strip() for x in open("Day 10/data.txt", "r").read().split("\n") if len(x.strip()) != 0]

##### Problem 19 #####
cycle = 0
strengths = []
x = 1
for inst in data:
    if cycle % 40 == 19:
        strengths.append((cycle + 1) * x)
    if inst == "noop":
        cycle += 1
    if inst.startswith("addx"):
        cycle += 2
        if cycle % 40 == 20:
            strengths.append(cycle * x)
        x += int(inst.split(" ")[-1])  
print("Problem 19:", sum(strengths))

##### Problem 20 ######
screen = [['.'] * 40 for _ in range(6)]
cycle = 0
x = 1
cur_op = None
data_index = 0
data_len = len(data)
while data_index < data_len:
    if cycle%40 in [x-1, x, x+1]:
        screen[cycle//40][cycle%40] = '#'
    if cur_op is not None:
        x += int(cur_op.split(" ")[-1]) 
        cur_op = None
    else:
        inst = data[data_index]
        data_index += 1
        if inst.startswith("addx"):
            cur_op = inst
    cycle += 1
# TODO could hard-encode all possible character arts here, but this
# can just be read manually for now ^^
print("Problem 20:\n" + "\n".join("".join(row) for row in screen))
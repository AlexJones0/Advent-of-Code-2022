"""
FILE: sol.py
Solution to day 5 problems (9 & 10) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 5/data.txt", "r").read().split("\n")]

##### Problem 9 #####
n = 0
line = data[n]
part1 = []
while line.strip() != "":
    part1.append(line)
    n += 1
    line = data[n]
numStacks = int(part1[-1].split("   ")[-1].strip())
stacks = [[] for _ in range(numStacks)]
for line in part1[-2::-1]:
    for i in range(0, len(line), 4):
        if line[i+1] != " ":
            stacks[i//4].append(line[i+1])
part2 = data[n+1:]
copied = [x.copy() for x in stacks]
for line in part2:
    parts = line.split(" ")
    movenum, movefrom, moveto = int(parts[1]), int(parts[3])-1, int(parts[5])-1
    for i in range(movenum):
        stacks[moveto].append(stacks[movefrom][-1])
        stacks[movefrom] = stacks[movefrom][:-1]
final = "".join(s[-1] for s in stacks)    
print("Problem 9:", final)

##### Problem 10 ######
stacks = copied
for line in part2:
    parts = line.split(" ")
    movenum, movefrom, moveto = int(parts[1]), int(parts[3])-1, int(parts[5])-1
    stacks[moveto] += stacks[movefrom][-movenum:]
    stacks[movefrom] = stacks[movefrom][:-movenum]
final = "".join(s[-1] for s in stacks) 

print("Problem 10:", final)
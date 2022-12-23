"""
FILE: sol.py
Solution to day 8 problems (15 & 16) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.strip() for x in open("Day 8/data.txt", "r").read().split("\n")]

##### Problem 15 #####
usedpos = set()

def f(data, swap=False):
    global usedpos
    for j, row in enumerate(data):
        highest = -1
        for i, char in enumerate(row):
            char = int(char)
            if char > highest:
                highest = char
                if swap:
                    usedpos.add((i, j))
                else:
                    usedpos.add((j, i))
                if char == 9:
                    break
        highest = -1
        for i, char in enumerate(row[::-1]):
            char = int(char)
            if char > highest:
                highest = char
                if (swap and (len(row)-i-1, j) not in usedpos) or (not swap and (j, len(row)-i-1) not in usedpos): # TODO check
                    if swap:
                        usedpos.add((len(row)-i-1, j))
                    else:
                        usedpos.add((j, len(row)-i-1))
                if char == 9:
                    break

f(data)
cols = ["" for i in range(len(data[0]))]
for col in range(len(data[0])):
    for i in range(len(data)):
        cols[col] += data[i][col]
f(cols, swap=True)
        
print("Problem 15:", len(usedpos))

##### Problem 16 ######
above = {}
allvals = []
for i, row in enumerate(data):
    for j, col in enumerate(row):
        height = int(col)
        vals = [0,0,0,0]
        for k in range(j-1, -1, -1):
            vals[0] += 1
            if int(row[k]) >= height:
                break
        for k in range(j+1, len(row)):
            vals[1] += 1
            if int(row[k]) >= height:
                break
        for k in range(i-1, -1, -1):
            vals[2] += 1
            if int(data[k][j]) >= height:
                break
        for k in range(i+1, len(data)):
            vals[3] += 1
            if int(data[k][j]) >= height:
                break
        allvals.append(vals[0] * vals[1] * vals[2] * vals[3])

print("Problem 16:", max(allvals))
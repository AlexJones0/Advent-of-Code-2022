"""
FILE: sol.py
Solution to day 21 problems (41 & 42) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 21/data.txt", "r").read().split("\n")]        

##### Problem 41 #####
data = [(x.split(":")[0], x.split(":")[0] + " = " + x.split(":")[1].strip(),
         [] if x.split(":")[1].strip().isdigit() else 
         [x.split(":")[1].split(" ")[1].strip(),
          x.split(":")[1].split(" ")[3].strip()]
        ) for x in data]
data = sorted(data, key = lambda x: len(x[2]))
remaining = [x for x in data]
def p1(remaining):
    while 'root' not in locals():
        for i, item in enumerate(remaining):
            all_defined = True
            for var in item[2]:
                if var not in locals():
                    all_defined = False
                    break
            if not all_defined:
                continue
            exec(item[1])
            remaining = remaining[:i] + remaining[(i+1):]
            break
    return int(eval('root'))

print("Problem 41:", p1(remaining))

##### Problem 42 ######
import math
remaining = [x if x[0] != 'root' else (x[0], x[1].replace("*", "==").replace("+", "==").replace("/", "==").replace("-", "=="), x[2]) for x in data if x[0] != 'humn']
rootvars = [x for x in data if x[0] == 'root'][0][2]
all_tested = False
while not all_tested:
    all_tested = True
    for i, item in enumerate(remaining):
        all_defined = True
        for var in item[2]:
            if var not in locals():
                all_defined = False
                break
        if not all_defined:
            continue
        all_tested = False
        exec(item[1])
        remaining = remaining[:i] + remaining[(i+1):]
        break
# Assume input guarantees one variable of root can be worked out without 'humn' - harder if not.
if rootvars[0] in locals():
    target = rootvars[1]
    targetval = int(eval(rootvars[0]))
else:
    target = rootvars[0]
    targetval = int(eval(rootvars[1]))
while target != 'humn':
    item = [x for x in data if x[0] == target][0]
    if item[2][0] in locals():
        targetnum = 1
        target = item[2][1]
    else:
        targetnum = 0
        target = item[2][0]
    if "+" in item[1] and targetnum == 0:
        targetval -= int(eval(item[2][1]))
    elif "+" in item[1] and targetnum == 1:
        targetval -= int(eval(item[2][0]))
    elif "*" in item[1] and targetnum == 0:
        targetval = int(targetval // eval(item[2][1]))
    elif "*" in item[1] and targetnum == 1:
        targetval = int(targetval // eval(item[2][0]))
    elif "-" in item[1] and targetnum == 0:
        targetval += int(eval(item[2][1]))
    elif "-" in item[1] and targetnum == 1:
        targetval = int(eval(item[2][0]) - targetval)
    elif "/" in item[1] and targetnum == 0:
        targetval *= int(eval(item[2][1]))
    elif "/" in item[1] and targetnum == 1:
        targetval = int(eval(item[2][0]) // targetval)

print("Problem 42:", targetval)
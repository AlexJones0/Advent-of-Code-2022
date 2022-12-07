"""
FILE: sol.py
Solution to day 5 problems (9 & 10) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 5/data.txt", "r").read().split("\n")]

##### Problem 9 #####
a, b = data[:data.index("")], [x.split(" ") for x in data[data.index("")+1:]]
s = [[] for _ in range(int(a[-1].split("   ")[-1].strip()))]
for l in a[-2::-1]:
    for i in range(0, len(l), 4):
        if l[i+1] != " ":
            s[i//4].append(l[i+1])
copied = [x.copy() for x in s]
for l in b:
    s[int(l[5])-1] += s[int(l[3])-1][-1:-int(l[1])-1:-1]
    s[int(l[3])-1] = s[int(l[3])-1][:-int(l[1])]
print("Problem 9:", "".join(z[-1] for z in s) )

##### Problem 10 ######
s = copied
for l in b:
    s[int(l[5])-1] += s[int(l[3])-1][-int(l[1]):]
    s[int(l[3])-1] = s[int(l[3])-1][:-int(l[1])]
print("Problem 10:", "".join(z[-1] for z in s) )
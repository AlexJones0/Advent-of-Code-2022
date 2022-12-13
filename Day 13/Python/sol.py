"""
FILE: sol.py
Solution to day 13 problems (25 & 26) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [tuple(x.split("\n")) for x in open("Day 13/data.txt", "r").read().split("\n\n")]

##### Problem 25 #####
def compare(fst, snd):
    for i in range(min(len(fst), len(snd))):
        if isinstance(fst[i], int) and isinstance(snd[i], int):
            if fst[i] != snd[i]:
                return fst[i] < snd[i]
            continue
        if isinstance(fst[i], list) and isinstance(snd[i], list):
            result = compare(fst[i], snd[i]) 
        elif isinstance(fst[i], int) and isinstance(snd[i], list):
            result = compare([fst[i]], snd[i])
        elif isinstance(fst[i], list) and isinstance(snd[i], int):
            result = compare(fst[i], [snd[i]])
        else:
            return False
        if result is not None:
            return result
    if len(fst) != len(snd):
        return len(fst) < len(snd)

print("Problem 25:", sum(i+1 for i, (fst, snd) in enumerate(data) if compare(eval(fst), eval(snd)))  )

##### Problem 26 ######
data = [eval(x) for x in list(sum(data + [('[[2]]', '[[6]]')], ()))]
from functools import cmp_to_key
data = sorted(data, key=cmp_to_key(lambda x, y: -1 if compare(x, y) else 1))
print("Problem 26:", (data.index([[2]]) + 1) * (data.index([[6]]) + 1))

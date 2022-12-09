"""
FILE: sol.py
Solution to day 9 problems (17 & 18) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.strip() for x in open("Day 9/data.txt", "r").read().split("\n") if len(x.strip()) > 0]

##### Problem 17 #####
def print_board(h, t, ts=[]):
    print(h, ts)
    pos_list = list(visited)
    if h is not None and t is not None:
        pos_list += [h, t]
    else:
        pos_list += [h] + ts
    min_h = min(x[0] for x in pos_list)
    min_w = min(x[1] for x in pos_list)
    max_h = max(x[0] for x in pos_list)
    max_w = max(x[1] for x in pos_list)
    for j in range(max_w, min_w-1, -1):
        line = ""
        for i in range(min_h, max_h+1):
            if (i, j) == h:
                line += "H"
            elif (i, j) == t and t is not None:
                line += "T"
            elif (i, j) in ts:
                line += str(ts.index((i,j)) + 1)
            elif (i, j) == (0, 0):
                line += "s"
            elif (i, j) in visited:
                line += "#"
            else:
                line += "."
        print(line)
    print("")
                

visited = set()
VISUALISE = False
dirs = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
headpos = (0, 0)
tailpos = (0, 0)
visited.add(tailpos)
if VISUALISE:
    print_board(headpos, tailpos)
    input()
for rule in data:
    movev = dirs[rule[0]]
    moves = int(rule[2:])
    for i in range(moves):
        headpos = (headpos[0] + movev[0], headpos[1] + movev[1])
        diff = (headpos[0] - tailpos[0], headpos[1] - tailpos[1])
        if abs(diff[0]) > 1 and abs(diff[0]) >= abs(diff[1]):
            tailpos = (tailpos[0] + movev[0], 
                       tailpos[1] + (diff[1] if abs(diff[1]) > 0 else 0))
        elif abs(diff[1]) > 1:
            tailpos = (tailpos[0] + (diff[0] if abs(diff[0]) > 0 else 0), 
                       tailpos[1] + movev[1])
        if VISUALISE:
            print_board(headpos, tailpos)
            input()
        visited.add(tailpos)  

print("Problem 17:", len(visited))

##### Problem 18 ######
visited = set()
VISUALISE = False
dirs = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
headpos = (0, 0)
tails = [(0, 0) for i in range(9)]
visited.add((0,0))
if VISUALISE:
    print_board(headpos, None, ts=tails)
    input()
for rule in data:
    movev = dirs[rule[0]]
    moves = int(rule[2:])
    for i in range(moves):
        headpos = (headpos[0] + movev[0], headpos[1] + movev[1])
        poss = [headpos] + tails
        for i in range(len(poss)-1):
            h, t = poss[i], poss[i+1]
            diff = (h[0] - t[0], h[1] - t[1])
            if abs(diff[0]) > 1 and abs(diff[0]) >= abs(diff[1]):
                tails[i] = (t[0] + (1 if diff[0] >= 0 else -1), 
                            t[1] + ((1 if diff[1] >= 0 else -1) if abs(diff[1]) > 0 else 0))
            elif abs(diff[1]) > 1:
                tails[i] = (t[0] + ((1 if diff[0] >= 0 else -1) if abs(diff[0]) > 0 else 0), 
                            t[1] + (1 if diff[1] >= 0 else -1))
            else:
                break
            poss[i+1] = tails[i]
        if VISUALISE:
            print_board(headpos, None, ts=tails)
            input()
        visited.add(tails[-1])

print("Problem 18:", len(visited))
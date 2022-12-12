"""
FILE: sol.py
Solution to day 12 problems (23 & 24) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 12/data.txt", "r").read().split("\n")]

##### Problem 23 #####
def parse(data):
    elevs = []
    start, end = None, None
    for i, row in enumerate(data):
        elevs.append([])
        for j, char in enumerate(row):
            match char:
                case 'S': 
                    elevs[-1].append(0)
                    start = (i, j)
                case 'E': 
                    elevs[-1].append(25)
                    end = (i, j)
                case x:   
                    elevs[-1].append(ord(x) - ord('a'))
    return (elevs, start, [end])

def bfs(elevs, start, goals, bfsrule):
    frontier = [(start, 0)]
    visited = set(start)
    while len(frontier) != 0:
        cur, m = frontier[0]
        frontier = frontier[1:]
        e = elevs[cur[0]][cur[1]]
        if cur in goals:
            return m
        for pos in [(cur[0]-1,cur[1]), (cur[0]+1,cur[1]), (cur[0],cur[1]-1), (cur[0],cur[1]+1)]:
            if pos not in visited and 0 <= pos[0] < len(elevs) and 0 <= pos[1] < len(elevs[0]):
                if bfsrule(elevs[pos[0]][pos[1]], e):
                    frontier.append((pos, m+1))
                    visited.add(pos)
    return -1
    
print("Problem 23:", bfs(*parse(data), bfsrule = lambda x, y: x <= (y+1)))

##### Problem 24 ######
def parse2(data):
    elevs, _, goals = parse(data)
    endset = set(list((i, j) for i, row in enumerate(elevs) for j, e in enumerate(row) if e == 0))
    return (elevs, goals[0], endset)

print("Problem 24:", bfs(*parse2(data), bfsrule = lambda x, y: x >= (y-1)))
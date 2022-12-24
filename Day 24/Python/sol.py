"""
FILE: sol.py
Solution to day 24 problems (47 & 48) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
VISUALISE, STEPPED = False, False
data = [x for x in open("Day 24/data.txt", "r").read().split("\n")]        

##### Problem 47 #####
# Define dict and anonymous functions for blizzard movement
moves = {">": [0, 1], "<": [0, -1], "v": [1, 0], "^": [-1, 0]}
add_pos = lambda x, y: (x[0] + y[0], x[1] + y[1])

# Parse wall information, start & end positions, and blizzards from input
blizzards = dict()
min_x, max_x, min_y, max_y = 0, 0, 0, 0
start, end = None, None
for i, row in enumerate(data):
    for j, char in enumerate(row):
        if char == "#":
            min_x, max_x = min(min_x, j), max(max_x, j)
            min_y, max_y = min(min_y, i), max(max_y, i)
        elif char != ".":
            if (i, j) in blizzards:
                blizzards[(i, j)].append(char)
            else:
                blizzards[(i, j)] = [char]
        elif char == ".":
            if i == 0:
                start = (i, j)
            elif i == (len(data) - 1):
                end = (i, j)
# Define anonymous functions for wrapping blizzard movement and bounded player movement
wrap = lambda pos: ((max_y - 1) if min_y >= pos[0] else ((min_y + 1) if max_y <= pos[0] else pos[0]),
                    (max_x - 1) if min_x >= pos[1] else ((min_x + 1) if max_x <= pos[1] else pos[1]))
directions = [[0, 1], [1, 0], [0, 0], [0, -1], [-1, 0]]
self_moves = lambda x: [y for y in [add_pos(x, d) for d in directions] if y == start or y == end or (min_x < y[1] < max_x and min_y < y[0] < max_y)]

# Simple function to print the board (at each step) according to the VISUALISE and STEPPED options;
# useful for debugging code problems
def display(blizzards):
    if VISUALISE:
        for row in range(min_y, max_y+1):
            for col in range(min_x, max_x+1):
                if (row, col) != start and (row, col) != end and (row == min_y or row == max_y or col == min_x or col == max_x):
                    print("#", end="")
                elif (row, col) in blizzards:
                    print(len(blizzards[(row, col)]) if len(blizzards[(row, col)]) > 1 else blizzards[(row, col)][0], end="")
                else:
                    print(".", end="")
            print("")
        print("=======================")
        if STEPPED:
            input()

# This function performs the actual simulation, advancing the timestep by 1 minute each time,
# at each step calculating the current stage of the blizzard simulation (updating each blizzard's
# position according to the definded rules) and the set of possible states that the player could
# be in at this time. Simulation is carried out on provided blizzards towards islands (i.e. 
# sub-goals), specified by the player, where the first island is the start point. Every time
# an island is sequentially reached the set of possible positions is reset to only be that 
# island (hence essentially starting another search for the next island, as in island search).
# The minimum amount of time to find all islands is returned.
def simulate(islands, blizzards):
    positions = set([islands[0]])
    islands = islands[1:]
    time = 0
    while True:
        # Check islands being searched for
        if islands[0] in positions:
            positions = set([islands[0]])
            islands = islands[1:]
            if len(islands) == 0:
                return time
        time += 1
        display(blizzards)
        # Update blizzard simulation
        next_blizzards = dict()
        for blizz_pos, blizz_types in blizzards.items():
            for blizz_type in blizz_types:
                next_pos = wrap(add_pos(blizz_pos, moves[blizz_type]))
                if next_pos in next_blizzards:
                    next_blizzards[next_pos].append(blizz_type)
                else:
                    next_blizzards[next_pos] = [blizz_type]
        blizzards = next_blizzards
        # Update possible player position simulation
        next_positions = set()
        for pos in positions:
            for next_pos in set(self_moves(pos)).difference(set(blizzards.keys())):
                next_positions.add(next_pos)
        positions = next_positions
            
print("Problem 47:", simulate([start, end], blizzards))

##### Problem 48 ######
print("Problem 48:", simulate([start, end, start, end], blizzards))
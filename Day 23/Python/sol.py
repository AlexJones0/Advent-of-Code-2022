"""
FILE: sol.py
Solution to day 23 problems (45 & 46) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
VISUALISE, STEPPED = False, False
data = [x for x in open("Day 23/data.txt", "r").read().split("\n")]        

##### Problem 45 #####
def display(elves, i):
    # Prints the current minimum bounding box for visualising the simulation
    elf = list(elves)[0]
    min_y, max_y, min_x, max_x = elf[0], elf[0], elf[1], elf[1]
    for elf in elves:
        min_y, max_y = min(min_y, elf[0]), max(max_y, elf[0])
        min_x, max_x = min(min_x, elf[1]), max(max_x, elf[1])
    for row in range(min_y, max_y+1):
        for col in range(min_x, max_x+1):
            if (row, col) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    print(f"======== ROUND {i+1} ========")
    if STEPPED: # Lets user view input in steps if the relevant option is set.
        input()

# Define directions used in the problem
directions = {
    "N": [-1, 0], "E": [0, 1], "S": [1, 0], "W": [0, -1],
    "NE": [-1, 1], "NW": [-1, -1], "SE": [1, 1], "SW": [1, -1]
}

# Define anonymous functions for simple operations - position retrieval, emptiness checking, rule list rotation
add_pos = lambda x, y: (x[0] + y[0], x[1] + y[1])
are_empty = lambda poss, elves: len([pos for pos in poss if pos in elves]) == 0
get_pos = lambda x, d: add_pos(x, directions[d])
get_poss = lambda x, ds: [get_pos(x, d) for d in ds]
adjacent = lambda x: get_poss(x, directions.keys())
rotate = lambda xs, n: xs[n:] + xs[:n]

def propose_move(elf, move, proposed):
    # Proposes a move by an elf, adding it to the list of elves proposing thatm ove if already proposed.
    if move not in proposed:
        proposed[move] = [elf]
    else:
        proposed[move].append(elf)

def simulate(elves, rounds=None):
    # This function simulates the elves, with two purposes. Either (a) it is given a number of
    # rounds along with the elves, at which point it simulates that number of rounds and returns
    # the number of empty tiles in the minimum rectangle box bounding the elves positions at the 
    # end of that number of rounds, or (b) no number of rounds are given, and simulation continues
    # forever until all elves stop, at which point the round number is returned.
    rules = [(['N', 'NE', 'NW'], 'N'), 
             (['S', 'SE', 'SW'], 'S'), 
             (['W', 'NW', 'SW'], 'W'),
             (['E', 'NE', 'SE'], 'E')]
    round = 0
    while rounds is None or round < rounds:
        round += 1
        if VISUALISE: display(elves, i)
        # First half of round - all elves proposed moves based on rules
        proposed = {}
        for elf in elves:
            if are_empty(adjacent(elf), elves):
                continue
            for rule in rotate(rules, (round-1) % len(rules)):
                if are_empty(get_poss(elf, rule[0]), elves):
                    propose_move(elf, get_pos(elf, rule[1]), proposed)
                    moved = True
                    break
        # Second half of round - move if only elf to propose moving there
        moved = False
        for move, moving in proposed.items():
            if len(moving) == 1:
                elves.remove(moving[0])
                elves.add(move)
                moved = True
        if not moved: # No elves moved - return if this is the goal, or stop simulating (optimisation)
            if rounds == None: return round
            break
    # Find bounding rectangle box for elves, and return its area minus the number of elves in it
    elf = list(elves)[0]
    min_y, max_y, min_x, max_x = elf[0], elf[0], elf[1], elf[1]
    for elf in elves:
        min_y, max_y = min(min_y, elf[0]), max(max_y, elf[0])
        min_x, max_x = min(min_x, elf[1]), max(max_x, elf[1])
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)

# Parse elf position information from the input, and simulate 10 rounds
elves = set()
for i, row in enumerate(data):
    for j, char in enumerate(row):
        if char == "#":
            elves.add((i, j))
print("Problem 45:", simulate(elves.copy(), 10))

##### Problem 46 ######
print("Problem 46:", simulate(elves))
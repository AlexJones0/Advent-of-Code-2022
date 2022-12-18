"""
FILE: sol.py
Solution to day 17 problems (33 & 34) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
VISUALISE = False
data = [x for x in open("Day 17/data.txt", "r").read().split("\n")]

def visualise(cur_height, covered, rocks_num, jets_num, state_index):
    for y in range(cur_height, -1, -1):
        row = ""
        for x in range(0, 7):
            if (x, y) in covered:
                row += "#"
            else:
                row += "."
        print(row)
    print(f"Rocks dropped: {rocks_num}, Air jetted: {jets_num}, State Index: {state_index}")
    input()

##### Problem 33 #####
pattern = [-1 if p == '<' else 1 for p in data[0]]
rocks = [
    lambda x,y: [(x,y), (x+1,y), (x+2,y), (x+3,y)],
    lambda x,y: [(x+1,y), (x,y+1), (x+1,y+1), (x+2,y+1), (x+1,y+2)],
    lambda x,y: [(x,y), (x+1,y), (x+2,y), (x+2,y+1), (x+2,y+2)],
    lambda x,y: [(x,y), (x,y+1), (x,y+2), (x,y+3)],
    lambda x,y: [(x,y), (x+1,y), (x,y+1), (x+1,y+1)],
]

def is_valid_positions(positions, covered):
    for (x,y) in positions:
        if x < 0 or x > 6 or y < 0 or (x,y) in covered:
            return False
    return True

def sim(pattern, rocks, sim_num):
    pattern_len = len(pattern)
    rock_types = len(rocks)
    cur_height = -1
    rocks_num = 0
    jets_num = 0
    covered = set()
    state_cache = {}
    while rocks_num < sim_num:
        # Perform cycle detection to optimise - if dropping the same rock at
        # the same point in the jet pattern, after both the rock list and
        # jet pattern have been traversed once, then we know that we 
        # have found a repetition. As a cycle will provide many such
        # sequential repetitions, we simply carry on dropping rocks
        # until we find the exact cycle such that after some number of 
        # iterations, it will end exactly on our desired simulation number.
        state_index = (rocks_num % rock_types, jets_num % pattern_len)
        if state_index in state_cache:
            prev_height, prev_num = state_cache[state_index]
            cycle_period = rocks_num - prev_num
            if rocks_num % cycle_period == sim_num % cycle_period:
                # We simply calculate the period and height (change in max elevation)
                # of the cycle, and find the height by doing:
                #   h = cycle height * num_cycles + height_before_cycles + 1 (as we zero index)
                height = cur_height - prev_height
                rocks_left = sim_num - rocks_num
                return height * ((rocks_left // cycle_period) + 1) + prev_height + 1
        state_cache[state_index] = (cur_height, rocks_num)
        # If no cycle, initialise the next rock to drop
        rock_pos = (2, cur_height + 4)
        stopped = False
        # Keep simulating until the rock stops
        while not stopped:
            # Simulate the jet pushing the rock, only allowing if valid
            new_rock_pos = (rock_pos[0] + pattern[jets_num % pattern_len], rock_pos[1])
            jets_num += 1
            new_positions = rocks[rocks_num % rock_types](*new_rock_pos)
            if is_valid_positions(new_positions, covered):
                rock_pos = new_rock_pos
            # Simulate the rock falling 1 unit, stopping if invalid.
            new_rock_pos = (rock_pos[0], rock_pos[1] - 1)
            new_positions = rocks[rocks_num % rock_types](*new_rock_pos)
            if is_valid_positions(new_positions, covered):
                rock_pos = new_rock_pos
            else:
                # The rock has stopped - record its positions and max height
                positions = rocks[rocks_num % rock_types](*rock_pos)
                stopped = True
                for pos in positions:
                    covered.add(pos)
                    if pos[1] > cur_height:
                        cur_height = pos[1]
        rocks_num += 1
        if VISUALISE:
            visualise(cur_height, covered, rocks_num, jets_num, state_index)
    return cur_height + 1

print("Problem 33:", sim(pattern, rocks, 2022))

##### Problem 34 ######

print("Problem 34:", sim(pattern, rocks, 1000000000000))

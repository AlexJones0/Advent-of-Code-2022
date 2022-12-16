"""
FILE: sol.py
Solution to day 16 problems (31 & 32) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 16/data.txt", "r").read().split("\n")]

##### Problem 31 #####
valves = {x.split(" ")[1]: (   
            int(x.split("=")[1].split(";")[0]),
            [x.split(",")[0].split(" ")[-1]] + [y.strip() for y in x.split(",")[1:]]
        ) for x in data}

# Perform BFS from each meaningful node to simplify the graph, storing 
# distances between each node. This will facilitate memoisation later
key_valves = set(list(v for v in valves if valves[v][0] > 0 or v == "AA"))
valve_distances = {}
for start_valve in key_valves:
    # Perform BFS from every meaningful valve ('AA' or with pressure > 0)
    distance = 0
    frontier = set([start_valve])
    valve_distances[(start_valve, start_valve)] = 0
    while len(frontier) > 0:
        # Simple BFS with edge weights of 1 to record distances to each valve
        new_frontier = set()
        distance += 1
        for cur_valve in frontier:
            for tunnel_valve in valves[cur_valve][1]:
                if (start_valve, tunnel_valve) not in valve_distances:
                    valve_distances[(start_valve, tunnel_valve)] = distance
                    new_frontier.add(tunnel_valve)
        frontier = new_frontier

# Next we search with dynamic programming to find the best possible path (the
# path with the highest pressure) by making use of recursive subproblems
def find_paths(cur_valve, cur_pressure, time_left, visited):
    visited = visited.copy()
    visited.add(cur_valve) # Update list of visited nodes
    unvisited = key_valves.difference(visited)
    max_pressure = 0
    for target_valve in unvisited: # Check all reachable unvisited nodes in the graph to potentially open
        new_time_left = time_left - valve_distances[(cur_valve, target_valve)] - 1
        if new_time_left > 0:
            # Calculate the new pressure after opening the target, and determine if it is b est
            new_pressure = new_time_left * valves[target_valve][0]
            new_pressure = new_pressure + find_paths(target_valve, cur_pressure + new_pressure, new_time_left, visited)
            max_pressure = max(max_pressure, new_pressure)
    return max_pressure
best = find_paths("AA", 0, 30, set())

print("Problem 31:", best)

##### Problem 32 ######

# TODO again, memoise by splitting the problem into subsets of visited nodes -
# store the maximum pressure found for a set of visited nodes (excluding 'AA')/
subset_vals = {}
def find_paths(cur_valve, cur_pressure, time_left, visited):
    # A sort of DP memoised depth-first search, breaking the problem into smaller
    # subproblems of finding flow in a graph with a given source and sink node.
    visited = visited.copy()
    visited.add(cur_valve)
    unvisited = key_valves.difference(visited)
    subset = set(list(v for v in visited if v != 'AA'))
    subset_key = tuple(sorted(subset))
    if subset_key not in subset_vals:
        subset_vals[subset_key] = cur_pressure
    else:
        subset_vals[subset_key] = max(subset_vals[subset_key], cur_pressure)
    max_pressure = 0
    for target_valve in unvisited:
        new_time_left = time_left - valve_distances[(cur_valve, target_valve)] - 1
        if new_time_left > 0:
            new_pressure = new_time_left * valves[target_valve][0]
            new_pressure = new_pressure + find_paths(target_valve, cur_pressure + new_pressure, new_time_left, visited)
            max_pressure = max(max_pressure, new_pressure)
    return max_pressure
find_paths("AA", 0, 26, set())

def add_other_subsets(subset):
    subset_key = tuple(sorted(subset))
    if subset_key not in subset_vals:
        max_pressure = 0
        for valve in subset:
            smaller_set = subset.difference({valve})
            max_pressure = max(max_pressure, add_other_subsets(smaller_set))
        subset_vals[subset_key] = max_pressure
    return subset_vals[subset_key]

other = key_valves.difference({'AA'})
complements = dict([(x, other.difference(set(x))) for x in subset_vals.keys()])
for elephant_valves in complements.values():
    add_other_subsets(elephant_valves)
max_pressure = 0
for cur_valves, elephant_valves in complements.items():
    # Assign the elephant the complement - even if they can't get every other valve,
    # the memoisation will account for this - subset_vals[elephant_valves] will just
    # be the maximum that they could open from 'AA' in 26 minutes.
    elephant_valves = tuple(sorted(elephant_valves))
    max_pressure = max(max_pressure, subset_vals[cur_valves] + subset_vals[elephant_valves])

print("Problem 32:", max_pressure)

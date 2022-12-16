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

# Perform BFS from each meaningful node to simplify the graph
key_valves = set(list(v for v in valves if valves[v][0] > 0 or v == "AA"))
frontier = [[v] for v in key_valves]
simple_graph = {v: set() for v in key_valves}
while len(frontier) != 0:
    # BFS - get next node from frontier
    cur_path = frontier[0]
    start_valve, cur_valve = cur_path[0], cur_path[-1]
    frontier = frontier[1:]
    # Add a node to the simplified graph if the current valve is meaningful
    if valves[cur_valve][0] > 0 and len(cur_path) > 1:
        simple_graph[start_valve].add((cur_valve, len(cur_path) - 1))
    else:
        # Add neighbours to the frontier
        for tunnel_valve in valves[cur_valve][1]:
            if tunnel_valve not in cur_path:
                frontier.append(cur_path + [tunnel_valve])
simple_graph = dict([(x, sorted(y, key=lambda item: valves[item[0]][0] / item[1], reverse=True)) for x, y in simple_graph.items()])

# Next perform DFS on the simplified graph to find the best path
#   TODO have to make an assumption that all meaningful (>0 value) valves should be opened, and never just
#   traversed - pretty sure this is wrong but no idea how to do this
frontier = [("AA", [], 0, 30)]
best = -1
while len(frontier) != 0:
    # DFS - get next node from frontier
    current = frontier[0]
    cur_valve, cur_open, cur_pressure, time_left = current
    frontier = frontier[1:]
    # Check for full paths of length 30 minutes
    if time_left <= 0:
        if cur_pressure > best:
            best = cur_pressure
        continue
    # First type of neighbour is going down a different tunnel
    found_sol = False
    for (tunnel_valve, time_cost) in simple_graph[cur_valve]: # TODO could I order this?
        if tunnel_valve == 'AA' or tunnel_valve in cur_open:
            new_open = cur_open
            new_time_left = time_left - time_cost
            new_pressure = cur_pressure
        else:
            new_open = cur_open.copy()
            new_open.append(tunnel_valve)
            new_time_left = time_left - time_cost - 1
            new_pressure = cur_pressure + new_time_left * valves[tunnel_valve][0]
        if new_time_left >= 0:
            frontier = [(tunnel_valve, new_open, new_pressure, new_time_left)] + frontier 
            found_sol = True
    if not found_sol:
        frontier = [(cur_valve, cur_open, cur_pressure, 0)] + frontier

print("Problem 31:", best)

##### Problem 32 ######
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
add_other_subsets(key_valves.difference({'AA'}))

max_pressure = 0
for cur_valves in subset_vals:
    # Assign the elephant the complement - even if they can't get every other valve,
    # the memoisation will account for this - subset_vals[elephant_valves] will just
    # be the maximum that they could open from 'AA' in 26 minutes.
    elephant_valves = key_valves.difference({'AA'}).difference(set(cur_valves))
    elephant_valves = tuple(sorted(elephant_valves))
    max_pressure = max(max_pressure, subset_vals[cur_valves] + subset_vals[elephant_valves])

print("Problem 32:", max_pressure)

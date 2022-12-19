"""
FILE: sol.py
Solution to day 19 problems (37 & 38) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 19/data.txt", "r").read().split("\n")]

##### Problem 37 #####
blueprints = [{
    "ore_robot_cost": int(x.split("costs ")[1].split(" ")[0]), # Ore
    "clay_robot_cost": int(x.split("costs ")[2].split(" ")[0]), # Ore
    "obs_robot_cost": (int(x.split("costs ")[3].split(" ")[0]), # (Ore, Clay)
                       int(x.split("costs ")[3].split("and ")[1].split(" ")[0])),
    "geode_robot_cost": (int(x.split("costs ")[4].split(" ")[0]), # (Ore, Obsidian)
                         int(x.split("costs ")[4].split("and ")[1].split(" ")[0]))
    } for x in data]

def dfs(time=24, ore_robs=1, clay_robs=0, obs_robs=0, geode_robs=0,
        ore=0, clay=0, obs=0, geodes=0, blueprint=None, best=0, 
        max_ore_robs=None, max_clay_robs=None, max_obs_robs=None):
    made_robot = False
    max_geodes = geodes
    if geodes + geode_robs * time + (time * (time + 1) // 2) <= best:
        return geodes  # Prune branch - can never be better
    elif ore_robs > max_ore_robs or clay_robs > max_clay_robs or obs_robs > max_obs_robs:
        return geodes  # Prune branch - sub-optimal
    
    # First consider making an ore robot
    ore_needed = max(0, blueprint["ore_robot_cost"] - ore)
    t = 1 + ore_needed // ore_robs + (1 if ore_needed % ore_robs != 0 else 0)
    if t <= time:
        made_robot = True
        g = dfs(time-t, ore_robs+1, clay_robs, obs_robs, geode_robs,
                ore-blueprint["ore_robot_cost"]+ore_robs*t, clay+clay_robs*t, obs+obs_robs*t, 
                geodes+geode_robs*t, blueprint, max(best, max_geodes), max_ore_robs,
                max_clay_robs, max_obs_robs)
        max_geodes = max(max_geodes, g)

    # Next consider making a clay robot
    ore_needed = max(0, blueprint["clay_robot_cost"] - ore) 
    t = 1 + ore_needed // ore_robs + (1 if ore_needed % ore_robs != 0 else 0)
    if t <= time:
        made_robot = True
        g = dfs(time-t, ore_robs, clay_robs+1, obs_robs, geode_robs,
                ore-blueprint["clay_robot_cost"]+ore_robs*t, clay+clay_robs*t, obs+obs_robs*t,
                geodes+geode_robs*t, blueprint, max(best, max_geodes), max_ore_robs,
                max_clay_robs, max_obs_robs)
        max_geodes = max(max_geodes, g)

    # Next consider making an obsidian robot
    if clay_robs > 0:
        ore_needed = max(0, blueprint["obs_robot_cost"][0] - ore)
        t1 = 1 + ore_needed // ore_robs + (1 if ore_needed % ore_robs != 0 else 0)
        clay_needed = max(0, blueprint["obs_robot_cost"][1] - clay)
        t2 = 1 + clay_needed // clay_robs + (1 if clay_needed % clay_robs != 0 else 0)
        t = max(t1, t2)
        if t <= time:
            made_robot = True      
            g = dfs(time-t, ore_robs, clay_robs, obs_robs+1, geode_robs,
                    ore-blueprint["obs_robot_cost"][0]+ore_robs*t, 
                    clay-blueprint["obs_robot_cost"][1]+clay_robs*t,
                    obs+obs_robs*t, geodes+geode_robs*t, blueprint, max(best, max_geodes),
                    max_ore_robs, max_clay_robs, max_obs_robs)
            max_geodes = max(max_geodes, g)

    # Next consider making a geode robot
    if obs_robs > 0:
        ore_needed = max(0, blueprint["geode_robot_cost"][0] - ore)
        t1 = 1 + ore_needed // ore_robs + (1 if ore_needed % ore_robs != 0 else 0)
        obs_needed = max(0, blueprint["geode_robot_cost"][1] - obs)
        t2 = 1 + obs_needed // obs_robs + (1 if obs_needed % obs_robs != 0 else 0)
        t = max(t1, t2)
        if t <= time:
            made_robot = True
            g = dfs(time-t, ore_robs, clay_robs, obs_robs, geode_robs+1,
                    ore-blueprint["geode_robot_cost"][0]+ore_robs*t, clay+clay_robs*t,
                    obs-blueprint["geode_robot_cost"][1]+obs_robs*t, geodes+geode_robs*t,
                    blueprint, max(best, max_geodes), max_ore_robs, max_clay_robs, max_obs_robs)
            max_geodes = max(max_geodes, g)

    # We finally consider the base case
    if not made_robot:
        return geodes + geode_robs * time
    return max_geodes

# Iterate through blueprints and calculate quality, summing it.
qualities = []
for i, bp in enumerate(blueprints):
    max_ore = max(bp["ore_robot_cost"], bp["clay_robot_cost"], bp["obs_robot_cost"][0], bp["geode_robot_cost"][0])
    max_clay, max_obs = bp["obs_robot_cost"][1], bp["geode_robot_cost"][1]
    geodes = dfs(blueprint=bp, max_ore_robs=max_ore, max_clay_robs=max_clay, max_obs_robs=max_obs)
    qualities.append(geodes * (i + 1))
print("Problem 37:", sum(qualities))

##### Problem 38 ######
# Iterate through first 3 blueprints and multiply max geodes with t=32mins.
total = 1
for i, bp in enumerate(blueprints[:3]):
    max_ore = max(bp["ore_robot_cost"], bp["clay_robot_cost"], bp["obs_robot_cost"][0], bp["geode_robot_cost"][0])
    max_clay, max_obs = bp["obs_robot_cost"][1], bp["geode_robot_cost"][1]
    total *= dfs(time=32, blueprint=bp, max_ore_robs=max_ore, max_clay_robs=max_clay, max_obs_robs=max_obs)
print("Problem 38:", total)
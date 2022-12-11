"""
FILE: sol.py
Solution to day 11 problems (21 & 22) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.split("\n") for x in open("Day 11/data.txt", "r").read().split("\n\n")]

##### Problem 21 #####
def get_monkey_info(data):
    return [{"items": [int("".join(i.split(","))) for i in m[1].strip().split(" ")[2:]], 
             "op": " ".join(m[2].strip().split(" ")[3:]),
             "test": int(m[3].strip().split(" ")[-1]),
             "true": int(m[4].strip().split(" ")[-1]),
             "false": int(m[5].strip().split(" ")[-1]),
             "inspects": 0} for m in data]

def simulate_rounds(rounds, monkeys, divval, modval=None):
    round = 1
    while round <= rounds:
        round += 1
        for monkey in monkeys:
            for i in range(len(monkey["items"])):
                old = monkey["items"][i]
                newval = eval(monkey["op"]) // divval
                if modval is not None:
                    newval = newval % modval
                throwto = monkey["true"] if (newval % monkey["test"] == 0) else monkey["false"]
                monkeys[throwto]["items"].append(newval)
                monkey["inspects"] += 1
            monkey["items"] = []
    inspects = sorted([m["inspects"] for m in monkeys], reverse=True)[:2]
    return inspects[0] * inspects[1]
    
print("Problem 21:", simulate_rounds(20, get_monkey_info(data), 3))

##### Problem 22 ######
monkeys = get_monkey_info(data)
modval = 1  # was going to replace this with math.lcm but the number turns out the same
for monkey in monkeys:
    modval *= monkey["test"]
print("Problem 22:", simulate_rounds(10000, monkeys, 1, modval=modval))
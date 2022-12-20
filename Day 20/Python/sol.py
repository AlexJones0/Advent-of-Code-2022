"""
FILE: sol.py
Solution to day 20 problems (39 & 40) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [int(x.strip()) for x in open("Day 20/data.txt", "r").read().split("\n")]        

##### Problem 39 #####
class Node():
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

nodes = [Node(x) for x in data]
length = len(data)
for i in range(length):
    nodes[i].next = nodes[(i+1)%length]
    nodes[i].prev = nodes[i-1]
for i in range(length):
    val = data[i]
    node = nodes[i]
    if val == 0:
        continue
    if val < 0:
        before = node.prev
        node.next.prev = node.prev
        node.prev.next = node.next
        for i in range(-val):
            before = before.prev
        before.next.prev = node
        node.next = before.next
        before.next = node
        node.prev = before
    elif val > 0:
        after = node.next
        node.next.prev = node.prev
        node.prev.next = node.next
        for i in range(val):
            after = after.next
        after.prev.next = node
        node.prev = after.prev
        after.prev = node
        node.next = after

start, i, total = nodes[data.index(0)], 0, 0
cur = start
while i <= 3000:
    if i in [1000, 2000, 3000]:
        total += cur.val
    cur = cur.next
    i += 1

print("Problem 39:", total)

##### Problem 40 ######
data = [x * 811589153 for x in data]
nodes = [Node(x) for x in data]
length = len(data)
for i in range(length):
    nodes[i].next = nodes[(i+1)%length]
    nodes[i].prev = nodes[i-1]
for round in range(10):
    for i in range(length):
        val = data[i]
        node = nodes[i]
        if val == 0 or abs(val) % length == 0:
            continue
        if val < 0:
            val = -val % length
            before = node.prev
            node.next.prev = node.prev
            node.prev.next = node.next
            for i in range(val):
                before = before.prev
            before.next.prev = node
            node.next = before.next
            before.next = node
            node.prev = before
        elif val > 0:
            val = val % length
            after = node.next
            node.next.prev = node.prev
            node.prev.next = node.next
            for i in range(val):
                after = after.next
            after.prev.next = node
            node.prev = after.prev
            after.prev = node
            node.next = after

start, i, total = nodes[data.index(0)], 0, 0
cur = start
while i <= 3000:
    if i in [1000, 2000, 3000]:
        total += cur.val
    cur = cur.next
    i += 1

print("Problem 40:", total)
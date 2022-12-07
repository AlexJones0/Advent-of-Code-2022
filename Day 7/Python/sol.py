"""
FILE: sol.py
Solution to day 7 problems (13 & 14) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.strip() for x in open("Day 7/data.txt", "r").read().split("\n")]

##### Problem 13 #####
dirtree = {"/": []}
parent = {"/": "/"}
filesize = {"/": 0}
curdir = "/"

def add_dir(parent_, newdir):
    dirtree[parent_].append(newdir)
    dirtree[newdir] = []
    parent[newdir] = parent_
    filesize[newdir] = 0

for line in data:
    print(curdir)
    if line == "$ cd ..":
        curdir = parent[curdir]
    elif line == "$ cd /":
        curdir = "/"
    elif line.startswith("$ cd "):
        newdir = line[5:]
        if curdir != "/":
            dirname = curdir + "/" + newdir
        else:
            dirname = curdir + newdir
        if dirname not in dirtree[curdir]:
            add_dir(curdir, dirname)
            curdir = dirname
    elif not line.startswith("$"):
        if line.startswith("dir "):
            lsdir = line[4:]
            if lsdir not in dirtree[curdir]:
                add_dir(curdir, lsdir)
        else:
            size = int(line.split(" ")[0])
            if curdir == "/":
                filesize[curdir] += size
                continue
            dirs = curdir.split("/")
            filesize['/'] += size
            for i in range(2, len(dirs) + 1):
                adddir = "/".join(dirs[:i])
                filesize[adddir] += size

result = sum([size for _, size in filesize.items() if size < 100000])
print("Problem 13:", result)

##### Problem 14 ######
to_save = 30000000 - 70000000 + filesize["/"]
result = min([size for _, size in filesize.items() if size > to_save])
print("Problem 14:", result)
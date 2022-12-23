"""
FILE: sol.py
Solution to day 7 problems (13 & 14) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x.strip() for x in open("Day 07/data.txt", "r").read().split("\n")]

##### Problem 13 #####
dirtree = {"/": []}
filesize = {"/": 0}
curdir = "/"

def add_dir(parent_, newdir):
    dirtree[parent_].append(newdir)
    dirtree[newdir] = []
    filesize[newdir] = 0

for line in data:
    if line == "$ cd ..":
        curdir = "/".join(curdir.split("/")[:-1])
        curdir = "/" if len(curdir) == 0 else curdir
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

result = sum([size for size in filesize.values() if size < 100000])
print("Problem 13:", result)

##### Problem 14 ######
to_save = -40000000 + filesize["/"]
result = min([size for size in filesize.values() if size > to_save])
print("Problem 14:", result)
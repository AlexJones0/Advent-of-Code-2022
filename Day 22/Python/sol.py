"""
FILE: sol.py
Solution to day 22 problems (43 & 44) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 22/data.txt", "r").read().split("\n")]        

##### Problem 43 #####
# Utility funcitons for representing directions and 90 degree rotations
dirs = [[1,0], [0,1], [-1,0], [0,-1]]
rotate = lambda d, n: dirs[(dirs.index(d)+n)%len(dirs)]
clockwise, anticlockwise = lambda d: rotate(d, 1), lambda d: rotate(d, -1)

# Puzzle information - password calculator, board/desc parsing and padding, dimension and start pos retrieval.
passwd = lambda x, y, d: 1000 * (y+1) + 4 * (x+1) + dirs.index(list(d))
board, desc = data[:-2], data[-1]
desc = desc.replace("R", "#R#").replace("L", "#L#")
width, height = max([len(row) for row in board]), len(board)
board = [row + ' ' * (width - len(row)) for row in board]
pos, dir_ = (board[0].index('.'), 0), [1, 0]

# This function wraps cardinal traversals of the grid according to part 1 rules (pure cardinal)
def wrap(board, width, height, loc, dir_):
    x, y = loc[0], loc[1]
    if dir_ == [1,0]:
        for nx, char in enumerate(board[y]):
            if char != ' ':
                return ((nx, y), dir_)
    elif dir_ == [-1,0]:
        for nx, char in enumerate(board[y][::-1]):
            if char != ' ':
                return ((width - 1 - nx, y), dir_)
    elif dir_ == [0, 1]:
        for ny in range(height):
            char = board[ny][x]
            if char != ' ':
                return ((x, ny), dir_)
    elif dir_ == [0, -1]:
        for ny in range(height-1, -1, -1):
            char = board[ny][x]
            if char != ' ':
                return ((x, ny), dir_)
    return (loc, dir_)

# Generalised solve function for part 1 and part 2 - rotates on a L/R instruction,
# and moves otherwise, calling the provided wrap function to determine its new position
# and direction after moving in the case that moving would leave the grid.
# Returns the resulting final position and direction for use in calculating the password.
def solve(board, width, height, desc, pos, dir_, wrapfunc):
    for inst in desc.split("#"):
        if inst == 'R':
            dir_ = clockwise(dir_); continue
        elif inst == 'L':
            dir_ = anticlockwise(dir_); continue
        for i in range(int(inst)):
            prev = pos
            pos = (pos[0] + dir_[0], pos[1] + dir_[1])
            x, y = pos[0], pos[1]
            if not (0 <= x < width and 0 <= y < height) or board[y][x] == ' ':
                old_dir = dir_
                pos, dir_ = wrapfunc(board, width, height, prev, dir_)
                x, y = pos[0], pos[1]
                if board[y][x] == '#':
                    pos = prev
                    dir_ = old_dir
                    break
            if board[y][x] == '#':
                pos = prev
                break
    return (pos[0], pos[1], dir_)

print("Problem 43:", passwd(*solve(board, width, height, desc, pos, dir_, wrap)))

##### Problem 44 ######
# General solution - first parse cube dimensions via. GCD on dimensions and whitespace parsing
from math import gcd
cube_dim = gcd(height, width)
cube_dim = min([cube_dim] + [len(row) - len(row.strip()) for row in board if len(row.strip()) != len(row)])  # Not 100% correct but correct enough for most cases

# Next form a simple map of links between cube faces from the net, using cardinal net links only.
# This is a map of net_map[(fx, fy)][dir_from] = ((nx, ny), dir_to)
# Where (fx, fy) are the top-left coordinates of the face, dir_from is the direction leaving that face from,
# (nx, ny) are the top-left coordinates of the face that leads to, and dir_to is the direction entering
# that face from.
net_map = {}
for x in range(0, width, cube_dim):
    for y in range(0, height, cube_dim):
        if board[y][x] != ' ':
            for d in dirs:
                nx, ny = x + cube_dim * d[0], y + cube_dim * d[1]
                if 0 <= nx < width and 0 <= ny < height and board[ny][nx] != ' ':
                    if (x,y) not in net_map:
                        net_map[(x,y)] = {}
                    net_map[(x,y)][tuple(d)] = ((nx, ny), clockwise(clockwise(d)))

# Next we perform propagation of determined faces to completely fill out the net_map
# representing cube transitions on our net map. We do this by calculating unknown
# faces where possible using compositions of known face transitions, and repating
# this process until all are defined - the net should have enough information such
# that this is generally at most 2 passes.
clockwise, anticlockwise = lambda d: tuple(rotate(list(d), 1)), lambda d: tuple(rotate(list(d), -1))   
while len([f for f, m in net_map.items() if len(m) != 4]) > 0: # Repeat until all info propagated (map filled)
    for face1 in net_map:
        f1map = net_map[face1]
        if len(f1map) == 4:
            continue
        for d in dirs:
            if tuple(d) in f1map:
                continue # Only consider undefined directions for each face
            cw, acw = tuple(clockwise(d)), tuple(anticlockwise(d))
            opp = tuple(clockwise(clockwise(d)))
            d = tuple(d)
            if cw in f1map: # Try to find face by looking clockwise->clockwise or looking clockwise->opposite->clockwise
                face2, nd = f1map[cw]
                f2map = net_map[face2]
                if clockwise(nd) in f2map:
                    target, td = f2map[clockwise(nd)]
                    f1map[d] = (target, clockwise(td)); continue
                elif clockwise(clockwise(nd)) in f2map:
                    face3, nnd = f2map[clockwise(clockwise(nd))]
                    f3map = net_map[face3]
                    if clockwise(nnd) in f3map:
                        target, td = f3map[clockwise(nnd)]
                        f1map[d] = (target, clockwise(clockwise(td))); continue
            if acw in f1map: # Try to find face by looking anti-clockwise->anti-clockwise or anti-clockwise->opposite->anti-clockwise
                face2, nd = f1map[acw]
                f2map = net_map[face2]
                if anticlockwise(nd) in f2map:
                    target, td = f2map[anticlockwise(nd)]
                    f1map[d] = (target, anticlockwise(td)); continue
                elif anticlockwise(anticlockwise(nd)) in f2map:
                    face3, nnd = f2map[anticlockwise(anticlockwise(nd))]
                    f3map = net_map[face3]
                    if anticlockwise(nnd) in f3map:
                        target, td = f3map[anticlockwise(nnd)]
                        f1map[d] = (target, anticlockwise(anticlockwise(td))); continue
            if opp in f1map: # Try to find face by looking opposite->opposite->opposite->opposite
                face2, nd = f1map[opp]
                f2map = net_map[face2]
                if clockwise(clockwise(nd)) in f2map:
                    face3, nnd = f2map[clockwise(clockwise(nd))]
                    f3map = net_map[face3]
                    if clockwise(clockwise(nnd)) in f3map:
                        target, td = f3map[clockwise(clockwise(nnd))]
                        f1map[d] = (target, clockwise(clockwise(td))); continue


# A function for performing wrapping according to the cube net map rules defined
# in part 2 - here we use the net map and input information to determine the
# face being left and arrived at, and the cardinal direction being left from
# and being arrived at. Using this and the relative rotations of these
# directions (same, opposite, clockwise or anticlockwise), I devise equations
# for computing the new indexes of the wrapped movement - in most cases
# completely hard-coding this because I don't have the time to figure out
# more generalised rotational matrices etc. This also returns a new direction
# as well as position, with the new direction being a rotation of the incoming
# direction based on the difference in rotation of the to- and from-directions.
def cubewrap(board, width, height, loc, dir_):
    face = (loc[0] // cube_dim * cube_dim, loc[1] // cube_dim * cube_dim)
    next_face, dir_to = net_map[face][tuple(dir_)]
    new_pos = loc
    if dir_to == dir_: # Same direction - Rotate 180 and flip perpendicular position
        new_dir = clockwise(clockwise(dir_))
        if dir_[0] == 0:
            new_pos = (next_face[0] + cube_dim - 1 - (loc[0] - loc[0] // cube_dim * cube_dim), 
                       next_face[1] + (0 if dir_to[1] == -1 else (cube_dim - 1)))
        elif dir_[1] == 0:
            new_pos = (next_face[0] + (0 if dir_to[0] == -1 else (cube_dim - 1)),
                       next_face[1] + cube_dim - 1 - (loc[1] - loc[1] // cube_dim * cube_dim))
    elif dir_to == anticlockwise(dir_): # Clockwise motion - Rotate clockwise and translate position accordingly
        new_dir = clockwise(dir_)
        if dir_[0] == 1 and dir_[1] == 0:
            new_pos = (next_face[0] + cube_dim - 1 - (loc[1] - loc[1] // cube_dim * cube_dim), next_face[1])
        elif dir_[0] == -1 and dir_[1] == 0:
            new_pos = (next_face[0] + cube_dim - 1 - (loc[1] - loc[1] // cube_dim * cube_dim), next_face[1] + cube_dim - 1)
        elif dir_[0] == 0 and dir_[1] == 1:
            new_pos = (next_face[0] + cube_dim - 1, next_face[1] + loc[0] - loc[0] // cube_dim * cube_dim)
        elif dir_[0] == 0 and dir_[1] == -1:
            new_pos = (next_face[0], next_face[1] + loc[0] - loc[0] // cube_dim * cube_dim)
    elif dir_to == clockwise(dir_): # Anticlockwise motion - Rotate anti-clockwise and translate position accordingly
        new_dir = anticlockwise(dir_)
        if dir_[0] == 1 and dir_[1] == 0:
            new_pos = (next_face[0] + loc[1] - loc[1] // cube_dim * cube_dim, next_face[1] + cube_dim - 1)
        elif dir_[0] == -1 and dir_[1] == 0:
            new_pos = (next_face[0] + loc[1] - loc[1] // cube_dim * cube_dim, next_face[1])
        elif dir_[0] == 0 and dir_[1] == 1:
            new_pos = (next_face[0], next_face[1] + cube_dim - 1 - (loc[0] - loc[0] // cube_dim * cube_dim))
        elif dir_[0] == 0 and dir_[1] == -1:
            new_pos = (next_face[0] + cube_dim - 1, next_face[1] + cube_dim - 1 - (loc[0] - loc[0] // cube_dim * cube_dim))
    else: # Opposite directions - do not transform the direction, and maintain perpendicular position.
        new_dir = dir_
        if dir_[0] == 0:
            new_pos = (next_face[0] + (loc[0] - loc[0] // cube_dim * cube_dim), 
                       next_face[1] + (0 if dir_to[1] == -1 else (cube_dim - 1)))
        elif dir_[1] == 0:
            new_pos = (next_face[0] + (0 if dir_to[0] == -1 else (cube_dim - 1)),
                       next_face[1] + (loc[1] - loc[1] // cube_dim * cube_dim))
    return (new_pos, new_dir)

print("Problem 44:", passwd(*solve(board, width, height, desc, pos, dir_, cubewrap)))
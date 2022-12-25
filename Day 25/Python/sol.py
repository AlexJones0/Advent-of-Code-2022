"""
FILE: sol.py
Solution to day 25 problems (49 & 50) for Advent of Code 2022, solved in python.
"""

NOT_IMPLEMENTED = "Not Yet Implemented"
data = [x for x in open("Day 25/data.txt", "r").read().split("\n")]        

##### Problem 49 #####
encodings = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

def get_decimal(word):
    total = 0
    for char in word:
        total = total * 5 + encodings[char]
    return total

def get_snafu(word):
    snafu = ""
    next = None
    while word > 0:
        next = word % 5
        word = word // 5
        if next <= 2:
            snafu += str(next)
        elif next == 3:
            snafu += "="
            word += 1
        elif next == 4:
            snafu += "-"
            word += 1
    return snafu[::-1]
            

sum_ = 0
for word in data:
    total = 0
    for char in word:
        total = total * 5 + encodings[char]
    sum_ += total
            
print("Problem 49:", get_snafu(sum_))

##### Problem 50 ######

print("Problem 50:", "Freebie :)")
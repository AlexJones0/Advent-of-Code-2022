import os
from subprocess import call

day_dirs = [f.path for f in os.scandir(os.getcwd()) if f.is_dir() and \
                len(f.path.split(" ")) > 1 and f.path.split(" ")[-2].endswith("Day")]
day_dirs = sorted(day_dirs, key=lambda fn: int(fn.split("\\")[-1].split(" ")[1]))
for dir_ in day_dirs:
    sol_path = dir_ + "\\Python\\sol.py"
    if os.path.exists(sol_path):
        call(["python", sol_path])

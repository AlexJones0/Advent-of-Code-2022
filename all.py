import os
from subprocess import call

day_dirs = [f.path for f in os.scandir(os.getcwd()) if f.is_dir()]
for dir_ in day_dirs:
    sol_path = dir_ + "\\Python\\sol.py"
    if os.path.exists(sol_path):
        call(["python", sol_path])

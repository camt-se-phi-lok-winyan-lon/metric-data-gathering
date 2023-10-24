import cProfile
import glob
import os
import re
import subprocess

from pathlib import Path

root = os.getcwd()
print(root)
with open("./input.csv", 'r') as file:
    next(file)
    n = 0
    for line in file: 
        if len(line) == 0 : continue
        token = line.strip().split(",")
    lines = file.read().strip().split("\n")

    for line in lines:
        
        repo_url = token[2].strip()
        project_dir = os.path.join(root, f"tmp/Project-{n}")
        # os.makedirs(project_dir, exist_ok=True)
        
        # Clone the Git repository
        # subprocess.run(["git", "clone", repo_url, project_dir])
        os.chdir(project_dir)

        file_list = os.listdir(project_dir)
        
        py_files = list(Path(".").rglob("*.py"))

        c_result = cProfile.run( os.path.join(project_dir, "*.py") )
    
        # for py_file in py_files:
        #     command = f"python -m cProfile -o profile.stats {py_file}"
        #     c_result = subprocess.run(command, shell=True)
        #     print(c_result)
        
        n = n+1

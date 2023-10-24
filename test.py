import cProfile
import os
import re
import subprocess


root = os.getcwd()
print(root)
with open("./input.csv", 'r') as file:
    next(file)
    n = 0
    for line in file: 
        if len(line) == 0 : continue
        token = line.strip().split(",")
    # lines = file.read().strip().split("\n")

    # for line in lines:
        
        repo_url = token[2].strip()
        project_dir = os.path.join(root, f"tmp/Project-{n}")
        os.makedirs(project_dir, exist_ok=True)
        
        # Clone the Git repository
        subprocess.run(["git", "clone", repo_url, project_dir])
        os.chdir(project_dir)

        file_list = os.listdir(project_dir)
        py_files = [file for file in file_list if file.endswith('.py')]

        for file in py_files:
            print(file)
        
        n = n+1

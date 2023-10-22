import os
import subprocess
from datetime import datetime

def days_between(d1, d2):
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(d1, date_format).date()
    d2 = datetime.strptime(d2, date_format).date()
    return abs((d2 - d1).days)


def main(filename):

    root = os.getcwd()
    header = "number|name|repo|pylin|test|document|activeness\n"

    output = os.path.join(root, "output")
    with open(os.path.join(root, "text.txt"), 'w') as text_file:
                    text_file.write(header)

    print(root)
    with open(filename, 'r') as file:
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

            # You can uncomment the following lines if you want to install requirements and run pytest.
            subprocess.run(["pip", "install", "-r", "requirements.txt"])
            subprocess.run(["coverage", "run", "-m", "pytest"])

    #         # Write project information to text.txt
            with open(os.path.join(root, "text.txt"), 'a') as text_file:
                text_file.write(f"{n}|{token[0].strip()}|{repo_url}|")

            results = subprocess.run(["pylint", "./*"], stdout=subprocess.PIPE, text=True).stdout
            rating = [line for line in results.split('\n') if 'rated at' in line]
            if rating:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write(rating[0] + "|")
            else:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write("Your code has been rated at 0.00/10|")

    #       Run coverage and capture the TOTAL line
            coverage_output = subprocess.run(["python", "-m", "coverage", "report"], stdout=subprocess.PIPE, text=True).stdout
            total_line = [line for line in coverage_output.split('\n') if 'TOTAL' in line]
            if total_line:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write(total_line[0] + "|")
            else:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write("TOTAL                                       0     0    0%" + "|")

            try:
                with open('readme.md', 'r') as readme:
                    document_score = 0
                    content = readme.read()
                    content.strip()
                    if str(content).lower().find("document") != -1 : document_score = document_score + 1
                    if str(content).lower().find("installation") != -1 : document_score = document_score + 1
                    if str(content).lower().find("requirement") != -1 : document_score = document_score + 1
                    if str(content).lower().find("getting started") != -1 : document_score = document_score + 1
                    if str(content).lower().find("setup") != -1 : document_score = document_score + 1
                    with open(os.path.join(root, "text.txt"), 'a') as text_file:
                        text_file.write(f"{document_score}|")
            except FileNotFoundError:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write("0|")

            start_date = 0
            last_date = 0
            # Define the Git command as a list of arguments
            git_command = ["git", "log", "--reverse", "--format=format:%as", "--all"]

            # Run the Git command
            git_process = subprocess.Popen(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git_process.wait()
            # Read the first line of the Git log
            first_commit_timestamp = git_process.stdout.readline().decode().strip()

            # Check for errors
            if git_process.returncode == 0:
                start_date = first_commit_timestamp
            else:
                print("Error:", git_process.stderr.read().decode())

            # Define the Git command as a list of arguments
            git_command = ["git", "log", "--format=format:%as", "--all"]

            # Run the Git command
            git_process = subprocess.Popen(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git_process.wait()
            # Read the first line of the Git log
            first_commit_timestamp = git_process.stdout.readline().decode().strip()

            # Check for errors
            if git_process.returncode == 0:
                last_date = first_commit_timestamp
            else:
                print("Error:", git_process.stderr.read().decode())

            # days_between(start_date,last_date)

        
            git_command = ['git', 'rev-list' ,'--count' ,'--all']
            commit = subprocess.run(git_command, stdout=subprocess.PIPE, text=True).stdout
            # print(commit)

            try:
                activeness = int(commit)/days_between(start_date,last_date)
                print(activeness)
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write(str(activeness) + "\n")
            except ZeroDivisionError:
                with open(os.path.join(root, "text.txt"), 'a') as text_file:
                    text_file.write("0\n")
            n = n+1


    os.system("rm -rf ./tmp")

if __name__ == "__main__":
    # filename = input("Enter the filename: ")
    main('./input.csv')

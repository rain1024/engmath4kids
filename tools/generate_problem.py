import os
import sys
import shutil
from os.path import join

script_folder = os.path.dirname(os.path.realpath(__file__))
project_folder = os.path.dirname(script_folder)
problem_folder = os.path.join(script_folder, "template", "problem")

if __name__ == '__main__':
    # get first argument
    if len(sys.argv) < 2:
        print("Generate problem script")
        print("Usage:\n\tpython generate_problem.py <problem_id>")
        exit(1)
    problem_id = sys.argv[1]

    # copy template to new folder
    new_problem_folder = join(project_folder, "problems", problem_id)
    shutil.copytree(problem_folder, new_problem_folder)
    
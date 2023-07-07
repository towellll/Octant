import json
import sys

import numpy as np
from scipy.sparse import load_npz


def get_bug_list(bug_path):
    if bug_path.endswith(".npy"):
        bug_lines = np.load(bug_path)
        bug_lines = np.where(bug_lines == 1)[0]
        bug_lines = bug_lines.tolist()
    elif bug_path.endswith(".json"):
        with open(bug_path, 'r') as f:
            bug_lines = json.load(f)
    else:
        with open(bug_path, 'r') as f:
            bug_lines = f.read()
            bug_lines = eval(bug_lines)
        if not isinstance(bug_lines, list):
            print("\033[1;31mThe document file must contain a python list, please check.\033[0m")
            sys.exit(1)
    bug_lines = [int(x) for x in bug_lines]
    return bug_lines


def get_matrix(matrix_path):
    if matrix_path.endswith(".npy"):
        matrix = np.load(matrix_path)
    elif matrix_path.endswith(".npz"):
        matrix = load_npz(matrix_path).toarray()
    else:
        row_list = []
        with open(matrix_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                row = []
                for element in line.strip().split():
                    if element not in ["-", "+"]:
                        row.append(int(element))
                    else:
                        if element == "+":  # Passed
                            row.append(0)
                        else:  # Failed
                            row.append(1)
                row_list.append(row)
        matrix = np.array(row_list)
    return matrix

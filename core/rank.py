import os
import json
import sys
from utils.sbfl_compute import SBFL_compute
from utils.open_files import get_matrix, get_bug_list
from tabulate import tabulate
import numpy as np


class Rank(object):
    def __init__(self, matrix_path, bug_path, dest_path, formula):
        self.matrix_path = matrix_path
        self.bug_path = bug_path
        self.dest_path = dest_path
        self.formula = formula

    def compute_value(self):
        """
        For reading a matrix file
        :return:
        """
        all_sbfl = []
        line_matrix = get_matrix(self.matrix_path)
        error_vector = line_matrix[:, -1]
        for i in range(line_matrix.shape[1] - 1):
            pairs = list(zip(line_matrix[:, i], error_vector))  # need -1
            ef, ep, nf, np = pairs.count((1, 1)), pairs.count((1, 0)), pairs.count((0, 1)), pairs.count((0, 0))
            sbfl_compute = SBFL_compute(ef, ep, nf, np)
            sbfl_value = None
            if self.formula == 'dstar':
                sbfl_value = sbfl_compute.dstar()
            elif self.formula == 'ochiai':
                sbfl_value = sbfl_compute.ochiai()
            elif self.formula == 'barinel':
                sbfl_value = sbfl_compute.barinel()
            elif self.formula == 'ochiai2':
                sbfl_value = sbfl_compute.ochiai2()
            elif self.formula == 'gp02':
                sbfl_value = sbfl_compute.gp02()
            elif self.formula == 'gp03':
                sbfl_value = sbfl_compute.gp03()
            elif self.formula == 'gp13':
                sbfl_value = sbfl_compute.gp13()
            elif self.formula == 'gp19':
                sbfl_value = sbfl_compute.gp19()
            elif self.formula == 'jaccard':
                sbfl_value = sbfl_compute.jaccard()
            elif self.formula == 'wong2':
                sbfl_value = sbfl_compute.wong2()
            elif self.formula == 'tarantula':
                sbfl_value = sbfl_compute.tarantula()
            all_sbfl.append([i + 1, sbfl_value])
        return all_sbfl

    def rank(self):
        all_sbfl = self.compute_value()
        all_sbfl = sorted(all_sbfl, key=lambda x: x[1], reverse=True)
        all_sbfl = [[idx + 1, x[0], x[1]] for idx, x in enumerate(all_sbfl)]
        bug_list = get_bug_list(self.bug_path)
        bug_sbfl = [x for x in all_sbfl if x[1] in bug_list]
        output_path = os.path.join(self.dest_path, self.formula + "_sfl_rank.json")
        with open(output_path, 'w') as f:
            json.dump(bug_sbfl, f)
        headers = ["rank", "bug_line", self.formula]
        print(tabulate(bug_sbfl, headers=headers, tablefmt="grid"))
        rank_array = np.array(bug_sbfl)
        mfr = np.min(rank_array[:, 0])
        mar = np.mean(rank_array[:, 0])
        print(f"\033[1;32mMFR: {mfr}, MAR: {mar}.\033[0m")
        print(f"\033[1;32mBug rank of {self.bug_path} is saved at location {output_path}.\033[0m")

    def rank_all(self):
        all_sbfl = self.compute_value()
        all_sbfl = sorted(all_sbfl, key=lambda x: x[1], reverse=True)
        all_sbfl = [[idx + 1, x[0], x[1]] for idx, x in enumerate(all_sbfl)]
        all_sbfl = sorted(all_sbfl, key=lambda x: x[1], reverse=False)
        output_path = os.path.join(self.dest_path, self.formula + "_sfl_rank.json")
        with open(output_path, 'w') as f:
            json.dump(all_sbfl, f)
        headers = ["rank", "line", self.formula]
        print(tabulate(all_sbfl, headers=headers, tablefmt="grid"))
        print(f"\033[1;32mAll rank of {self.matrix_path} is saved at location {output_path}.\033[0m")

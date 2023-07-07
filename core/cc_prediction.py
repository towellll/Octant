import os
import copy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils.open_files import *


class CC_Prediction(object):
    def __init__(self, matrix_path, bug_path, dest_path):
        self.bug_path = bug_path
        self.matrix_path = matrix_path
        self.dest_path = dest_path

    def PTsetSplit(self, pt, n):
        shuffled = pt.sample(frac=1)
        result = np.array_split(shuffled, n)
        return result

    def locate(self):
        matrix = get_matrix(self.matrix_path)
        bug_indices = get_bug_list(self.bug_path)
        # Find row indexes where specified columns are 1 and the last element is 0
        cc_list = np.where((matrix[:, bug_indices] == 1).any(axis=1) & (matrix[:, -1] == 0))[0]
        cc_list = cc_list.tolist()
        cases_number = len(np.where(matrix[:, -1] == 0)[0])
        if cases_number:
            ratio = len(cc_list) * 100 / cases_number
        else:
            ratio = 0
        print(f"\033[1;32mThe number of passed cases is {cases_number}.\033[0m")
        print(f"\033[1;32mThe number of failed cases is {matrix.shape[0] - cases_number}.\033[0m")
        print(f"\033[1;32mThe number of bugs is {len(bug_indices)}.\033[0m")
        print(f"\033[1;32mThe number of CC is {len(cc_list)}.\033[0m")
        print(f"\033[1;32mThe ratio of CC is {ratio:.2f}%.\033[0m")
        return cc_list

    def prediction(self):
        matrix = get_matrix(self.matrix_path)
        data_df = pd.DataFrame(matrix)
        PT_data = data_df[data_df.iloc[:, -1] == 0]
        PT_data_copy = copy.deepcopy(PT_data)
        PT_len = len(PT_data_copy)
        FT_data = data_df[data_df.iloc[:, -1] == 1]
        K = max(int(len(PT_data) * 0.2), 1)  # 0.8 is selectable, and it repesents the percent of train test
        N = min(5, PT_data.shape[0] - K)
        if N == 0:
            return
        PT_data = PT_data.sample(frac=1)
        CT = []
        for i in range(0, len(PT_data), K):
            PT_split = self.PTsetSplit(pd.concat([PT_data.iloc[:i, :], PT_data.iloc[i + K:, :]]), N)
            PT_Test = PT_data.iloc[i:i + K, :]
            train = []
            RF_classifier = []
            Zm = []
            for j in range(N):
                Zm.append([])
            for j in range(N):
                train.append(pd.concat([PT_split[j], FT_data]))
                train_set = train[j].iloc[:, [m for m in range(PT_data.shape[1] - 1)]]
                train_label = train[j].iloc[:, [PT_data.shape[1] - 1]]
                test = PT_Test
                test_set = test.iloc[:, [m for m in range(PT_data.shape[1] - 1)]]
                test_label = test.iloc[:, [PT_data.shape[1] - 1]]
                RF = RandomForestClassifier(n_estimators=10, random_state=0)
                RF.fit(train_set, np.array(train_label.T)[0])
                RF_classifier.append(RF)
                for item in test_set.index:
                    loc_item = test_set.index.get_loc(item)
                    Zm[j].append(RF.score(test_set.iloc[loc_item, :].to_frame().values.reshape(-1, 1).T,
                                          test_label.iloc[loc_item, :].to_frame().values.reshape(-1, 1).T))
            for j in range(len(PT_Test)):
                cc_num = 0
                ncc_num = 0
                for Z in Zm:
                    if Z[j] == 1:
                        cc_num += 1
                    else:
                        ncc_num += 1
                if cc_num >= ncc_num:
                    CT.append(PT_Test.index.values.tolist()[j])
        CT_Bool = pd.DataFrame([False for _ in range(PT_len)], index=PT_data_copy.index.values.tolist())
        CT_Bool.loc[CT, :] = True
        final_CT = CT_Bool.values.T[0]
        ground_truth = np.where(data_df.iloc[:, -1] == 0)[0]
        cc_list = pd.Series(final_CT, index=ground_truth)
        cc_list = cc_list[cc_list].index
        cc_list = cc_list.tolist()
        cases_number = PT_data.shape[0]
        if cases_number:
            ratio = len(cc_list)*100 / cases_number
        else:
            ratio = 0
        print(f"\033[1;32mThe ratio of the predicted CC is {ratio:.2f}%.\033[0m")
        return cc_list

    def remove(self, cc_list):
        # Remove rows from the matrix
        matrix = get_matrix(self.matrix_path)
        filtered_matrix = np.delete(matrix, cc_list, axis=0)
        output_path = os.path.join(self.dest_path, "updated_matrix_remove.npy")
        np.save(output_path, filtered_matrix)
        print(f"\033[1;32mThe matrix after removing CC is saved at location {output_path}.\033[0m")

    def relabel(self, cc_list):
        matrix = get_matrix(self.matrix_path)
        matrix[cc_list, -1] = 1
        output_path = os.path.join(self.dest_path, "updated_matrix_relabel.npy")
        np.save(output_path, matrix)
        print(f"\033[1;32mThe matrix after relabeling CC is saved at location {output_path}.\033[0m")

    def save(self, cc_list, is_truth):
        if is_truth:
            output_path = os.path.join(self.dest_path, "cc_list.json")
        else:
            output_path = os.path.join(self.dest_path, "cc_rf_prediction_list.json")
        with open(output_path, "w") as f:
            json.dump(cc_list, f)
        print(f"\033[1;32mThe CC list of {self.matrix_path} is saved at location {output_path}.\033[0m")

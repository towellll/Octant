import argparse
import os
import sys
from core.rank import Rank
from core.cc_prediction import CC_Prediction
from utils.text_color import *
import warnings

warnings.filterwarnings("ignore")

def main():
    parser = argparse.ArgumentParser(
        description='Octant: A tool for analyzing coincidental correctness test cases and fault localization.')

    # Add arguments for each entry
    parser.add_argument('function',
                        choices=['predict', 'locate', 'ratio', 'remove', 'relabel', 'rank', 'sfl'],
                        help='Choose a function to run the tool.')

    # Add arguments
    parser.add_argument('-m', '--matrix', required=True, help='Specify a matrix file path.')
    parser.add_argument('-b', '--bug', required=True, help='Specify a buggy line file path.')
    parser.add_argument("-f", '--formula',
                        help="formula to compute the suspicious value, choose from ['dstar', 'ochiai', 'barinel',\
                         'ochiai2', 'gp02', 'gp03', 'gp13', 'gp19', 'jaccard','wong2', 'tarantula']",
                        choices=['dstar', 'ochiai', 'barinel', 'ochiai2', 'gp02', 'gp03', 'gp13', 'gp19', 'jaccard',
                                 'wong2', 'tarantula'])
    parser.add_argument('-d', '--dest',
                        help='Destination path to save the output, default is the matrix input directory.')

    parser.add_argument('-t', '--type', help="Choose cc list type, prediction or truth?",
                        choices=['prediction', 'truth'])

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    if args.matrix:
        if not os.path.exists(args.matrix):
            print(f"{RED}{BOLD}Matrix file not exist.{RESET}")
            sys.exit(1)

    if args.bug:
        if not os.path.exists(args.bug):
            print(f"{RED}{BOLD}Bug file not exist.{RESET}")
            sys.exit(1)

    if args.dest:
        if not os.path.isdir(args.dest):
            print(F"{RED}{BOLD}Please input a correct directory path.{RESET}")
            sys.exit(1)
        dest_path = args.dest
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
    else:
        dest_path = os.path.dirname(args.matrix)

    # Call the appropriate function based on the specified entry
    if args.function == 'predict':
        print(f"{CYAN}{BOLD}Predicting all CC based on given matrix and bug info. Please wait.{RESET}")
        predict = CC_Prediction(matrix_path=args.matrix, dest_path=dest_path, bug_path=args.bug)
        cc_list = predict.prediction()
        predict.save(cc_list, False)
    elif args.function == 'locate':
        print(f"{CYAN}{BOLD}Locating all CC based on given matrix and bug info. Please wait.{RESET}")
        predict = CC_Prediction(matrix_path=args.matrix, dest_path=dest_path, bug_path=args.bug)
        cc_list = predict.locate()
        predict.save(cc_list, True)
    elif args.function == 'remove':
        if args.type is None:
            print(f"{RED}{BOLD}Please specify a cc list type with -t.{RESET}")
            sys.exit(1)
        print(f"{CYAN}{BOLD}Removing all CC based on {args.type}. Please wait.{RESET}")
        predict = CC_Prediction(matrix_path=args.matrix, dest_path=dest_path, bug_path=args.bug)
        if args.type == "prediction":
            cc_list = predict.prediction()
        else:
            cc_list = predict.locate()
        predict.remove(cc_list)
    elif args.function == 'relabel':
        if args.type is None:
            print(f"{RED}{BOLD}Please specify a cc list type with -t.{RESET}")
            sys.exit(1)
        predict = CC_Prediction(matrix_path=args.matrix, dest_path=dest_path, bug_path=args.bug)
        print(f"{CYAN}{BOLD}Relabeling all CC based on {args.type}. Please wait.{RESET}")
        if args.type == "prediction":
            cc_list = predict.prediction()
        else:
            cc_list = predict.locate()
        predict.relabel(cc_list)
    elif args.function == 'rank':
        if args.formula is None:
            raise argparse.ArgumentTypeError("Please specify formula to compute the suspicious value, choose from \
                                             ['dstar', 'ochiai','barinel','ochiai2', 'gp02', 'gp03', 'gp13', 'gp19', \
                                             'jaccard','wong2', 'tarantula']")
        print(f"{CYAN}{BOLD}Ranking bugs based on {args.formula}. Please wait.{RESET}")
        rank = Rank(matrix_path=args.matrix,
                    bug_path=args.bug,
                    dest_path=dest_path,
                    formula=args.formula)
        rank.rank()
    elif args.function == 'sfl':
        if args.formula is None:
            raise argparse.ArgumentTypeError("Please specify formula to compute the suspicious value, choose from \
                                             ['dstar', 'ochiai','barinel','ochiai2', 'gp02', 'gp03', 'gp13', 'gp19', \
                                             'jaccard','wong2', 'tarantula']")
        print(f"{CYAN}{BOLD}Ranking all lines based on {args.formula}. Please wait.{RESET}")
        rank = Rank(matrix_path=args.matrix,
                    bug_path=args.bug,
                    dest_path=dest_path,
                    formula=args.formula)
        rank.rank_all()


if __name__ == '__main__':
    main()

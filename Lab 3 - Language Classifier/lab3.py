"""
Filename : classifier.py
Author : Archit Joshi (aj6082)
Description : CSCI630 - Lab 3 -> Wikipedia Language Classification
Language : python2
"""
import pickle
from sys import argv
# from decisionTree import *
from adaBoost import *
from decision import *


def main():
    """
    python lab3.py train <examples> <.model> <learning-type>
    python lab3.py predict <.model> <testdata_file>
    :return: None
    """

    if argv[1] == 'train':
        if argv[4] == 'ada':
            # INCOMPLETE Code
            adaTrainData(argv[2], argv[3])
        else:
            dtTrainData(argv[2], argv[3])
    elif argv[1] == 'predict':
        with open(argv[2], 'rb') as f:
            model = pickle.load(f)
            if model.type == 'ada':
                # INCOMPLETE Code
                adaPredict(argv[3], argv[2])
            else:
                dtPredict(argv[2], argv[3])


if __name__ == "__main__":
    main()

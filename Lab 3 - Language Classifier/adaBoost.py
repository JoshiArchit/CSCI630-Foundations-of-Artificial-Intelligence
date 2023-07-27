"""
Filename : adaBoost.py
Author : Archit Joshi (aj6082)
Description : CSCI630 - Lab 3 -> Wikipedia Language Classification
Language : python2
"""
import math

from decision import *


class Node:
    __slots__ = 'feature', 'correct', 'incorrect', 'trueBranch', 'falseBranch', 'trueBranchEntropy', 'falseBranchEntropy', 'totalEntropy', 'truePrediction', 'falsePrediction', 'type'

    def __init__(self, feature, trueBranch=None, falseBranch=None,
                 trueBranchEntropy=None, falseBranchEntropy=None,
                 totalEntropy=None, truePrediction = None, falsePrediction = None):
        self.feature = feature
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
        self.trueBranchEntropy = trueBranchEntropy
        self.falseBranchEntropy = falseBranchEntropy
        self.totalEntropy = totalEntropy
        self.truePrediction = truePrediction
        self.falsePrediction = falsePrediction
        self.type = 'ada'

    def __str__(self):
        return f"Feature {self.feature} \n TrueBranch : {self.trueBranch} \n FalseBranch : {self.falseBranch} \n TrueBranch Entropy : {self.trueBranchEntropy} \n FalseBranch Entropy : {self.falseBranchEntropy} \nTotal Entropy : {self.totalEntropy}"


def adaTrainData(file_in, file_out):
    """
    Function to train data.
    :param file_in: training data
    :param file_out: model
    :return:
    """
    frame = calculateFeatures(file_in)
    total = len(frame)
    initial_sample_weight = 1 / total
    df_col = [initial_sample_weight] * total
    frame['Sample_Weight'] = df_col

    stumps = []
    columns = frame.columns.values.tolist()

    for col in columns:
        if col != 7 and col != 'Sample_Weight':
            stumps.append(createStump(col, zip(frame[col], frame[7])))

    # Get best stump
    best_stump = None
    entropy = 1
    for stump in stumps:
        if entropy > stump.totalEntropy > 0:
            best_stump = stump
            entropy = stump.totalEntropy


    # Get alpha value for this iteration
    alpha = 0.5 * m.log((1 - initial_sample_weight) / initial_sample_weight)

    with open(file_out, 'wb') as f:
        pickle.dump(best_stump, f)


def createStump(feature, frame):
    """
    Create stumps
    :param feature: root feature
    :param frame: dataframe with features and label
    :return: stump
    """
    trueCorrect = 0
    trueIncorrect = 0
    trueIncorrectIndex = []
    falseCorrect = 0
    falseIncorrect = 0
    falseIncorrectIndex = []
    stump = Node(feature)
    true_en = 0
    false_en = 0
    true_nl = 0
    false_nl = 0

    i = 0
    if feature == 0 or feature == 1 or feature == 2 or feature == 3 or feature == 4 or feature == 5:
        # calculate correctly classified and incorrectly classified
        for item in frame:
            if item[0] == 'Yes':  # true branch
                if item[1] == 'en':
                    trueCorrect += 1
                    true_en += 1
                else:
                    trueIncorrect += 1
                    trueIncorrectIndex.append(i)
                    true_nl += 1
            elif item[0] == 'No':  # false branch
                if item[1] == 'nl':
                    falseCorrect += 1
                    false_en += 1
                else:
                    falseIncorrect += 1
                    falseIncorrectIndex.append(i)
                    false_nl += 1
        stump.trueBranch = (trueCorrect, trueIncorrect)
        stump.falseBranch = (falseCorrect, falseIncorrect)
        i += 1
        if true_en > false_en:
            stump.truePrediction = 'en'
        else:
            stump.truePrediction = 'nl'
        if true_nl > false_nl:
            stump.falsePrediction = 'nl'
        else:
            stump.falsePrediction = 'en'

    elif feature == 6:
        for item in frame:
            if item[0] == 'Yes':
                if item[1] == 'en':
                    trueCorrect += 1
                    true_en += 1
                else:
                    trueIncorrect += 1
                    trueIncorrectIndex.append(i)
                    true_nl += 1
            elif item[0] == 'No':
                if item[1] == 'nl':
                    falseCorrect += 1
                    false_nl += 1
                else:
                    falseIncorrect += 1
                    falseIncorrectIndex.append(i)
                    false_en += 1
        stump.trueBranch = (trueCorrect, trueIncorrect)
        stump.falseBranch = (falseCorrect, falseIncorrect)
        i += 1
        if true_en > false_en:
            stump.truePrediction = 'en'
        else:
            stump.truePrediction = 'nl'
        if true_nl > false_nl:
            stump.falsePrediction = 'nl'
        else:
            stump.falsePrediction = 'en'

    # True Branch Entropy
    totalTrueBranch = trueCorrect + trueIncorrect
    try:
        entropyCorrect = -(trueCorrect / totalTrueBranch * m.log2(
            trueCorrect / totalTrueBranch))
        entropyIncorrect = -(trueIncorrect / totalTrueBranch) * m.log2(
            trueIncorrect / totalTrueBranch)
        trueBranchEntropy = entropyCorrect + entropyIncorrect
    except:
        trueBranchEntropy = 0
    stump.trueBranchEntropy = trueBranchEntropy

    # False Branch Entropy
    totalFalseBranch = falseCorrect + falseIncorrect
    try:
        entropyCorrect = -(falseCorrect / totalFalseBranch * m.log2(
            falseCorrect / totalFalseBranch))
        entropyIncorrect = -(falseIncorrect / totalFalseBranch * m.log2(
            falseIncorrect / totalFalseBranch))
        falseBranchEntropy = entropyCorrect + entropyIncorrect
    except:
        falseBranchEntropy = 0
    stump.falseBranchEntropy = falseBranchEntropy

    # Total entropy for stump
    totalEntropy = (totalTrueBranch / (
            totalTrueBranch + totalFalseBranch) * trueBranchEntropy) + \
                   (totalFalseBranch / (
                           totalTrueBranch + totalFalseBranch) * falseBranchEntropy)
    stump.totalEntropy = totalEntropy

    return stump


def adaPredict(data, file):
    """
    Predict adaBoost.

    :param data: input data
    :param file: model file
    :return:
    """

    features = calculateFeaturesPredict(data)
    with open(file, 'rb') as f:
        model = pickle.load(f)
    feature = model.feature
    feature_lst = features.values
    flagT = False
    flagF = False
    for line in feature_lst:
        if line[feature] == 'Yes':
            node = model.trueBranch
            flagT = True
        else:
            node = model.falseBranch
            flagF = True

        if flagT:
            print(model.truePrediction)
        elif flagF:
            print(model.falsePrediction)



# def main():
#     file = 'train.dat'
#     hypo = 'best.model'
#     adaTrainData(file, hypo)
#     adaPredict(file, hypo)
#
#
# if __name__ == '__main__':
#     main()

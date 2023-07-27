"""
Filename : decisionTree.py
Author : Archit Joshi (aj6082)
Description : CSCI630 - Lab 3 -> Wikipedia Language Classification
Language : python2
"""

import re
import numpy as np
import pandas as pd
import pickle
import math as m

class Node:
    """
    Decision tree node.
    """
    __slots__ = 'feature', 'gain', 'trueBranch', 'falseBranch', 'threshold', 'data', 'label', 'leftSplit', 'rightSplit'

    def __init__(self, feature, gain, left=None, right=None, data=None,
                 label=None, leftSplit=None, rightSplit=None):
        self.feature = feature
        self.gain = gain
        self.trueBranch = left
        self.falseBranch = right
        self.leftSplit = leftSplit
        self.rightSplit = rightSplit

    def str(self):
        return f'node : {self.feature}, left: {self.trueBranch}, right : {self.falseBranch}'


class DTree:
    """
    Decision Tree
    """
    __slots__ = 'root', 'min_sample_split', 'max_depth', 'type'

    def __init__(self, root=None, max_depth=5):
        self.root = root
        self.type = 'dt'
        self.max_depth = max_depth


def dtTrainData(trainingData, hypothesisOut):
    """
    Train data using decision tree.

    :param trainingData: input training data
    :param hypothesisOut: output file name for model
    :return: decision tree
    """
    features = calculateFeatures(trainingData)
    features_left = [x for x in range(7)]
    gain, featureIndex = calcInformationGain(features)
    tree = DTree(Node(featureIndex, gain, None, None))
    features_left.pop(featureIndex)

    leftData, rightData = partitionData(features, featureIndex)
    tree.root.leftSplit = leftData[7].tolist()
    tree.root.rightSplit = rightData[7].tolist()

    # Create left subtree
    tree.root.trueBranch, features_left = createDecisionTree(leftData,
                                                             features_left,
                                                             tree.root)
    rightData = cleanRight(rightData, features_left)
    # Create right subtree
    tree.root.falseBranch, features_left = createDecisionTree(rightData,
                                                              features_left,
                                                              tree.root)

    with open(hypothesisOut, 'wb') as f:
        pickle.dump(tree, f)
    return tree


def createDecisionTree(data, features_left, parent):
    """
    Recursive function to create decision tree.

    :param data: data frame
    :param features_left: features left for nodes
    :param parent: parent of current node
    :return: left/right child of parent or label as leaf node
    """

    if len(features_left) == 0:
        return plurality(parent), features_left
    # Same classification
    elif len(set(data[7])) == 1:
        label = set(data[7])
        return next(iter(label)), features_left
    elif len(data) == 1:
        label = data[7]
        return label, features_left
    elif len(data.columns) == 1:
        return plurality(data), features_left
    elif data is None:
        return plurality(parent), features_left

    gain, featureIndex = calcInformationGain(data)
    if gain == 0:
        return plurality(parent), features_left
    if gain < 0.02:
        return plurality(parent), features_left

    features_left.remove(featureIndex)

    node = Node(featureIndex, gain, None, None)

    leftData, rightData = partitionData(data, featureIndex)
    node.leftSplit = leftData[7].tolist()
    node.rightSplit = rightData[7].tolist()

    node.trueBranch, features_left = createDecisionTree(leftData,
                                                        features_left, node)
    rightData = cleanRight(rightData, features_left)

    node.falseBranch, features_left = createDecisionTree(rightData,
                                                         features_left, node)

    return node, features_left


def plurality(node):
    """
    Calculate plurality of a node.

    :param node: Decision tree node
    :return: plurality
    """
    data = node.rightSplit

    count_en = 0
    count_nl = 0

    for item in data:
        if item == 'en':
            count_en += 1
        else:
            count_nl += 1

    if count_en > count_nl:
        return 'en'
    else:
        return 'nl'


def cleanRight(data, features):
    for column in data:
        if column != 7:
            if column not in features:
                data.drop([column], axis=1, inplace=True)
    return data


def partitionData(features, featureIndex):
    """
    Partition data for left and right subtree.

    """
    lst = list(features.columns.values)
    columns = []
    for item in lst:
        if item != featureIndex:
            columns.append(item)

    left = pd.DataFrame(columns=columns)  # True Branch
    right = pd.DataFrame(columns=columns)  # False Branch

    for index, row in features.iterrows():
        if row[featureIndex] == 'Yes':
            left.loc[index] = row
        else:
            right.loc[index] = row

    return left, right


def calcInformationGain(features):
    """
    Calculate information gain.

    """
    gain = dict()
    shape = features.shape
    rows = shape[0]
    columns = shape[1]
    column_vals = features.columns.tolist()
    column_vals.pop()

    for i in column_vals:
        attrEntropy, parentEntropy = calcEntropy(i, rows, zip(features[i],
                                                              features[7]))
        informationGain = parentEntropy - attrEntropy
        gain[i] = informationGain

    max_gain_feature = max(gain, key=gain.get)
    max_gain = gain[max_gain_feature]

    return max_gain, max_gain_feature


def calcEntropy(iteration, total, column):
    """
    Calculate entropy.

    """
    total_en = 0
    total_nl = 0
    yes_en = 0
    no_en = 0
    yes_nl = 0
    no_nl = 0

    for data in column:
        if data[1] == 'en':
            total_en += 1
            if data[0] == 'Yes':
                yes_en += 1
            else:
                no_en += 1
        else:
            total_nl += 1
            if data[0] == 'Yes':
                yes_nl += 1
            else:
                no_nl += 1

    totalYes = (yes_nl + yes_en) / (total_en + total_nl)
    totalNo = (no_nl + no_en) / (total_en + total_nl)

    try:
        entropyYes = - ((yes_en / (yes_en + yes_nl)) * m.log2(
            (yes_en / (yes_en + yes_nl)))) \
                     - ((yes_nl / (yes_en + yes_nl)) * m.log2(
            (yes_nl / (yes_en + yes_nl))))
    except:
        entropyYes = 0

    try:
        entropyNo = - ((no_en / (no_en + no_nl)) * m.log2(
            (no_en / (no_en + no_nl)))) \
                    - ((no_nl / (no_en + no_nl)) * m.log2(
            (no_nl / (no_en + no_nl))))
    except:
        entropyNo = 0

    try:
        parentEntropy = - (total_en / (total_en + total_nl)) * m.log2(
            (total_en / (total_en + total_nl))) \
                        - (total_nl / (total_en + total_nl)) * m.log2(
            (total_nl / (total_en + total_nl)))
    except:
        parentEntropy = 0

    attrEntropy = (totalYes * entropyYes) + (totalNo * entropyNo)

    return attrEntropy, parentEntropy


def calculateFeaturesPredict(predictData):
    """
    Calculate features for given data for predicting.
    """

    f = open(predictData, 'r', encoding='UTF-8')
    line_list = []
    for line in f:
        feature_lst = [None] * 7
        line = line.split()
        checkArticleAgain = checkDutchPronounAgain = \
            checkIJAgain = checkDupAgain = checkWordLenAgain \
            = checkCommonWord = checkEArticle = True

        for word in line:
            word = re.sub(r'(\w+)[^\w\s]*$', r'\1', word)

            if checkArticleAgain is True:
                if checkDutchArticle(word.lower()):  # True
                    feature_lst[0] = 'No'
                    checkArticleAgain = False
                else:
                    feature_lst[0] = 'Yes'

            # Check if Dutch pronoun
            if checkDutchPronounAgain is True:
                if checkDutchPronoun(word.lower()):
                    feature_lst[1] = 'No'
                    checkDutchPronounAgain = False
                else:
                    feature_lst[1] = 'Yes'

            # Check if 'ij' end the word
            if checkIJAgain is True:  # Dutch word
                if 'ij' in word.lower()[-2:]:
                    feature_lst[2] = 'No'
                    checkIJAgain = False
                else:
                    feature_lst[2] = 'Yes'

            # Check for consecutive duplicate letters
            if checkDupAgain is True:
                if checkIfDuplicate(word.lower()):
                    feature_lst[3] = 'No'
                else:
                    feature_lst[3] = 'Yes'

            # # Check word length
            if checkWordLenAgain is True:
                if checkAverageWordLength(line) > 5:
                    feature_lst[4] = 'No'
                    checkWordLenAgain = False
                else:
                    feature_lst[4] = 'Yes'

            # Check if the word is common Dutch word
            if checkCommonWord is True:
                if commonDutchWords(word.lower()):
                    feature_lst[5] = 'No'
                    checkCommonWord = False
                else:
                    feature_lst[5] = 'Yes'

            if checkEArticle is True:
                if checkEnglishArticle(word.lower()):
                    feature_lst[6] = 'Yes'
                    checkEArticle = False
                else:
                    feature_lst[6] = 'No'

        line_list.append(feature_lst)
    numpyarray = np.array(line_list)
    features = pd.DataFrame(numpyarray)

    return features


def calculateFeatures(trainingData):
    """
    Calculate features for training decision tree.

    """
    f = open(trainingData, 'r', encoding='UTF-8')
    line_list = []
    for line in f:
        # list of features and a class
        feature_lst = [None] * 8
        line = line.split()
        item = line[0].split('|')
        line.pop(0)
        for _ in reversed(item):
            line.insert(0, _)

        checkLabel = checkArticleAgain = checkDutchPronounAgain = \
            checkIJAgain = checkDupAgain = checkWordLenAgain \
            = checkCommonWord = checkEArticle = True

        for word in line:
            word = re.sub(r'(\w+)[^\w\s]*$', r'\1', word)
            # Check label for test line
            if checkLabel is True:
                if line[0] == 'en':
                    feature_lst[7] = 'en'
                else:
                    feature_lst[7] = 'nl'
                checkLabel = False
            # Label checked. Move on to attributes. "No" signifies that its not English language
            else:
                # Check if Dutch article
                if checkArticleAgain is True:

                    if checkDutchArticle(word.lower()):  # True
                        feature_lst[0] = 'No'
                        checkArticleAgain = False
                    else:
                        feature_lst[0] = 'Yes'

                # Check if Dutch pronoun
                if checkDutchPronounAgain is True:
                    if checkDutchPronoun(word.lower()):
                        feature_lst[1] = 'No'
                        checkDutchPronounAgain = False
                    else:
                        feature_lst[1] = 'Yes'

                # Check if 'ij' end the word
                if checkIJAgain is True:  # Dutch word
                    if 'ij' in word.lower()[-2:]:
                        feature_lst[2] = 'No'
                        checkIJAgain = False
                    else:
                        feature_lst[2] = 'Yes'

                # Check for consecutive duplicate letters
                if checkDupAgain is True:
                    if checkIfDuplicate(word.lower()):
                        feature_lst[3] = 'No'
                    else:
                        feature_lst[3] = 'Yes'

                # # Check word length
                if checkWordLenAgain is True:
                    if checkAverageWordLength(line) > 5:
                        feature_lst[4] = 'No'
                        checkWordLenAgain = False
                    else:
                        feature_lst[4] = 'Yes'

                # Check if the word is common Dutch word
                if checkCommonWord is True:
                    if commonDutchWords(word.lower()):
                        feature_lst[5] = 'No'
                        checkCommonWord = False
                    else:
                        feature_lst[5] = 'Yes'

                if checkEArticle is True:
                    if checkEnglishArticle(word.lower()):
                        feature_lst[6] = 'Yes'
                        checkEArticle = False
                    else:
                        feature_lst[6] = 'No'

        line_list.append(feature_lst)
    numpyarray = np.array(line_list)
    features = pd.DataFrame(numpyarray)

    return features


def checkDutchArticle(word):
    dutchArticles = ['de', 'het', 'een']
    if word in dutchArticles:
        return True
    return False


def checkDutchPronoun(word):
    dutchPronouns = ['ik', 'jij', 'u', 'hij', 'zij', 'het', 'wij', 'jullie',
                     'mij', 'jou', 'hem', 'haar', 'ons', 'hen', 'mijn', 'jouw',
                     'uw', 'zijn', 'haar', 'ons', 'hun', 'mezelf', 'jezelf',
                     'zichzelf']

    if word in dutchPronouns:
        return True
    return False


def checkIfDuplicate(word):
    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            return True
    return False


def checkEnglishArticle(word):
    articles = ['a', 'an', 'the']
    if word in articles:
        return True
    return False


def checkAverageWordLength(line):
    words = 15
    total = 0
    line = line[1:]
    for word in line:
        word = re.sub(r'(\w+)[^\w\s]*$', r'\1', word)
        total += len(word)
    return total / words


def commonDutchWords(word):
    """
    Checking for the presence of common dutch words
    :param statement:Input Statement
    :return:Boolean value representing the presence or absence of the common dutch words
    """
    commonWords = ['van', 'een', 'op', 'aan', 'met', 'voor', 'er', 'maar', 'om'
        , 'tegen', 'naar', 'bij', 'tot', 'uit', 'door', 'dus', 'nog', 'dan',
                   'wel',
                   'echter', 'meest', 'meer', 'alleen']

    if word.lower() in commonWords:
        return True
    return False


def checkEnglishPronouns(word):
    pronouns = ['i', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours',
                'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                'her', 'hers', 'herself', 'it', 'its', 'itself', 'we', 'us',
                'our', 'ours', 'ourselves', 'they', 'them', 'their', 'theirs',
                'themselves']
    if word in pronouns:
        return True
    return False


def dtPredict(model, data):
    """
    Traverse the trained model and predict label.
    """

    features = calculateFeaturesPredict(data)
    with open(model, 'rb') as f:
        model = pickle.load(f)
    feature = model.root.feature
    feature_lst = features.values
    for lst in feature_lst:
        node = model.root
        while True:
            if lst[feature] == 'Yes':
                node = node.trueBranch
            else:
                node = node.falseBranch
            if node == 'en' or node == 'nl':
                print(node)
                break

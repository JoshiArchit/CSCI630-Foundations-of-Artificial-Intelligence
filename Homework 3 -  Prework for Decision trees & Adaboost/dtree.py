"""
Filename : dtree.py
Author : Archit Joshi
Description : Decision Tree and Adaboost prework
Language : Python3
"""

import math as m

path = 'data.txt'

# Decide which attribute needs to be selected for a split on root node
level0Gain = []
for i in range(8):
    with open(path) as f:
        count_A = 0
        count_B = 0
        trueA = 0
        trueB = 0
        falseA = 0
        falseB = 0

        for line in f:
            line = line.strip().split()
            if line[8] == 'A':
                if line[i] == 'True':
                    trueA += 1
                else:
                    falseA += 1
                count_A += 1
            else:
                if line[i] == 'True':
                    trueB += 1
                else:
                    falseB += 1
                count_B += 1

        totalTrue = (trueA + trueB) / (count_A + count_B)

        totalFalse = (falseA + falseB) / (count_A + count_B)

        entropyTrue = - ((trueA / (trueA + trueB)) * m.log(
            (trueA / (trueA + trueB)), 2)) \
                      - ((trueB / (trueA + trueB)) * m.log(
            (trueB / (trueA + trueB)), 2))

        entropyFalse = - ((falseA / (falseA + falseB)) * m.log(
            (falseA / (falseA + falseB)), 2)) \
                       - ((falseB / (falseA + falseB)) * m.log(
            (falseB / (falseA + falseB)), 2))

        parentEntropy = - (count_A / (count_A + count_B)) * m.log(
            (count_A / (count_A + count_B)), 2) \
                        - (count_B / (count_A + count_B)) * m.log(
            (count_B / (count_A + count_B)), 2)
        entropyAttr = (totalTrue * entropyTrue) + (totalFalse * entropyFalse)
        informationGain = parentEntropy - entropyAttr
        level0Gain.append(informationGain)

maxGain = max(level0Gain)
index0 = level0Gain.index(maxGain)
print(f'Attribute A{index0 + 1} to get to Level 1')
print(f'Gain using attribute A{index0 + 1} " {maxGain}')
print(f'A True : {trueA}')
print(f'B True : {trueB}')
print()

# Decide which attribute needs to be used for a split on root nodes True split
level1TrueGain = []
for i in range(8):
    if i == index0:
        level1TrueGain.append(0)
        continue
    with open(path) as f:
        count_A = 0
        count_B = 0
        trueA = 0
        trueB = 0
        falseA = 0
        falseB = 0

        for line in f:
            line = line.strip().split()
            # True split at index1
            if line[index0] == 'True':
                if line[8] == 'A':
                    if line[i] == 'True':
                        trueA += 1
                    else:
                        falseA += 1
                    count_A += 1
                else:
                    if line[i] == 'True':
                        trueB += 1
                    else:
                        falseB += 1
                    count_B += 1

        totalTrue = (trueA + trueB) / (count_A + count_B)

        totalFalse = (falseA + falseB) / (count_A + count_B)

        entropyTrue = - ((trueA / (trueA + trueB)) * m.log(
            (trueA / (trueA + trueB)), 2)) \
                      - ((trueB / (trueA + trueB)) * m.log(
            (trueB / (trueA + trueB)), 2))

        entropyFalse = - ((falseA / (falseA + falseB)) * m.log(
            (falseA / (falseA + falseB)), 2)) \
                       - ((falseB / (falseA + falseB)) * m.log(
            (falseB / (falseA + falseB)), 2))

        parentEntropy = - (count_A / (count_A + count_B)) * m.log(
            (count_A / (count_A + count_B)), 2) \
                        - (count_B / (count_A + count_B)) * m.log(
            (count_B / (count_A + count_B)), 2)
        entropyAttr = (totalTrue * entropyTrue) + (totalFalse * entropyFalse)
        informationGain = parentEntropy - entropyAttr
        level1TrueGain.append(informationGain)

maxGain = max(level1TrueGain)
index_1_True = level1TrueGain.index(maxGain)
print(f'Attribute A{index_1_True + 1} for True node split')
print(f'Gain using attribute A{index_1_True + 1} : {maxGain}')
print(f'A True : {trueA}')
print(f'B True : {trueB}')
print()

# Decide which attribute needs to be used for a split on root nodes False split
level1FalseGain = []
for i in range(8):
    if i == index0:
        level1FalseGain.append(0)
        continue
    with open(path) as f:
        count_A = 0
        count_B = 0
        trueA = 0
        trueB = 0
        falseA = 0
        falseB = 0

        for line in f:
            line = line.strip().split()
            # False split at index0
            if line[index0] == 'False':
                if line[8] == 'A':
                    if line[i] == 'True':
                        trueA += 1
                    else:
                        falseA += 1
                    count_A += 1
                else:
                    if line[i] == 'True':
                        trueB += 1
                    else:
                        falseB += 1
                    count_B += 1

        totalTrue = (trueA + trueB) / (count_A + count_B)

        totalFalse = (falseA + falseB) / (count_A + count_B)

        entropyTrue = - ((trueA / (trueA + trueB)) * m.log(
            (trueA / (trueA + trueB)), 2)) \
                      - ((trueB / (trueA + trueB)) * m.log(
            (trueB / (trueA + trueB)), 2))

        entropyFalse = - ((falseA / (falseA + falseB)) * m.log(
            (falseA / (falseA + falseB)), 2)) \
                       - ((falseB / (falseA + falseB)) * m.log(
            (falseB / (falseA + falseB)), 2))

        parentEntropy = - (count_A / (count_A + count_B)) * m.log(
            (count_A / (count_A + count_B)), 2) \
                        - (count_B / (count_A + count_B)) * m.log(
            (count_B / (count_A + count_B)), 2)
        entropyAttr = (totalTrue * entropyTrue) + (totalFalse * entropyFalse)
        informationGain = parentEntropy - entropyAttr
        level1FalseGain.append(informationGain)

maxGain = max(level1FalseGain)
index_1_False = level1FalseGain.index(maxGain)
print(f'Attribute A{index_1_False + 1} for False node split')
print(f'Gain using attribute A{index_1_False + 1} : {maxGain}')
print(f'A True : {trueA}')
print(f'B True : {trueB}')



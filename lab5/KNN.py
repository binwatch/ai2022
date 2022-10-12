import numpy as np
import operator
from os import listdir

def classify0(inX, dataSet, labels, k):
    m = dataSet.shape[0]
    diffMat = np.tile(inX, (m, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter)
    return sortedClassCount[0][0]

dataSet = np.array([[250, 100], [270, 120], [111, 230], [130, 260], [200, 80], [70, 190]])
labels = ["s", "s", "a", "a", "s", "a"]
inX = [105, 210]
print(classify0(inX, dataSet, labels, 3))
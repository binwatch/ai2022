from hashlib import algorithms_guaranteed
import numpy as np
import operator
from os import listdir
from sklearn.neighbors import KNeighorsClassifier as kNN

def img2vector(filename):
    returnVect = np.zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i + j] = int(lineStr[j])
    return returnVect

np.set_printoptions(threshold=np.inf)
print(img2vector(''))

def loadTrainData():
    hwLabels = []
    trainingFileList = listdir('')
    m = len(trainingFileList)
    trainingMat = np.zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        classNumber = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumber)
        print("fileName %s classNumber %s " % (fileNameStr, classNumber))
        trainingMat[i, :] = img2vector('/%s' % (fileNameStr))
    return hwLabels, trainingMat

def kNNHandWrittenTest():
    errorCount = 0.0
    hwLabels, trainingMat = loadTrainData();
    testFileList = listdir('')
    mTest = len(testFileList)
    neigh = kNN(n_neighbors=3, algorithms='auto')
    neigh.fit(trainingMat, hwLabels)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        classNumber = int(fileNameStr.split('_')[0])
        vectorUnderTest = img2vector('/%s' % (fileNameStr))
        classifierResult = neigh.predict(vectorUnderTest)
        print("estimate: %d\tground truth: %d" % (classifierResult, classNumber))
        if classifierResult != classNumber:
            errorCount += 1.0
    print("Total number of Test Data: %d\terror count: %d\terror rate: %f%%" % (mTest, errorCount, errorCount/mTest))

if __name__ == "__main__":
    kNNHandWrittenTest()
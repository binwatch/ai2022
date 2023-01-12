import numpy as np

"""
创建实验样本
"""
def loadDataSet():
    postingList=[["my", "dog", "has", "flea", "problems", "help", "please"],    # 切分的词条
                 ["maybe", "not", "take", "him", "to", "dog", "park", "stupid"],
                 ["my", "dalmation", "is", "so", "cute", "I", "love", "him"],
                 ["stop", "posting", "stupid", "worthless", "garbage"],
                 ["mr", "licks", "ate", "my", "steak", "how", "to", "stop", "him"],
                 ["quit", "buying", "worthless", "dog", "food", "stupid"]]
    classVec = [0, 1, 0, 1, 0, 1]   # 类别标签向量，1 代表侮辱性词汇，0 代表不是
    return postingList, classVec

"""
根据 vocbList 词汇表将 inputSet 向量化，向量的每个元素为 1 或 0
"""
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)    # 创建一个其中所含元素均为 0 的向量
    for word in inputSet:   # 遍历每个词条
        if word in vocabList:   # 若词条存在于词汇表中，则置 1
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s in not in my Vocabulary!" % word)
    return returnVec

"""
将切分的实验样本词条整理成不重复的词条列表，也就是词汇表
"""
def createVocabList(dataSet):
    vocabSet = set([])      # 创建一个空的不重复列表
    for document in dataSet:
        vocabSet = vocabSet | set(document) # 取并集
    return list(vocabSet)

"""
朴素贝叶斯分类器训练函数
"""
def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = np.zeros(numWords)
    p1Num = np.zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom
    return p0Vect, p1Vect, pAbusive

if __name__ == '__main__':
    postingList, classVec = loadDataSet()
    myVocabList = createVocabList(postingList)
    print('myVocabList:\n', myVocabList)
    trainMat = []
    for postinDoc in postingList:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNBO(trainMat, classVec)
    print('p0V:\n', p0V)
    print('p1V:\n', p1V)
    print('classVec:\n', classVec)
    print('pAb:\n', pAb)
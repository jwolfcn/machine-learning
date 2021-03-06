from math import log
import operator
from os import listdir
from numpy import zeros, tile

def calcShannonEnt(dataSet):
    labels = {}
    shannon = 0
    numEnt = len(dataSet)
    for data in dataSet:
        currentLabel = data[-1]
        if (currentLabel not in labels.keys()):
            labels[currentLabel] = 0
        labels[currentLabel] = labels[currentLabel] + 1
    for label in labels.keys():
        p = labels[label]/float(numEnt)
        shannon = shannon - p * log(p, 2)
    return shannon

def createDataSet():
    dataSet = [[1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    rntData = []
    for data in dataSet:
        if data[axis] == value:
            reduceData = data[:axis]
            reduceData.extend(data[axis + 1:])
            rntData.append(reduceData)
    return rntData
    
def chooseBestFeatureToSplit(dataSet):
    num = len(dataSet[0]) - 1
    baseShannon = calcShannonEnt(dataSet)
    bestFeatureIndex = -1
    bestShannon = 0.0
    totalLen = len(dataSet)
    for i in range(num): 
        featureList = [item[i] for item in dataSet]
        uniqueFeatures = set(featureList)
        shannon = 0.0
        for feature in uniqueFeatures: 
            subDataSet = splitDataSet(dataSet, i, feature)
            p = float(len(subDataSet))/totalLen
            shannon += p * calcShannonEnt(subDataSet)
        print "by feature %d, shannon is %f" % (i, shannon)
        gainShannon = baseShannon - shannon
        if gainShannon > bestShannon:
            bestShannon = gainShannon
            bestFeatureIndex = i
    return bestFeatureIndex

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClass = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClass[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    subLabels = labels[:]
    del(subLabels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree
       

def storeTree(inputTree, filenames):
    import pickle
    fw = open(filenames, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

# return [0,0,0,...0,0,0]
def img2vector(filename):
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        line = [int(lineStr[j]) for j in range(32)]
        returnVect.extend(line)
    return returnVect

def getTraningMat():
    hwLabels = []
    trainingFileList = listdir('../chapter2/digits/trainingDigits/')           #load the training set
    m = len(trainingFileList)
    trainingMat = []
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        item = img2vector('../chapter2/digits/trainingDigits/%s' % fileNameStr)
        item.append(classNumStr)
        trainingMat.append(item)
    return trainingMat

def predictByTree(myTree, data):
    isLeaf = False
    root = myTree
    while not isLeaf:
        label = root.keys()[0]
        indi = data[int(label)]
        root = root[label][indi]
        isLeaf = isinstance(root, int)
    return root

def testPredictByTree(tree):
    testFileList = listdir('../chapter2/digits/testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('../chapter2/digits/testDigits/%s' % fileNameStr)
        classifierResult = int(predictByTree(tree, vectorUnderTest))
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\n %f %% are right" % ((1-errorCount/float(mTest))*100)


    #  dataSet = trees.getTraningMat()
    #  labels = [str(item) for item in range(1024)]
    #  mytree = trees.createTree(dataSet,labels)
    #  wait for 210 s
    #  trees.testPredictByTree(mytree) 
    #  88.054968 % are right
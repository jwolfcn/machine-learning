from numpy import *
from os import listdir

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary" % word
    return returnVec

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

def getDocMat(vocabList, listOPosts):
    mat = []
    for post in listOPosts:
        mat.append(bagOfWords2VecMN(vocabList, post))
    return mat

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            print trainMatrix[i]
            print sum(trainMatrix[i])
            print p1Denom
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
            # print sum(trainMatrix[i])
            # print p0Denom
    print p1Num
    print sum(p1Num)
    print p1Denom
    # print p0Num
    # print sum(p0Num)
    # print p0Denom
    p1Vect = p1Num/p1Denom # log(p1Num/p1Denom)
    p0Vect = p0Num/p0Denom # log(p0Num/p1Denom)
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    print "vec2Classify:", vec2Classify
    # p1 = sum(vec2Classify * p1Vec) + log(pClass1) # why? if w = 1 : log(p(w=1|c1)); if w = 0: log(p(w=0|c1)) = log(1 - p(w=1|c1)) almost 0
    # p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
    p1 = logProp(vec2Classify, p1Vec) + log(pClass1)
    p0 = logProp(vec2Classify, p0Vec) + log(1 - pClass1)    
    if p1 > p0:
        return 1
    else:
        return 0

def logProp(vec2Classify, pVec):
    l = len(pVec)
    result = 0
    for i in range(l):
        if (vec2Classify[i] == 1):
            result = result + log(pVec[i])
        else:
            result = result + log(1 - pVec[i])
    return result

    
def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(bagOfWords2VecMN(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
    print 'thisDoc: ', thisDoc
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)

def trainNB1(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    classList = list(set(trainCategory))
    result = {}
    for i in range(len(classList)):
        sumOfThisClass = 0
        for j in range(numTrainDocs):
            if trainCategory[j] == classList[i]:
                sumOfThisClass = sumOfThisClass + 1
        temp = {}
        temp['p'] = sumOfThisClass / float(numTrainDocs)
        temp['pVec'] = ones(numWords)
        result[classList[i]] = temp
    # pAbusive = sum(trainCategory)/float(numTrainDocs)
    # p0Num = ones(numWords); p1Num = ones(numWords)
    # p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        for j in range(len(classList)):
            if trainCategory[i] == classList[j]:
                result[classList[j]]['pVec'] += trainMatrix[i]
    for j in range(len(classList)):
        result[classList[j]]['pVec'] = result[classList[j]]['pVec'] / float(numTrainDocs)
    return result

def classifyNB1(vec2Classify, pObj):
    labels = pObj.keys()
    # maxP = logProp(vec2Classify, pObj[labels[0]]['pVec']) + log(pObj[labels[0]]['p'])
    maxP = sum(vec2Classify * log(pObj[labels[0]]['pVec'])) + log(pObj[labels[0]]['p'])
    result = labels[0]
    for label in labels:
        p = sum(vec2Classify * log(pObj[label]['pVec'])) + log(pObj[label]['p'])
        if p > maxP:
            maxP = p
            result = label
    return result

def spamTest1():
    docList = []; classList = []; fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    r = trainNB1(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB1(array(wordVector), r) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)

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
    classList = []
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        item = img2vector('../chapter2/digits/trainingDigits/%s' % fileNameStr)
        classList.append(classNumStr)
        trainingMat.append(item)
    return trainingMat, classList

def testPredictByBayes():
    trainingMat, classList = getTraningMat()
    r = trainNB1(trainingMat, classList)
    testFileList = listdir('../chapter2/digits/testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('../chapter2/digits/testDigits/%s' % fileNameStr)
        classifierResult = classifyNB1(vectorUnderTest, r)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\n %f %% are right" % ((1-errorCount/float(mTest))*100)
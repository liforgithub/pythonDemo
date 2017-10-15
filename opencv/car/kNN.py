# -*- coding: cp936 -*-
from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    lables=['A','A','B','B']
    return group,lables
#k-Nearest Neighbors algorithm
#inX为待分类的点，dataSet为n*m的数据集，lables为dataSet中每一个点对应的分类结果，k为前k个距离最小的点
def classify0(inX,dataSet,labels,k):#intX为共有m个元素的一行矩阵
    dataSetSize=dataSet.shape[0]#行数
    diffMat=tile(inX,(dataSetSize,1))-dataSet#此时，diffMat为n*m维的矩阵
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()#根据值的大小生成对应的参数位置列表
    classCount={}
    for i in range(k):#取前k个距离的最小值
        voteIlabel=labels[sortedDistIndicies[i]]
        #键为lables中的种类，值为出现的次数
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    #对字典按照值从大到小排序，返回一个排序好的列表
    sortedClassCount=sorted(classCount.iteritems(),
    key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
#从text文本中解析需要的数据
def file2matrix(filename):
    fr=open(filename)
    numberOfLines=len(fr.readlines())
    returnMat=zeros((numberOfLines,3))
    #print fr.readlines(),numberOfLines
    fr=open(filename)
    classLableVector=[]
    index=0
    for line in fr.readlines():
        line=line.strip()#剥去末尾的空格
        listFromLine=line.split('\t')#以空格分割字符串，返回分割后的字符串列表
        returnMat[index,0:3]=listFromLine[0:3]
        classLableVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLableVector
#归一化,公式为(x-min)/(max-min)
def autoNorm(dataSet):#dataSet为n*m维
    minVals=dataSet.min(0)#求每一列的最小值，返回一个1*m的矩阵
    maxVals=dataSet.max(0)#求每一列的最大值，返回一个1*m的矩阵
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    normDataSet=dataSet-tile(minVals,(dataSet.shape[0],1))#n*m的矩阵
    normDataSet=normDataSet/tile(ranges,(dataSet.shape[0],1))
    return normDataSet,ranges,minVals
def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLables=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],\
                        datingLables[numTestVecs:m],5)
        print "the classifier came back with: %d, the real answer is: %d"\
% (classifierResult, datingLables[i])
        if classifierResult != datingLables[i]:errorCount+=1.0
    print 'the  total error rate is:%f' % (errorCount/float(numTestVecs))
def classifyPerson():
    resultList=['not at all','in small doses','in large doses']
    #从终端输入个人数据
    percentTats=float(raw_input(\
        'percentage of time spent playing video games?'))
    ffMiles=float(raw_input('frequent flier miles earned per year?'))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    inArr=array([ffMiles,percentTats,iceCream])#转换成矩阵
    datingDataMat,datingLables=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)#归一化处理
    #进行k近邻分类
    classifierResult=classify0((inArr-minVals)/ranges,normMat,\
                        datingLables,5)#先要对要进行分类的点进行归一化处理
    print 'the result is:%s' % resultList[classifierResult-1]

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('E:\\研究生学习课件\\机器学习实战（中文版+英文版+源代码）\\machinelearninginaction\\Ch02\\digits\\trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('E:\\研究生学习课件\\机器学习实战（中文版+英文版+源代码）\\machinelearninginaction\\Ch02\\digits\\trainingDigits/%s' % fileNameStr)
    testFileList = listdir('E:\\研究生学习课件\\机器学习实战（中文版+英文版+源代码）\\machinelearninginaction\\Ch02\\digits\\testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('E:\\研究生学习课件\\机器学习实战（中文版+英文版+源代码）\\machinelearninginaction\\Ch02\\digits\\testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))
if __name__ == '__main__':
    '''returnMat,classLableVector=file2matrix('E:\\研究生学习课件\\机器学习实战（中文版+英文版+源代码）\\machinelearninginaction\\Ch02\\datingTestSet.txt')
    normDataSet,ranges,minVals=autoNorm(returnMat)
    print returnMat#,classLableVector[:20]
    print normDataSet,ranges,minVals'''
    #datingClassTest()
    #classifyPerson()
    handwritingClassTest()

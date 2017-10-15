# -*- coding: cp936 -*-
from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    lables=['A','A','B','B']
    return group,lables
#k-Nearest Neighbors algorithm
#inXΪ������ĵ㣬dataSetΪn*m�����ݼ���lablesΪdataSet��ÿһ�����Ӧ�ķ�������kΪǰk��������С�ĵ�
def classify0(inX,dataSet,labels,k):#intXΪ����m��Ԫ�ص�һ�о���
    dataSetSize=dataSet.shape[0]#����
    diffMat=tile(inX,(dataSetSize,1))-dataSet#��ʱ��diffMatΪn*mά�ľ���
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()#����ֵ�Ĵ�С���ɶ�Ӧ�Ĳ���λ���б�
    classCount={}
    for i in range(k):#ȡǰk���������Сֵ
        voteIlabel=labels[sortedDistIndicies[i]]
        #��Ϊlables�е����ֵ࣬Ϊ���ֵĴ���
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    #���ֵ䰴��ֵ�Ӵ�С���򣬷���һ������õ��б�
    sortedClassCount=sorted(classCount.iteritems(),
    key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
#��text�ı��н�����Ҫ������
def file2matrix(filename):
    fr=open(filename)
    numberOfLines=len(fr.readlines())
    returnMat=zeros((numberOfLines,3))
    #print fr.readlines(),numberOfLines
    fr=open(filename)
    classLableVector=[]
    index=0
    for line in fr.readlines():
        line=line.strip()#��ȥĩβ�Ŀո�
        listFromLine=line.split('\t')#�Կո�ָ��ַ��������طָ����ַ����б�
        returnMat[index,0:3]=listFromLine[0:3]
        classLableVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLableVector
#��һ��,��ʽΪ(x-min)/(max-min)
def autoNorm(dataSet):#dataSetΪn*mά
    minVals=dataSet.min(0)#��ÿһ�е���Сֵ������һ��1*m�ľ���
    maxVals=dataSet.max(0)#��ÿһ�е����ֵ������һ��1*m�ľ���
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    normDataSet=dataSet-tile(minVals,(dataSet.shape[0],1))#n*m�ľ���
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
    #���ն������������
    percentTats=float(raw_input(\
        'percentage of time spent playing video games?'))
    ffMiles=float(raw_input('frequent flier miles earned per year?'))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    inArr=array([ffMiles,percentTats,iceCream])#ת���ɾ���
    datingDataMat,datingLables=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)#��һ������
    #����k���ڷ���
    classifierResult=classify0((inArr-minVals)/ranges,normMat,\
                        datingLables,5)#��Ҫ��Ҫ���з���ĵ���й�һ������
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
    trainingFileList = listdir('E:\\�о���ѧϰ�μ�\\����ѧϰʵս�����İ�+Ӣ�İ�+Դ���룩\\machinelearninginaction\\Ch02\\digits\\trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('E:\\�о���ѧϰ�μ�\\����ѧϰʵս�����İ�+Ӣ�İ�+Դ���룩\\machinelearninginaction\\Ch02\\digits\\trainingDigits/%s' % fileNameStr)
    testFileList = listdir('E:\\�о���ѧϰ�μ�\\����ѧϰʵս�����İ�+Ӣ�İ�+Դ���룩\\machinelearninginaction\\Ch02\\digits\\testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('E:\\�о���ѧϰ�μ�\\����ѧϰʵս�����İ�+Ӣ�İ�+Դ���룩\\machinelearninginaction\\Ch02\\digits\\testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))
if __name__ == '__main__':
    '''returnMat,classLableVector=file2matrix('E:\\�о���ѧϰ�μ�\\����ѧϰʵս�����İ�+Ӣ�İ�+Դ���룩\\machinelearninginaction\\Ch02\\datingTestSet.txt')
    normDataSet,ranges,minVals=autoNorm(returnMat)
    print returnMat#,classLableVector[:20]
    print normDataSet,ranges,minVals'''
    #datingClassTest()
    #classifyPerson()
    handwritingClassTest()

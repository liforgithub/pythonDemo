# -*- coding: cp936 -*-
import os
import cv2
import math
import kNN
from PIL import Image
from pylab import *
from numpy import *
from matplotlib import pyplot as plt
from matplotlib import cm #从包中导入模块

#创建一个包含文件夹中所有jpg图像文件的文件名列表
def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path)if f.endswith('.jpg')]

#图像缩放，输入图像数组，返回图像数组
def imresize(im,sz):
    pil_im=Image.fromarray((uint8)(im))
    return array(pil_im.resize(sz))

#对灰度图像进行直方图均衡化
def histeq(im,nbr_bins=256):
    #计算图像的直方图
    imhits,bins=histogram(im.flatten(),nbr_bins,normed=True)
    cdf=imhits.cumsum()#累积分布函数
    cdf=255*cdf/cdf[-1]#归一化
    #使用累积分布函数的线性插值，计算新的像素值
    im2=interp(im.flatten(),bins[:-1],cdf)

    return im2.reshape(im.shape),cdf

#图像平均,据算图像列表的平均图像
def copute_average(imlist):#imlist为文件名列表
    averageim=array(Image.open(imlist[0]),'f')
    for imname in imlist[1:]:
        try:
            averagein+=array(Image.open(imname),'f')
        except:
            print (imname+'...skipped')
    averageim/=len(imlist)
    
    #返回unit8类型的平均图像
    return array(averageim,'unit8')

#图像旋转
def rotate_about_center(src,rangle,scale=1.0):
    w=src.shape[1]
    h=src.shape[0]
    angle=np.rad2deg(rangle)#从弧度换算到度数
    #计算新的图像宽度和高度
    nw=(abs(sin(rangle)*h)+abs(cos(rangle)*w))*scale
    nh=(abs(cos(rangle)*h)+abs(sin(rangle)*w))*scale
    #调用opencv得到旋转矩阵
    rot_mat=cv2.getRotationMatrix2D((nw*0.5,nh*0.5),angle,scale)
    rot_move=dot(rot_mat,array([(nw-w)*0.5,(nh-h)*0.5,0]))
    rot_mat[0,2]+=rot_move[0]
    rot_mat[1,2]+=rot_move[1]
    return cv2.warpAffine(src,rot_mat,(int(math.ceil(nw)),int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
#车牌去除边框
def border_segment(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=0
    yy1=0
    yy2=h-1
  #  寻找上边界
    for y in xrange(h/2):
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#上边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最上边的第一个空行
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最上边的第一个字符行
                yy1=y#上边框位置
            #    print yy1
                flag=False
    
    #寻找下边界
    flag=False
    pixels=0
    for y in xrange(h-1,h/2-1,-1):#从下向上扫描
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#上边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最下边的第一个空行
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最下边的第一个字符行
                yy2=y#下边框位置
            #    print yy2
                flag=False
    #src[:yy1,:]=0
   # src[yy2:,:]=0#通过切片将边框以外的部分设置为黑色的点
    #寻找左边界
    xx1=0
    xx2=w-1
    flag=False
    pixels=0
    for x in xrange(w/8):
      #  print x
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#左边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.7*pixels:#找到最左边的空列，此处参数越大表示值越近
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.3*curpixels:#找到第一个字符所在列，参数有待优化
                xx1=x#左边框位置
           #     print 'xx1:%s' % xx1
                flag=False
                
    #寻找右边界
    flag=False
    pixels=0
    for x in xrange(w-1,7*w/8-1,-1):#从右向左扫描
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#左边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最右边的第一个空列
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最右边的第一个字符列
                xx2=x#下边框位置
               # print 'xx2:%s' % xx2
                flag=False
    #src[:,:xx1]=0
    #src[:,xx2:]=0
    return src[yy1:yy2,xx1:xx2]
#车牌字符分割
def get_single_char(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=[]
    threshlod1=4#白色点数阈值，大于阈值为字符开始列，小于为字符结束列
    threshlod2=15#第一个汉字宽度阈值，必须要大于此阈值，才能被判定为完整的汉字
    for x in xrange(w):
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        pixels.append(count)
    print pixels #打印所有列像素值为255的点数
    for x in xrange(w):#寻找第一个汉字
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        if not flag and count>threshlod1:
            L=x
            flag=True
        if flag and count<threshlod1:
            R=x
            if R-L > threshlod2:break
    print L,R
    '''for y in xrange(h):
        src[y,L]=255
        src[y,R]=255'''
    flag=False
    Lborder=[]
    Rborder=[]
    threshlod2=12#剩下的六个字符间的宽度阈值
    for x in xrange(R+1,w):#寻找剩下的六个字符
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        if not flag and count>threshlod1:
            xx1=x
            Lborder.append(xx1)
            print 'L:%s,count:%s' % (xx1,count)
            flag=True
        if flag and count<threshlod1:
            if x-xx1>threshlod2:
                xx2=x
                Rborder.append(xx2)
                print 'R:%s,count:%s' % (xx2,count)
                flag=False
    '''for y in xrange(h):
        for x in Lborder:
            src[y,x]=255
        for x in Rborder:
            src[y,x]=255'''
    #如果没有判断出最后一条边界，则将右边界加入到列表中
    if len(Rborder)<len(Lborder):Rborder.append(w-1)
    print Lborder,Rborder
    #字符归一化处理，5*10的尺寸
    char=[]#存储每个归一化后的图像列表
    char1=src[:,L:R]
    #print 'char1-11:',char1
    char1=cv2.resize(char1,(20,40))#resize 会改变一些像素点的值,会存在一些不为0或者255的点
    ret,char1=cv2.threshold(char1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#0-255
    char.append(char1)
    #print 'char1:',char1
    for i in range(6):#处理剩下的六个字符
        char_each=src[:,Lborder[i]:Rborder[i]]
        char_each=cv2.resize(char_each,(20,40))
        ret,char_each=cv2.threshold(char_each,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #进行细化
        '''kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,6))
        char_each=cv2.erode(char_each,kernel,iterations=2)'''
        #char_each=cv2Thin(char_each,1)
        cv2.imshow('字符细化后%s' % (i+1),char_each)
        #print char_each.shape,char_each[3,:]
        char.append(char_each)
        
    return char
#通过findContours函数进行字符分割,效果不佳，有待改进
def charac_segment_contours(img_binary):
    img=cv2.resize(img_binary,None,fx=2,fy=2)
    image1,contours,heirs = cv2.findContours(img.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    rectangles=[]
    for tours in contours:
        rc= cv2.boundingRect(tours)
        print '字符分割：',rc
        rectangles.append(rc)
        if rc[2]>5 and rc[3]>5 :
            cv2.rectangle(img, (rc[0],rc[1]),(rc[0]+rc[2],rc[1]+rc[3]),(255,0,255))
    cv2.imshow('车牌分割图像',img)
    
#图像细化算法
def cv2Thin(img,interations):
    h,w=img.shape
    print '尺寸:',img.shape
    print 'img is:',img[3,:]
    for n in range(interations):#迭代n次
        #进行第一次循环扫描，去除东南方向的边界点
        for y in xrange(h):
            for x in xrange(w):
                if img[y,x]==255:
                    ap=0
                    p2= np.uint32((y==0)and [0] or [img[y-1,x]][0])#模拟？：表达式
                    p3= np.uint32((y==0 or x==w-1 ) and [0] or [img[y-1,x+1]][0])
                    if p2==0 and p3==255:ap+=1
                    p4= np.uint32((x==w-1)and [0] or [img[y,x+1]][0])
                    if p3==0 and p4==255:ap+=1
                    p5= np.uint32((y==h-1 or x==w-1)and [0] or [img[y+1,x+1]][0])
                    if p4==0 and p5==255:ap+=1
                    p6= np.uint32((y==h-1)and [0] or [img[y+1,x]][0])
                    if p5==0 and p6==255:ap+=1
                    p7= np.uint32((y==h-1 or x==0)and [0] or [img[y+1,x-1]][0])
                    if p6==0 and p7==255:ap+=1
                    p8= np.uint32(x==0 and [0] or [img[y,x-1]][0])
                    if p7==0 and p8==255:ap+=1
                    p9= np.uint32((x==0 or y==0)and [0] or [img[y-1,x-1]][0])
                    if p8==0 and p9==255:ap+=1
                    if p9==0 and p2==255:ap+=1
                    sum1=(p2+p3+p4+p5+p6+p7+p8+p9)#使用np.uint32进行类型转换，防止加法溢出
                    #print 'sum1 is:',sum1
                    if sum1 >1*255 and sum1<7*255 :
                        if ap==1:
                            if not(p2 and p4 and p6):
                                if not (p4 and p6 and p8):
                                    img[y,x]=0
        #进行第二次扫描，去除西北方向的边界点
        for y in xrange(h):
            for x in xrange(w):
                if img[y,x]==255:
                    ap=0
                    p2= np.uint32((y==0)and [0] or [img[y-1,x]])[0]#模拟？：表达式
                    #print 'p2:',p2
                    p3= np.uint32((y==0 or x==w-1 ) and [0] or [img[y-1,x+1]])[0]
                    if p2==0 and p3==255:ap+=1
                    p4= np.uint32((x==w-1)and [0] or [img[y,x+1]])[0]
                    if p3==0 and p4==255:ap+=1
                    p5= np.uint32((y==h-1 or x==w-1)and [0] or [img[y+1,x+1]])[0]
                    if p4==0 and p5==255:ap+=1
                    p6= np.uint32((y==h-1)and [0] or [img[y+1,x]])[0]
                    if p5==0 and p6==255:ap+=1
                    p7= np.uint32((y==h-1 or x==0)and [0] or [img[y+1,x-1]])[0]
                    if p6==0 and p7==255:ap+=1
                    p8= np.uint32((x==0)and [0] or [img[y,x-1]])[0]
                    if p7==0 and p8==255:ap+=1
                    p9= np.uint32((x==0 or y==0)and [0] or [img[y-1,x-1]])[0]
                    if p8==0 and p9==255:ap+=1
                    if p9==0 and p2==255:ap+=1
                    sum1=(p2+p3+p4+p5+p6+p7+p8+p9)
                    #print 'sum1-2 is:',sum1
                    if sum1>1*255 and sum1<7*255 :
                        if ap==1:
                            if not (p2 and p4 and p6):
                                if not(p4 and p6 and p8):
                                    img[y,x]=0
    return img

#对分割后的图像生成对应的0-1模板，尺寸为20*40
def generateTemplate(charList):
    List=[]
    h,w=charList[2].shape
    for i in xrange(len(charList)):
        for y in xrange(h):
            for x in xrange(w):
                if charList[i][y,x]>127:
                    charList[i][y,x]=1
                else:charList[i][y,x]=0
        #cv2.imshow('字符旋转前',charList[i])
        L=(rotate_about_center(charList[i],-np.pi/2))
        List.append(L)#顺时针旋转90度
        cv2.imshow('字符%s旋转后' % (i+1),List[i])
        print '旋转后的尺寸为:',List[i].shape
    return List
#从磁盘中读入模板txt文件到一维向量中，并做水平镜像变换
def img2vector(filename):
    fr=open(filename) 
    returnMat=np.zeros((1,800))#将20*40的0-1矩阵归并到一行
    for i in xrange(20):
        lineStr=fr.readline()
        for j in xrange(40):
            returnMat[0,i*40+j]=int(lineStr[39-j])#水平镜像变换
    fr.close()
    return returnMat
#使用kNN进行字符识别，传入待识别的字符列表
def characterClassifyBykNN(charList):
     #建立模板矩阵
    characLables=[]
    characFileList=os.listdir('model')
    m=len(characFileList)
    trainingMat=np.zeros((m,800))
    for i in xrange(m):
        classNumStr=characFileList[i].split('.')[0]
        characLables.append(classNumStr)#建立每个模板对应的标签
        trainingMat[i,:]=img2vector('model/%s' % characFileList[i])
    #进行字符识别，汉字除外
    mTest=len(charList)
    vectorCharac=np.zeros((1,800))
    classfierResult=[]
    for i in xrange(1,mTest):#暂不识别第一个汉字
      #将待识别的字符归并到一行  
        for y in xrange(20):
            for x in xrange(40):
                vectorCharac[0,y*40+x]=charList[i][y,x]
      #进行kNN识别
        result=kNN.classify0(vectorCharac,trainingMat,characLables,3)
        classfierResult.append(result)
    return classfierResult#返回识别后的结果列表

#将待识别的字符模板写入到txt文件中
def characWriteTxt(charList):
    for i in xrange(len(charList)):
        fr=open(('/车牌字符/%s.txt' % (i+1)),'w')
        for y in xrange(charList[i].shape[0]):
            fr.writelines(str(charList[i][y,:])+'\n')#将每一行写入到txt文件中
        fr.close()

    
if __name__ == '__main__':#直接运行测试
    im=array(Image.open('E:\\袁悦\\1_copy.jpg'))
    ret,binary=cv2.threshold(im,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img=cv2Thin(im,3)
    im2,cdf=histeq(im)
    cv2.imshow('细化图像',img)
    plt.imshow(im2,cmap=cm.gray)
    show()#定义在pylab中

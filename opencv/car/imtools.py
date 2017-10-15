# -*- coding: cp936 -*-
import os
import cv2
import math
import kNN
from PIL import Image
from pylab import *
from numpy import *
from matplotlib import pyplot as plt
from matplotlib import cm #�Ӱ��е���ģ��

#����һ�������ļ���������jpgͼ���ļ����ļ����б�
def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path)if f.endswith('.jpg')]

#ͼ�����ţ�����ͼ�����飬����ͼ������
def imresize(im,sz):
    pil_im=Image.fromarray((uint8)(im))
    return array(pil_im.resize(sz))

#�ԻҶ�ͼ�����ֱ��ͼ���⻯
def histeq(im,nbr_bins=256):
    #����ͼ���ֱ��ͼ
    imhits,bins=histogram(im.flatten(),nbr_bins,normed=True)
    cdf=imhits.cumsum()#�ۻ��ֲ�����
    cdf=255*cdf/cdf[-1]#��һ��
    #ʹ���ۻ��ֲ����������Բ�ֵ�������µ�����ֵ
    im2=interp(im.flatten(),bins[:-1],cdf)

    return im2.reshape(im.shape),cdf

#ͼ��ƽ��,����ͼ���б��ƽ��ͼ��
def copute_average(imlist):#imlistΪ�ļ����б�
    averageim=array(Image.open(imlist[0]),'f')
    for imname in imlist[1:]:
        try:
            averagein+=array(Image.open(imname),'f')
        except:
            print (imname+'...skipped')
    averageim/=len(imlist)
    
    #����unit8���͵�ƽ��ͼ��
    return array(averageim,'unit8')

#ͼ����ת
def rotate_about_center(src,rangle,scale=1.0):
    w=src.shape[1]
    h=src.shape[0]
    angle=np.rad2deg(rangle)#�ӻ��Ȼ��㵽����
    #�����µ�ͼ���Ⱥ͸߶�
    nw=(abs(sin(rangle)*h)+abs(cos(rangle)*w))*scale
    nh=(abs(cos(rangle)*h)+abs(sin(rangle)*w))*scale
    #����opencv�õ���ת����
    rot_mat=cv2.getRotationMatrix2D((nw*0.5,nh*0.5),angle,scale)
    rot_move=dot(rot_mat,array([(nw-w)*0.5,(nh-h)*0.5,0]))
    rot_mat[0,2]+=rot_move[0]
    rot_mat[1,2]+=rot_move[1]
    return cv2.warpAffine(src,rot_mat,(int(math.ceil(nw)),int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
#����ȥ���߿�
def border_segment(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=0
    yy1=0
    yy2=h-1
  #  Ѱ���ϱ߽�
    for y in xrange(h/2):
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#�ϱ߽�
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#�ҵ����ϱߵĵ�һ������
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#�ҵ����ϱߵĵ�һ���ַ���
                yy1=y#�ϱ߿�λ��
            #    print yy1
                flag=False
    
    #Ѱ���±߽�
    flag=False
    pixels=0
    for y in xrange(h-1,h/2-1,-1):#��������ɨ��
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#�ϱ߽�
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#�ҵ����±ߵĵ�һ������
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#�ҵ����±ߵĵ�һ���ַ���
                yy2=y#�±߿�λ��
            #    print yy2
                flag=False
    #src[:yy1,:]=0
   # src[yy2:,:]=0#ͨ����Ƭ���߿�����Ĳ�������Ϊ��ɫ�ĵ�
    #Ѱ����߽�
    xx1=0
    xx2=w-1
    flag=False
    pixels=0
    for x in xrange(w/8):
      #  print x
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#��߽�
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.7*pixels:#�ҵ�����ߵĿ��У��˴�����Խ���ʾֵԽ��
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.3*curpixels:#�ҵ���һ���ַ������У������д��Ż�
                xx1=x#��߿�λ��
           #     print 'xx1:%s' % xx1
                flag=False
                
    #Ѱ���ұ߽�
    flag=False
    pixels=0
    for x in xrange(w-1,7*w/8-1,-1):#��������ɨ��
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#��߽�
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#�ҵ����ұߵĵ�һ������
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#�ҵ����ұߵĵ�һ���ַ���
                xx2=x#�±߿�λ��
               # print 'xx2:%s' % xx2
                flag=False
    #src[:,:xx1]=0
    #src[:,xx2:]=0
    return src[yy1:yy2,xx1:xx2]
#�����ַ��ָ�
def get_single_char(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=[]
    threshlod1=4#��ɫ������ֵ��������ֵΪ�ַ���ʼ�У�С��Ϊ�ַ�������
    threshlod2=15#��һ�����ֿ����ֵ������Ҫ���ڴ���ֵ�����ܱ��ж�Ϊ�����ĺ���
    for x in xrange(w):
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        pixels.append(count)
    print pixels #��ӡ����������ֵΪ255�ĵ���
    for x in xrange(w):#Ѱ�ҵ�һ������
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
    threshlod2=12#ʣ�µ������ַ���Ŀ����ֵ
    for x in xrange(R+1,w):#Ѱ��ʣ�µ������ַ�
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
    #���û���жϳ����һ���߽磬���ұ߽���뵽�б���
    if len(Rborder)<len(Lborder):Rborder.append(w-1)
    print Lborder,Rborder
    #�ַ���һ������5*10�ĳߴ�
    char=[]#�洢ÿ����һ�����ͼ���б�
    char1=src[:,L:R]
    #print 'char1-11:',char1
    char1=cv2.resize(char1,(20,40))#resize ��ı�һЩ���ص��ֵ,�����һЩ��Ϊ0����255�ĵ�
    ret,char1=cv2.threshold(char1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#0-255
    char.append(char1)
    #print 'char1:',char1
    for i in range(6):#����ʣ�µ������ַ�
        char_each=src[:,Lborder[i]:Rborder[i]]
        char_each=cv2.resize(char_each,(20,40))
        ret,char_each=cv2.threshold(char_each,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #����ϸ��
        '''kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,6))
        char_each=cv2.erode(char_each,kernel,iterations=2)'''
        #char_each=cv2Thin(char_each,1)
        cv2.imshow('�ַ�ϸ����%s' % (i+1),char_each)
        #print char_each.shape,char_each[3,:]
        char.append(char_each)
        
    return char
#ͨ��findContours���������ַ��ָ�,Ч�����ѣ��д��Ľ�
def charac_segment_contours(img_binary):
    img=cv2.resize(img_binary,None,fx=2,fy=2)
    image1,contours,heirs = cv2.findContours(img.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    rectangles=[]
    for tours in contours:
        rc= cv2.boundingRect(tours)
        print '�ַ��ָ',rc
        rectangles.append(rc)
        if rc[2]>5 and rc[3]>5 :
            cv2.rectangle(img, (rc[0],rc[1]),(rc[0]+rc[2],rc[1]+rc[3]),(255,0,255))
    cv2.imshow('���Ʒָ�ͼ��',img)
    
#ͼ��ϸ���㷨
def cv2Thin(img,interations):
    h,w=img.shape
    print '�ߴ�:',img.shape
    print 'img is:',img[3,:]
    for n in range(interations):#����n��
        #���е�һ��ѭ��ɨ�裬ȥ�����Ϸ���ı߽��
        for y in xrange(h):
            for x in xrange(w):
                if img[y,x]==255:
                    ap=0
                    p2= np.uint32((y==0)and [0] or [img[y-1,x]][0])#ģ�⣿�����ʽ
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
                    sum1=(p2+p3+p4+p5+p6+p7+p8+p9)#ʹ��np.uint32��������ת������ֹ�ӷ����
                    #print 'sum1 is:',sum1
                    if sum1 >1*255 and sum1<7*255 :
                        if ap==1:
                            if not(p2 and p4 and p6):
                                if not (p4 and p6 and p8):
                                    img[y,x]=0
        #���еڶ���ɨ�裬ȥ����������ı߽��
        for y in xrange(h):
            for x in xrange(w):
                if img[y,x]==255:
                    ap=0
                    p2= np.uint32((y==0)and [0] or [img[y-1,x]])[0]#ģ�⣿�����ʽ
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

#�Էָ���ͼ�����ɶ�Ӧ��0-1ģ�壬�ߴ�Ϊ20*40
def generateTemplate(charList):
    List=[]
    h,w=charList[2].shape
    for i in xrange(len(charList)):
        for y in xrange(h):
            for x in xrange(w):
                if charList[i][y,x]>127:
                    charList[i][y,x]=1
                else:charList[i][y,x]=0
        #cv2.imshow('�ַ���תǰ',charList[i])
        L=(rotate_about_center(charList[i],-np.pi/2))
        List.append(L)#˳ʱ����ת90��
        cv2.imshow('�ַ�%s��ת��' % (i+1),List[i])
        print '��ת��ĳߴ�Ϊ:',List[i].shape
    return List
#�Ӵ����ж���ģ��txt�ļ���һά�����У�����ˮƽ����任
def img2vector(filename):
    fr=open(filename) 
    returnMat=np.zeros((1,800))#��20*40��0-1����鲢��һ��
    for i in xrange(20):
        lineStr=fr.readline()
        for j in xrange(40):
            returnMat[0,i*40+j]=int(lineStr[39-j])#ˮƽ����任
    fr.close()
    return returnMat
#ʹ��kNN�����ַ�ʶ�𣬴����ʶ����ַ��б�
def characterClassifyBykNN(charList):
     #����ģ�����
    characLables=[]
    characFileList=os.listdir('model')
    m=len(characFileList)
    trainingMat=np.zeros((m,800))
    for i in xrange(m):
        classNumStr=characFileList[i].split('.')[0]
        characLables.append(classNumStr)#����ÿ��ģ���Ӧ�ı�ǩ
        trainingMat[i,:]=img2vector('model/%s' % characFileList[i])
    #�����ַ�ʶ�𣬺��ֳ���
    mTest=len(charList)
    vectorCharac=np.zeros((1,800))
    classfierResult=[]
    for i in xrange(1,mTest):#�ݲ�ʶ���һ������
      #����ʶ����ַ��鲢��һ��  
        for y in xrange(20):
            for x in xrange(40):
                vectorCharac[0,y*40+x]=charList[i][y,x]
      #����kNNʶ��
        result=kNN.classify0(vectorCharac,trainingMat,characLables,3)
        classfierResult.append(result)
    return classfierResult#����ʶ���Ľ���б�

#����ʶ����ַ�ģ��д�뵽txt�ļ���
def characWriteTxt(charList):
    for i in xrange(len(charList)):
        fr=open(('/�����ַ�/%s.txt' % (i+1)),'w')
        for y in xrange(charList[i].shape[0]):
            fr.writelines(str(charList[i][y,:])+'\n')#��ÿһ��д�뵽txt�ļ���
        fr.close()

    
if __name__ == '__main__':#ֱ�����в���
    im=array(Image.open('E:\\Ԭ��\\1_copy.jpg'))
    ret,binary=cv2.threshold(im,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img=cv2Thin(im,3)
    im2,cdf=histeq(im)
    cv2.imshow('ϸ��ͼ��',img)
    plt.imshow(im2,cmap=cm.gray)
    show()#������pylab��

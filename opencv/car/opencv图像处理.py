# -*- coding: cp936 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imtools

img=cv2.imread('C:\Users\Administrator\Desktop\VC++数字图像处理\车牌图片收集\\1.bmp')
#img=cv2.imread('C:\Users\Administrator\Desktop\VC++数字图像处理\图像库\plate picture_jpg\Level_1\初出茅庐003.jpg')

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#灰度变换
cv2.imshow('灰度图像',gray)
blur = cv2.GaussianBlur(gray,(5,5),0)#高斯滤波
edge=cv2.Canny(blur,100,200,True)#用canny算子边缘检测

#使用3*3的内核对梯度图进行平均模糊，有助于平滑地图表征的图形中的高频噪声,此步骤不能少
blured=cv2.blur(edge,(3,3))
#二值化，采用OTSU
ret,binary=cv2.threshold(blured,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('二值化图像',binary)
#print binary[10,:]
#形态学处理
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(13,4))
closing=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,kernel)
#先腐蚀再膨胀去除孤立的白色点噪声
closing=cv2.erode(closing,kernel,iterations=6)
closing=cv2.dilate(closing,kernel,iterations=6)
cv2.imshow('形态学运算图像',closing)
#去除伪车牌，通过长宽比例
image1,contours,heirs = cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
rectangles=[]
for tours in contours:
     rc= cv2.boundingRect(tours)
     rectangles.append(rc)
     #print rectangles
if len(rectangles)>1:rc=sorted(rectangles,key=lambda each:each[0],reverse=True)[0]#有多个矩阵时，找到最下面的那个矩阵
else:rc=rectangles[0]#只有一个矩阵
#print rc,rc[2],rc[3],rc[2]/rc[3]
if  2.0<float (rc[2])/rc[3]<4.5 :#比例值有待优化
     #rc[0] 表示图像左上角的纵坐标，rc[1] 表示图像左上角的横坐标，rc[2] 表示图像的宽度，rc[3] 表示图像的高度，
     cv2.rectangle(img, (rc[0],rc[1]),(rc[0]+rc[2],rc[1]+rc[3]),(255,0,255))
     print rc
     #通过切片来提取目标区域，注意坐标的变换，稍微放大一些目标区域
     plate=gray[rc[1]-5:(rc[1]+rc[3]+5),rc[0]-5:(rc[0]+rc[2]+5)]
     cv2.imshow('车牌提取灰度图片',plate)
     print plate.shape
     # break #break要不要？
    
#开始下一步，进行字符分割
plate=cv2.resize(plate,None,fx=2,fy=2) #放大两倍
cv2.imshow('车牌提取灰度图片',plate) 
ret,img_binary=cv2.threshold(plate,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#print 'img_binary-1:',img_binary[10,:]
print plate.shape
jump=[]#存储每行0到255跳变的个数
incline=False
#进行倾斜检测
for y in xrange(img_binary.shape[0]).__reversed__():#从下往上扫描，xrange返回的是列表
    # print y
     i=0
     for x in xrange(img_binary.shape[1]-1):#从左往右扫描,剔除最后一个元素
          if not img_binary[y,x] and img_binary[y,x+1]==255:
               i+=1
     jump.append(i)
     if i>8 :
          if 3*jump[-1]/(jump[-2]+jump[-3]+jump[-4]) < 2.0 :
               print '车牌倾斜'
               incline=True
          break
#print jump
#print img_binary[20]
if incline:#倾斜校正,使用霍夫变换进行直线检测
     lines=cv2.HoughLines(img_binary.copy(),1,np.pi/180,128)#lines是一个三维数组
     #print lines
     all_line=sorted(lines,key=lambda line:line[0][0],reverse=True)#找到一条最长直线
    # print all_line
     max_line=all_line[0]
     aver_theta=0
     for i in range(3):
           aver_theta+=all_line[i][0][1]
     aver_theta/=3  #取前三次最大的角度的平均值
     print '倾斜角度为：%s' % np.rad2deg(np.pi/2-aver_theta)
     rho=max_line[0][0]
     theta=max_line[0][1]
     # 该直线与第一列的交点  
     pt1 = (0,int(rho/np.sin(theta)))  
     #该直线与最后一列的交点  
     pt2 = (img_binary.shape[1], int((rho-img_binary.shape[1]*np.cos(theta))/np.sin(theta)))  
     #绘制最长的那条直线  
     #cv2.line(img_binary, pt1, pt2, (255), 1)
     #旋转图像
     img_binary=imtools.rotate_about_center(img_binary,-(np.pi/2-aver_theta))
    # ret,img_binary=cv2.threshold(img_binary,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     #cv2.imshow('旋转后的图像',img_binary)
#img_binary=imtools.cv2Thin(img_binary,3)
cv2.imshow('彩色图像',img)
cv2.imwrite('二值化图片.jpg',img_binary)
cv2.imshow('车牌提取二值化图像',img_binary)
#车牌边框分割以及归一化处理
img_border=imtools.border_segment(img_binary)
#imtools.charac_segment_contours(img_border)
char=imtools.get_single_char(img_border)
'''for i in range(len(char)):
     cv2.imshow('字符旋转前',char[i])'''
cv2.imshow('去除边框图像',img_border)
cv2.imshow('字符旋转前',char[2])#如果第一个名字相同就会被覆盖
print 'char[2]\n',char[2].shape
#cv2.imshow('字符旋转前',char[3])
#对分割后的七个字符进行模板匹配
charlist=imtools.generateTemplate(char)#生成模板
for i in range(len(char)):
     print '旋转后的尺寸为:',charlist[i].shape
print '旋转后的尺寸为:',charlist[3]
imtools.characWriteTxt(charlist)#写入到文件中
#用kNN进行字符识别
classfierResult=imtools.characterClassifyBykNN(charlist)
print '车牌识别结果是:',classfierResult
#img_border=cv2.resize(img_border,None,fx=0.5,fy=0.5) #缩放回原来的尺寸

cv2.waitKey(0)
cv2.destroyAllWindows()

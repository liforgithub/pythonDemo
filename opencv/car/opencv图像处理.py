# -*- coding: cp936 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imtools

img=cv2.imread('C:\Users\Administrator\Desktop\VC++����ͼ����\����ͼƬ�ռ�\\1.bmp')
#img=cv2.imread('C:\Users\Administrator\Desktop\VC++����ͼ����\ͼ���\plate picture_jpg\Level_1\����é®003.jpg')

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#�Ҷȱ任
cv2.imshow('�Ҷ�ͼ��',gray)
blur = cv2.GaussianBlur(gray,(5,5),0)#��˹�˲�
edge=cv2.Canny(blur,100,200,True)#��canny���ӱ�Ե���

#ʹ��3*3���ں˶��ݶ�ͼ����ƽ��ģ����������ƽ����ͼ������ͼ���еĸ�Ƶ����,�˲��費����
blured=cv2.blur(edge,(3,3))
#��ֵ��������OTSU
ret,binary=cv2.threshold(blured,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('��ֵ��ͼ��',binary)
#print binary[10,:]
#��̬ѧ����
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(13,4))
closing=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,kernel)
#�ȸ�ʴ������ȥ�������İ�ɫ������
closing=cv2.erode(closing,kernel,iterations=6)
closing=cv2.dilate(closing,kernel,iterations=6)
cv2.imshow('��̬ѧ����ͼ��',closing)
#ȥ��α���ƣ�ͨ���������
image1,contours,heirs = cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
rectangles=[]
for tours in contours:
     rc= cv2.boundingRect(tours)
     rectangles.append(rc)
     #print rectangles
if len(rectangles)>1:rc=sorted(rectangles,key=lambda each:each[0],reverse=True)[0]#�ж������ʱ���ҵ���������Ǹ�����
else:rc=rectangles[0]#ֻ��һ������
#print rc,rc[2],rc[3],rc[2]/rc[3]
if  2.0<float (rc[2])/rc[3]<4.5 :#����ֵ�д��Ż�
     #rc[0] ��ʾͼ�����Ͻǵ������꣬rc[1] ��ʾͼ�����Ͻǵĺ����꣬rc[2] ��ʾͼ��Ŀ�ȣ�rc[3] ��ʾͼ��ĸ߶ȣ�
     cv2.rectangle(img, (rc[0],rc[1]),(rc[0]+rc[2],rc[1]+rc[3]),(255,0,255))
     print rc
     #ͨ����Ƭ����ȡĿ������ע������ı任����΢�Ŵ�һЩĿ������
     plate=gray[rc[1]-5:(rc[1]+rc[3]+5),rc[0]-5:(rc[0]+rc[2]+5)]
     cv2.imshow('������ȡ�Ҷ�ͼƬ',plate)
     print plate.shape
     # break #breakҪ��Ҫ��
    
#��ʼ��һ���������ַ��ָ�
plate=cv2.resize(plate,None,fx=2,fy=2) #�Ŵ�����
cv2.imshow('������ȡ�Ҷ�ͼƬ',plate) 
ret,img_binary=cv2.threshold(plate,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#print 'img_binary-1:',img_binary[10,:]
print plate.shape
jump=[]#�洢ÿ��0��255����ĸ���
incline=False
#������б���
for y in xrange(img_binary.shape[0]).__reversed__():#��������ɨ�裬xrange���ص����б�
    # print y
     i=0
     for x in xrange(img_binary.shape[1]-1):#��������ɨ��,�޳����һ��Ԫ��
          if not img_binary[y,x] and img_binary[y,x+1]==255:
               i+=1
     jump.append(i)
     if i>8 :
          if 3*jump[-1]/(jump[-2]+jump[-3]+jump[-4]) < 2.0 :
               print '������б'
               incline=True
          break
#print jump
#print img_binary[20]
if incline:#��бУ��,ʹ�û���任����ֱ�߼��
     lines=cv2.HoughLines(img_binary.copy(),1,np.pi/180,128)#lines��һ����ά����
     #print lines
     all_line=sorted(lines,key=lambda line:line[0][0],reverse=True)#�ҵ�һ���ֱ��
    # print all_line
     max_line=all_line[0]
     aver_theta=0
     for i in range(3):
           aver_theta+=all_line[i][0][1]
     aver_theta/=3  #ȡǰ�������ĽǶȵ�ƽ��ֵ
     print '��б�Ƕ�Ϊ��%s' % np.rad2deg(np.pi/2-aver_theta)
     rho=max_line[0][0]
     theta=max_line[0][1]
     # ��ֱ�����һ�еĽ���  
     pt1 = (0,int(rho/np.sin(theta)))  
     #��ֱ�������һ�еĽ���  
     pt2 = (img_binary.shape[1], int((rho-img_binary.shape[1]*np.cos(theta))/np.sin(theta)))  
     #�����������ֱ��  
     #cv2.line(img_binary, pt1, pt2, (255), 1)
     #��תͼ��
     img_binary=imtools.rotate_about_center(img_binary,-(np.pi/2-aver_theta))
    # ret,img_binary=cv2.threshold(img_binary,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     #cv2.imshow('��ת���ͼ��',img_binary)
#img_binary=imtools.cv2Thin(img_binary,3)
cv2.imshow('��ɫͼ��',img)
cv2.imwrite('��ֵ��ͼƬ.jpg',img_binary)
cv2.imshow('������ȡ��ֵ��ͼ��',img_binary)
#���Ʊ߿�ָ��Լ���һ������
img_border=imtools.border_segment(img_binary)
#imtools.charac_segment_contours(img_border)
char=imtools.get_single_char(img_border)
'''for i in range(len(char)):
     cv2.imshow('�ַ���תǰ',char[i])'''
cv2.imshow('ȥ���߿�ͼ��',img_border)
cv2.imshow('�ַ���תǰ',char[2])#�����һ��������ͬ�ͻᱻ����
print 'char[2]\n',char[2].shape
#cv2.imshow('�ַ���תǰ',char[3])
#�Էָ����߸��ַ�����ģ��ƥ��
charlist=imtools.generateTemplate(char)#����ģ��
for i in range(len(char)):
     print '��ת��ĳߴ�Ϊ:',charlist[i].shape
print '��ת��ĳߴ�Ϊ:',charlist[3]
imtools.characWriteTxt(charlist)#д�뵽�ļ���
#��kNN�����ַ�ʶ��
classfierResult=imtools.characterClassifyBykNN(charlist)
print '����ʶ������:',classfierResult
#img_border=cv2.resize(img_border,None,fx=0.5,fy=0.5) #���Ż�ԭ���ĳߴ�

cv2.waitKey(0)
cv2.destroyAllWindows()

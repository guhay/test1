import face_so,face_class
from ctypes import *
import cv2
from io import BytesIO

# from Main import *
c_ubyte_p = POINTER(c_ubyte)
# 激活函数
def JH(appkey,sdkey):
    ret=face_so.jihuo(appkey,sdkey)
    if ret==0:
        return
    else:
        raise Exception("激活失败",ret)
# 初始化函数
def CSH():# 1：视频或图片模式,2角度,3最小人脸尺寸推荐16,4最多人脸数最大50,5功能,6返回激活句柄
    Handle = c_void_p()
    ret=face_so.chushihua(0xFFFFFFFF,0x1,30,1,5,byref(Handle))
    if ret!=0:
        raise Exception("初始化失败",ret)
    return Handle
#销毁引擎
def DUE(Handle):
    ret=face_so.xiaohui(Handle)
    if ret!=0:
        raise  Exception("引擎销毁失败",ret)
# cv2记载图片并处理
def LoadImg(im):
    img=cv2.imread(im.filepath)
    if img is None:
        raise Exception("图片路径错误")
    sp=img.shape
    img=cv2.resize(img,(sp[1]//4*4,sp[0]//4*4))
    sp=img.shape
    im.data=img
    im.width=sp[1]
    im.height=sp[0]
    return im
def RLSB(im,Handle):
    faces=face_class.ASF_MultiFaceInfo()
    imgby=bytes(im.data)
    imgcuby=cast(imgby,c_ubyte_p)
    ret=face_so.shibie(Handle,im.width,im.height,0x201,imgcuby,byref(faces))
    if ret!=0:
        raise Exception("人脸识别失败",ret)
    return faces
# 显示人脸识别图片
def showimg(im,faces):
    for i in range(0,faces.faceNum):
        ra=faces.faceRect[i]
        cv2.rectangle(im.data,(ra.left1,ra.top1),(ra.right1,ra.bottom1),(255,0,0,),2)
    print('-------------')
    cv2.imwrite('test.jpg',im.data)
#提取人脸特征
def RLTZ(im,ft,Handle):
    detectedFaces=face_class.ASF_FaceFeature()
    imgby=bytes(im.data)
    imgcuby=cast(imgby,c_ubyte_p)
    ret=face_so.tezheng(Handle,im.width,im.height,0x201,imgcuby,ft,byref(detectedFaces))
    if ret==0:
        retz = face_class.ASF_FaceFeature()
        retz.featureSize = detectedFaces.featureSize
        # 必须操作内存来保留特征值,因为c++会在过程结束后自动释放内存
        retz.feature = face_so.malloc(detectedFaces.featureSize)
        face_so.memcpy(retz.feature, detectedFaces.feature, detectedFaces.featureSize)
        # print('提取特征成功:',detectedFaces.featureSize,mem)
        return retz
    else:
        raise Exception("提取人脸特征失败",ret)
#特征值比对,返回比对结果
def BD(tz1,tz2,Handle):
    jg=c_float()
    ret=face_so.bidui(Handle,tz1,tz2,byref(jg))
    if ret!=0:
        raise Exception("比对失败",ret)
    return jg.value
#单人特征写入文件
def writeFTFile(feature,filepath):
    f = BytesIO(string_at(feature.feature,feature.featureSize))
    a=open(filepath,'wb')
    a.write(f.getvalue())
    a.close()
#从多人中提取单人数据
def getsingleface(singleface,index):
    ft=face_class.ASF_SingleFaceInfo()
    ra=singleface.faceRect[index]
    ft.faceRect.left1=ra.left1
    ft.faceRect.right1=ra.right1
    ft.faceRect.top1=ra.top1
    ft.faceRect.bottom1=ra.bottom1
    ft.faceOrient=singleface.faceOrient[index]
    return ft
#从文件获取特征值
def ftfromfile(filepath):
    fas=face_class.ASF_FaceFeature()
    f=open(filepath,'rb')
    b=f.read()
    f.close()
    fas.featureSize=b.__len__()
    fas.feature=face_so.malloc(fas.featureSize)
    face_so.memcpy(fas.feature,b,fas.featureSize)
    return fas
# Hnadle=CSH()
# im=face_class.IM()
# im.filepath='/data/yisa_person/249e2c9e2c5eac56a44664c664d6a4d620d6a35622162636622623262f262b06.jpg'
# im=LoadImg(im)
# faces=RLSB(im,Hnadle)
# print(faces.faceNum)
# face=getsingleface(faces,0)
# padtop=20
# padleft=10
# padbottom=10
# padright=10
# top=face.faceRect.top1
# bottom=face.faceRect.bottom1
# left=face.faceRect.left1
# right=face.faceRect.right1
# top=top-padtop if top-padtop>=0 else 0
# left=left-padleft if left-padleft>=0 else 0
# bottom=bottom+padbottom if bottom+padbottom<=im.height else im.height
# right=right+padright if right+padright<im.width else im.width
# crop=im.data[top:bottom,left:right]
# cv2.imwrite('test3.jpg',crop)
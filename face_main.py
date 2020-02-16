import face_so,face_class
from ctypes import *
import cv2
import face_function as fun
import time
import os
from multiprocessing import Pool
from tqdm import tqdm

def cut_save_pic(path,savepath,Handle):
    im = face_class.IM()
    im.filepath = path
    im = fun.LoadImg(im)
    faces = fun.RLSB(im, Handle)
    if faces.faceNum==0:
        return
    face=fun.getsingleface(faces,0)
    padtop = 20
    padleft = 10
    padbottom = 10
    padright = 10
    top = face.faceRect.top1
    bottom = face.faceRect.bottom1
    left = face.faceRect.left1
    right = face.faceRect.right1
    top = top - padtop if top - padtop >= 0 else 0
    left = left - padleft if left - padleft >= 0 else 0
    bottom = bottom + padbottom if bottom + padbottom <= im.height else im.height
    right = right + padright if right + padright < im.width else im.width
    crop = im.data[top:bottom, left:right]
    cv2.imwrite(savepath,crop)
def extract_feature(path,Handle):
    # 加载图片
    im = face_class.IM()
    im.filepath = path
    im = fun.LoadImg(im)
    # print('加载图片完成:')

    faces = fun.RLSB(im,Handle)
    # print('人脸识别成功:')
    ft = fun.getsingleface(faces, 0)
    tz1 = fun.RLTZ(im, ft,Handle)
    return tz1
def compare_feature(feature1,feature2,Handle):
    num=fun.BD(feature1, feature2,Handle)
    return num
def compare_pic(path1,path2):
    Handle=fun.CSH()
    feature1=extract_feature(path1,Handle)
    feature2=extract_feature(path2,Handle)
    num=fun.BD(feature1,feature2,Handle)
    fun.DUE(Handle)
    return round(num,3)
def cutOnePicture(orgpath,savepath):
    Handle=fun.CSH()
    cut_save_pic(orgpath,savepath,Handle)
    fun.DUE(Handle)
def cutPictures(dirpath,savepath):
    Handle=fun.CSH()
    l=os.listdir(dirpath)
    for filename in tqdm(l):
        filepath=os.path.join(dirpath,filename)
        savefile=os.path.join(savepath,filename)
        try:
            cut_save_pic(filepath,savefile,Handle)
        except Exception as err:
            print(str(err))
    fun.DUE(Handle)
def extractFeatures(dirpath,savepath):
    Handle = fun.CSH()
    l=os.listdir(dirpath)
    for filename in tqdm(l):
        filepath=os.path.join(dirpath,filename)
        try:
            feature=extract_feature(filepath,Handle)
            fun.writeFTFile(feature,os.path.join(savepath,filename[:-4]))
        except Exception as err:
            print(str(err))
    fun.DUE(Handle)
# cutPictures('/data/yisa_person/','./static/yisa_person/')
# extractFeatures('./static/yisa_person/','./feature/')
def getAllSavedFeature(dirpath):
    d={}
    l = os.listdir(dirpath)
    for filename in tqdm(l):
        d[filename]=fun.ftfromfile(os.path.join(dirpath,filename))
    return d
def searchSimFromDir(picpath,featuredir='./feature/'):
    Handle=fun.CSH()
    fz=extract_feature(picpath,Handle)
    d=getAllSavedFeature(featuredir)
    for k,v in d.items():
        num=compare_feature(fz,v,Handle)
        d[k]=num
    d=sorted(d.items(),key=lambda x:x[1],reverse=True)
    fun.DUE(Handle)
    return [tmp[0]+'.jpg' for tmp in d[:10]],[round(tmp[1],3) for tmp in d[:10]]




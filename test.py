# import cv2
# import uuid
# cap = cv2.VideoCapture(r"E:\百度云\anjianju100031.mp4")
# total = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 总帧数
# fps = cap.get(cv2.CAP_PROP_FPS)
# second=8
# n=0
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# #指定写视频的格式, I420-avi, MJPG-mp4
# videoWriter = cv2.VideoWriter('oto_other.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, size)
# for i in range(0,int(total),second*int(fps)):
#     try:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, i)
#         cap.grab()  # 解码并返回捕获的视频帧
#     except Exception as e:
#         print(e)
#     # if n>=500:
#     #     break
#     print(i)
#     ret, frame = cap.read()
#     if not ret:
#         continue
#     #cv2.imwrite('E:/zhibanshi/'+str(uuid.uuid1()) + '.jpg', frame)  # 存储为图像
#     videoWriter.write(frame)
#     n+=1
#     cv2.waitKey(5)
#     if n>=15:
#         break
# cap.release()
# videoWriter.release()

# import os
# import shutil
# l=os.listdir('E:/zhibanshi/label')
# for name in l:
#     name=name.split('.')[0]
#     shutil.move('E:/zhibanshi/'+name+'.jpg','E:/zhibanshi/picture/')

import os
import xml.etree.ElementTree as ET

# dirpath = 'G:yisa/aug_label_xml/'     #原来存放xml文件的目录
# newdir = 'G:yisa/aug_label_yolo/'  #修改label后形成的txt目录
dirpath = r'C:\Users\guhay\Desktop\1\pic_res'
newdir = r'C:\Users\guhay\Desktop\1\pic_yolo'

if not os.path.exists(newdir):
    os.makedirs(newdir)

for fp in os.listdir(dirpath):

    root = ET.parse(os.path.join(dirpath, fp)).getroot()

    xmin, ymin, xmax, ymax = 0, 0, 0, 0
    sz = root.find('size')

    width = float(sz[0].text)
    height = float(sz[1].text)
    filename = root.find('filename').text
    for child in root.findall('object'):  # 找到图片中的所有框
        # print(child.find('name').text)

        sub = child.find('bndbox')  # 找到框的标注值并进行读取
        label = child.find('name').text
        xmin = float(sub[0].text)
        ymin = float(sub[1].text)
        xmax = float(sub[2].text)
        ymax = float(sub[3].text)
        try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
            x_center = (xmin + xmax) / (2 * width)
            y_center = (ymin + ymax) / (2 * height)
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height
        except ZeroDivisionError:
            print(filename, '的 width有问题')

        with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
            f.write(' '.join([str(label), str(x_center), str(y_center), str(w), str(h) + '\n']))

# import os
# from shutil import copyfile
#
# xmllist="C:/Users/guhay/Desktop/新建文件夹/test3_res"
# piclist="C:/Users/guhay/Desktop/新建文件夹/test3"
# picsave="C:/Users/guhay/Desktop/新建文件夹/test3_pic"
# l=os.listdir(xmllist)
# for file in l:
#     filename=file.split('.')[0]+'.jpg'
#     copyfile(piclist+'/'+filename,picsave+'/'+filename)
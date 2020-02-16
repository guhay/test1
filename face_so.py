from ctypes import *
from face_class import *

CDLL("./linux_so/libarcsoft_face.so", mode=RTLD_GLOBAL)
d1=CDLL("./linux_so/libtest.so")
dll=CDLL("./linux_so/libarcsoft_face_engine.so")
ASF_DETECT_MODE_VIDEO = 0x00000000
ASF_DETECT_MODE_IMAGE = 0xFFFFFFFF
c_ubyte_p = POINTER(c_ubyte)
#激活
jihuo=dll.ASFActivation
jihuo.restype = c_int32
jihuo.argtypes = (c_char_p,c_char_p)
#初始化
chushihua=dll.ASFInitEngine
chushihua.restype=c_int32
chushihua.argtypes=(c_long,c_int32,c_int32,c_int32,c_int32,POINTER(c_void_p))
#销毁引擎
xiaohui=dll.ASFUninitEngine
xiaohui.restype=c_int32
xiaohui.argtypes=(c_void_p,)
#人脸识别
shibie=dll.ASFDetectFaces
shibie.restype=c_int32
shibie.argtypes=(c_void_p,c_int32,c_int32,c_int32,POINTER(c_ubyte),POINTER(ASF_MultiFaceInfo))
#特征提取
tezheng=dll.ASFFaceFeatureExtract
tezheng.restype=c_int32
tezheng.argtypes=(c_void_p,c_int32,c_int32,c_int32,POINTER(c_ubyte),POINTER(ASF_SingleFaceInfo),POINTER(ASF_FaceFeature))

#特征比对
bidui=dll.ASFFaceFeatureCompare
bidui.restype=c_int32
bidui.argtypes=(c_void_p,POINTER(ASF_FaceFeature),POINTER(ASF_FaceFeature),POINTER(c_float))

malloc=d1.malloc_my
malloc.restype = c_void_p
malloc.argtypes = (c_size_t, )

memcpy = d1.memcpy
memcpy.restype = c_void_p
memcpy.argtypes = (c_void_p, c_void_p, c_size_t)
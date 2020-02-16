import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import ctypes
from face_main import *

UPLOAD_FOLDER = os.getcwd()+'/static/'
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/compare/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file_list=[]
            for index,file in enumerate(request.files.getlist('file')): # 这里改动以存储多份文件
                filepath=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                #保存原始图片
                file.save(filepath)
                #保存剪切以后的人脸图片
                facepath = ''.join(filepath.split('.')[:-1]) + '_face.' + filepath.split('.')[-1]
                cutOnePicture(filepath, facepath)
                file_list.append(facepath)
            similarity = compare_pic(file_list[0], file_list[1])
            return render_template('compare_success.html',similarity=similarity,file=[f.split('/')[-1] for f in file_list])
        except Exception as err:
            return "图片"+str(err)
    return render_template('compare.html')
@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        try:
            #保存原始图片
            file=request.files.getlist('file')[0]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            #保存剪切后人脸图片
            facepath=''.join(filepath.split('.')[:-1])+'_face.'+filepath.split('.')[-1]
            cutOnePicture(filepath,facepath)
            #去数据库中匹配图片
            search_pic,simility=searchSimFromDir(filepath)
            return render_template('search_success.html',orgfile=facepath.split('/')[-1],search_pic=search_pic,simility=simility)
        except Exception as err:
            return "原始图片:"+str(err)
    return render_template('search.html')
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
if __name__=="__main__":
    app.run(host='0.0.0.0')
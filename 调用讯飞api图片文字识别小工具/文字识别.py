import os
import sys
import requests
import time
import hashlib
import base64
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
APPID = "47cfa8ba"
API_KEY = "e50788325d155c916acd2d46a4a6294b"
rootdir = ''

def getHeader():
    curTime = str(int(time.time()))
    param = {"language": "cn|en", "location": "false"}
    param = json.dumps(param)
    paramBase64 = base64.b64encode(param.encode('utf-8'))
    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64,'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header

class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
 
    def __init__(self, dirs):
        super(Runthread, self).__init__()
        self.dirs = dirs
 
    def __del__(self):
        self.wait()
 
    def run(self):
        lis = os.listdir(self.dirs)
        for i in range(0, len(lis)):
            path = os.path.join(self.dirs,lis[i])
            file_path = path
            with open(file_path, 'rb') as f:
                f1 = f.read()
            f1_base64 = str(base64.b64encode(f1), 'utf-8')
            data = {
                    'image': f1_base64
                    }
            r = requests.post(URL, data=data, headers=getHeader())
            result = str(r.content, 'utf-8')
            js = json.loads(result)
            text = ''
            for line in js['data']['block'][0]['line']:
                text += line['word'][0]['content']
            path1 = 'D:/文字识别结果/' + os.path.basename(file_path).split('.')[0] + '.txt'
            file = open(path1, mode='w')
            file.write(text)
            file.flush()
            file.close()
            time.sleep(0.2)
            msg = os.path.basename(file_path) + ' 完成！'
            self._signal.emit(msg)
        time.sleep(0.2)
        self._signal.emit('全部完成，共' + str(len(lis)) + '个文件。')

class Example(QtWidgets.QWidget):
     
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None
        
    def initUI(self):
        font = QtGui.QFont()
        font.setFamily('黑体')
        font.setPointSize(15)
         
        dirs = QLabel('图片所在目录：')
        proc = QLabel('进度：')
 
        self.dirEdit = QLineEdit()
        self.procEdit = QTextEdit()
        self.procEdit.setPlainText('说明：将要识别的图片文件放在同一文件夹下，选择目录后点击开始按钮，识别结果在“D:/文字识别结果”中，若是首次使用，需手动创建该目录。')
        okBtn = QPushButton('开始')
        sBtn = QPushButton('选择目录')
        okBtn.clicked.connect(self.buttonClicked)
        sBtn.clicked.connect(self.sbtnClicked)

        self.dirEdit.setReadOnly(True)
        self.procEdit.setReadOnly(True)
 
        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(dirs, 1, 0)
        grid.addWidget(self.dirEdit, 1, 1)
 
        grid.addWidget(proc, 4, 0)
        grid.addWidget(self.procEdit, 2, 1, 5, 1)

        grid.addWidget(okBtn, 4, 0)
        grid.addWidget(sBtn, 2, 0)
         
        self.setLayout(grid)
        self.resize(600, 500)
        self.setWindowTitle('文字识别')
        self.setFont(font)

    def call_backlog(self, msg):
        self.procEdit.append(msg)

    def sbtnClicked(self):
        rootdir = QFileDialog.getExistingDirectory(self,  "选取文件夹",  'C:/')
        self.dirEdit.setText(rootdir)
        
    def buttonClicked(self):
        dirs = self.dirEdit.text()
        if(dirs != ''):
            self.procEdit.append('识别已经开始，请不要操作，耐心等待！')
            self.thread = Runthread(dirs)
            self.thread._signal.connect(self.call_backlog)
            self.thread.start()
        else:
            QMessageBox.warning(self, '错误', '文件路径不能为空')
         
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

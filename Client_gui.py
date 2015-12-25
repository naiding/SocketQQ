#!/usr/bin/env python
#*-* coding:utf-8 *-*
import sys
from PyQt4 import QtCore, QtGui, uic
from Client import ChatClient
import thread
import time

qtCreatorFile = "./Client.ui" # 读取客户端GUI
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TheClientGUI(QtGui.QMainWindow, Ui_MainWindow):

    # 主机名
    Host = None
    # 端口
    Port = None

    def __init__(self):
        # 初始化GUI            
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 默认主机名为ocalhost
        self.hostEdit.setText('localhost')
        # 将connect按钮与connect_clicked函数连接
        self.connectButton.clicked.connect(self.connect_clicked)
        # 将close按钮与close_clicked函数连接
        self.closeButton.clicked.connect(self.close_clicked)
        # 将send按钮与send_clicked函数连接
        self.sendButton.clicked.connect(self.send_clicked)

    def connect_clicked(self):
        #实例化一个ChatClient
        self.QQClient = ChatClient(self.hostEdit.text(),int(self.portEdit.text()), self.receiveBrower)
        #跑起来
        self.QQClient.run()
        #输出日志
        self.receiveBrower.setText('Connected...\n')
        #开始接收信息
        self.reveive_clicked()

    def send_clicked(self):
        #读取输入框字符串
        string = QtCore.QString(self.sendEdit.toPlainText()).toUtf8()
        #发送
        self.QQClient.send_message(string)
        #将输入端发出的字符串加到接收框
        self.sendEdit.setText('')
        self.receiveBrower.append('%s\n>> %s\n'% (time.ctime(), string))

    def reveive_clicked(self):
        #创建一个线程接收信息
        thread.start_new_thread(self.QQClient.receive_message,())

    def close_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TheClientGUI()
    window.show()
    sys.exit(app.exec_())
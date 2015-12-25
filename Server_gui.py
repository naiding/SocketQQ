#!/usr/bin/env python
#*-* coding:utf-8 *-*
import sys
from PyQt4 import QtCore, QtGui, uic
from Server import ChatServer
import thread

 
qtCreatorFile = "./Server.ui" # 读取服务器端GUI
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) 

class TheServerGUI(QtGui.QMainWindow, Ui_MainWindow):

    # 主机名
    Host = None
    # 端口
    Port = None

    def __init__(self):
        # 初始化GUI
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 将bind按钮与bind_clicked函数连接
        self.bindButton.clicked.connect(self.bind_clicked)
        # 将close按钮与close_clicked函数连接
        self.closeButton.clicked.connect(self.close_clicked)

    def bind_clicked(self):

        # 读取输入的host名称，默认为空''
        Host = self.hostEdit.text()
        # 读取输入的端口名称
        Port = self.portEdit.text()
        # 实例化ChatServer类
        self.QQServer = ChatServer( Host, int(Port), int(10), int(5), self.logBrowser, self.onlineBrowser)
        # 创建一个子线程，跑Server程序
        thread.start_new_thread(self.QQServer.run,())

    def close_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TheServerGUI()
    window.show()
    sys.exit(app.exec_())
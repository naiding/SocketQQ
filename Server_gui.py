import sys
from PyQt4 import QtCore, QtGui, uic
from Server import ChatServer
import thread

qtCreatorFile = "./Server.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TheServerGUI(QtGui.QMainWindow, Ui_MainWindow):

    Host = None
    Port = None

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.bindButton.clicked.connect(self.bind_clicked)
        self.closeButton.clicked.connect(self.close_clicked)


    def bind_clicked(self):
        print 'bind'
        Host = self.hostEdit.text()
        Port = self.portEdit.text()
        self.QQServer = ChatServer( Host, int(Port), int(10), int(5), self.logBrower)
        
        thread.start_new_thread(self.QQServer.run,())


    def close_clicked(self):
        self.QQServer.close()




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TheServerGUI()
    window.show()
    sys.exit(app.exec_())
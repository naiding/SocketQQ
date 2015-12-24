import sys
from PyQt4 import QtCore, QtGui, uic
from Client import ChatClient
import thread

qtCreatorFile = "./Client.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TheClientGUI(QtGui.QMainWindow, Ui_MainWindow):

    Host = None
    Port = None

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.hostEdit.setText('localhost')
        self.connectButton.clicked.connect(self.connect_clicked)
        self.closeButton.clicked.connect(self.close_clicked)
        self.sendButton.clicked.connect(self.send_clicked)

    def connect_clicked(self):
        self.QQClient = ChatClient(self.hostEdit.text(),int(self.portEdit.text()), self.receiveBrower)
        self.QQClient.run()
        self.receiveBrower.setText('Connected...')
        self.reveive_clicked()

    def send_clicked(self):
        string = QtCore.QString(self.sendEdit.toPlainText()).toUtf8()
        self.QQClient.send_message(string)
        self.sendEdit.setText('')

    def reveive_clicked(self):
        thread.start_new_thread(self.QQClient.receive_message,())

    def close_clicked(self):
        print 'close'


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TheClientGUI()
    window.show()
    sys.exit(app.exec_())
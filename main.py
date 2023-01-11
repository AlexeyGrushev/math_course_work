from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

def equations():
    with open('data/profile.txt','r', encoding='utf-8') as f:
        if f.read() == 'None':
            return
        else:
            from loggedin import Ui
            app = QApplication([])
            win = Ui()
            app.setWindowIcon(QtGui.QIcon('data/img/icon.ico'))
            app.exec_()
            with open('data/profile.txt','w', encoding='utf-8') as f:
                f.write('None')
def auth():
    from auth import Ui
    app = QApplication([])
    win = Ui()
    app.setWindowIcon(QtGui.QIcon('data/img/icon.ico'))
    app.exec_()
if __name__ == '__main__':
    auth()
    equations()
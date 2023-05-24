from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from scripts.dbms import DBHelper


def app():
    with open('data/profile.txt', 'r', encoding='utf-8') as f:
        if f.read() == 'None':
            return
        else:
            from app import Ui
            app = QApplication([])
            win = Ui()
            app.setWindowIcon(QtGui.QIcon('data/img/logo.png'))
            app.exec_()
            with open('data/profile.txt','w', encoding='utf-8') as f:
                f.write('None')

def auth():
    from auth import Ui
    app = QApplication([])
    win = Ui()
    app.setWindowIcon(QtGui.QIcon('data/img/logo.png'))
    app.exec_()

if __name__ == '__main__':
    with open('data/profile.txt', 'w', encoding='utf-8') as f:
        f.write('None')
        f.close()
    db = DBHelper()
    db.setup_table()
    auth()
    app()

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QTimer

from scripts.dbms import DBHelper
from scripts.phrase_time_upd import hello_phrase
from scripts.authentication import auth_module
from scripts.registration import reg_module


class Ui(QMainWindow):
    def __init__(self) -> None:
        super(Ui, self).__init__()
        uic.loadUi("GUI/auth.ui", self)
        self.show()
        self.initial_setup()
        pass
    
    def initial_setup(self) -> None:
        self.db = DBHelper()
        self.buttons()
        self.timer()

        self.welcome_lbl.setText(hello_phrase())

        self.auth_switch.setEnabled(False)
        self.auth_switch.setText("АВТОРИЗАЦИЯ >")
        pass

    def buttons(self) -> None:
        self.reg_switch.clicked.connect(self.switch_to_reg)
        self.auth_switch.clicked.connect(self.switch_to_auth)

        self.regBtn.clicked.connect(self.registration)
        self.authBtn.clicked.connect(self.authentication)

        self.tech_supportBtn.clicked.connect(self.tech_support_link)
        pass

    def timer(self) -> None:
        self.cursorPos = 0
        
        self.timer1 = QTimer()
        self.timer1.setInterval(700)
        self.timer1.timeout.connect(self.__timerFunc)
        self.timer1.start()

    def __timerFunc(self) -> None:
        if self.cursorPos == 0:
            self.authLbl.setText("Авторизация|")
            self.regLbl.setText("Регистрация|")
            self.cursorPos = 1
        
        else:
            self.authLbl.setText("Авторизация")
            self.regLbl.setText("Регистрация")
            self.cursorPos = 0
    
    def switch_to_reg(self) -> None:
        self.tabW.setCurrentIndex(1)
        self.login.setText('')
        self.password.setText('')
        
        self.auth_switch.setEnabled(True)
        self.reg_switch.setEnabled(False)

        self.reg_switch.setText("РЕГИСТРАЦИЯ >")
        self.auth_switch.setText("АВТОРИЗАЦИЯ")

        lines = ["firstName","lastName","class_2","loginR","passwordR"]
        for i in lines:
            self.normalEdit(i)
        pass

    def switch_to_auth(self) -> None:
        self.tabW.setCurrentIndex(0)
        
        self.firstName.setText('')
        self.lastName.setText('')
        self.class_2.setText('')
        self.loginR.setText('')
        self.passwordR.setText('')
        
        self.reg_switch.setEnabled(True)
        self.auth_switch.setEnabled(False)

        self.reg_switch.setText("РЕГИСТРАЦИЯ")
        self.auth_switch.setText("АВТОРИЗАЦИЯ >")

        lines = ["login","password"]
        for i in lines:
            self.normalEdit(i)

    def normalEdit(self,element) -> None:
        with open("data/stylesheet/editLineNormal.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
    
    def errEdit(self,element) -> None:
        with open("data/stylesheet/editLineError.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
    
    def authentication(self) -> None:
        textNull = 0
        if self.login.text() == '':
            self.errEdit("login")
            textNull += 1
        if self.password.text() == '':
            self.errEdit("password")
            textNull += 1
        pass
        
        if textNull == 1:
            QMessageBox.critical(
                self,
                "Авторизация",
                "Заполните подсвечимое поле"
            )
        elif textNull == 2:
            QMessageBox.critical(
                self,
                "Авторизация",
                "Заполните подсвечиваемые поля"
            )
        else:
            user_data = [
                   self.login.text(),
                   self.password.text()
                ]
            
            profile = auth_module(user_data)
            if profile == None:
                QMessageBox.warning(
                    self,
                    "Авторизация",
                    "Неверный логин или пароль"
                )
                return
            else:
                with open('data/profile.txt', 'w', encoding='utf-8') as f:
                    f.write(str(profile))
                QApplication.exit()
           
    
    def tech_support_link(self) -> None:
        import webbrowser
        webbrowser.open("https://t.me/mytestisp_bot")
        pass

    def registration(self) -> None:
        reg_module(self)
        pass

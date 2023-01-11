from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from datetime import datetime
import sqlite3 as sq
from PyQt5.QtCore import QTimer

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("GUI/auth.ui", self)
        self.cursorPos = 0
        self.show()
        self.logic()
        self.timeUpd()
        self.startPreset()
        
# Подключаем кнопки
    def logic(self):
        self.reg_switch.clicked.connect(self.switch_to_reg)
        self.auth_switch.clicked.connect(self.switch_to_auth)

        self.regBtn.clicked.connect(self.registration)
        self.authBtn.clicked.connect(self.authentication)


# Таймер с анимацией курсора
    def timer(self):
        self.timer1 = QTimer()
        self.timer1.setInterval(700)
        self.timer1.timeout.connect(self.__timerFunc)
        self.timer1.start()

# Метод, который и выполняет таймер
    def __timerFunc(self):
        if self.cursorPos == 0:
            self.authLbl.setText("Авторизация|")
            self.regLbl.setText("Регистрация|")
            self.cursorPos = 1
        
        else:
            self.authLbl.setText("Авторизация")
            self.regLbl.setText("Регистрация")
            self.cursorPos = 0

# Действия, которые выполняются при запуске приложения
    def startPreset(self):
        
        # Подсказки для полей ввода при авторизации
        self.login.setPlaceholderText("Логин...")
        self.password.setPlaceholderText("Пароль...")
        
        # Подсказки для полей ввода при регистрации
        self.firstName.setPlaceholderText("Имя...")
        self.lastName.setPlaceholderText("Фамилия...")
        self.class_2.setPlaceholderText("Класс...")
        self.loginR.setPlaceholderText("Логин...")
        self.passwordR.setPlaceholderText("Пароль...")
        
        # Команда, чтобы окно приветствия всегда открывалось с авторизации
        self.tabW.setCurrentIndex(0)
        
        # Запуск таймера на анимацию
        self.timer()

        # Так как изначально открывается авторизация, а не регистрация, то мы выключаем кнопку "АВТОРИЗАЦИЯ" и добавляем обозначение, что мы находимся именно на этой вкладке
        self.auth_switch.setEnabled(False)
        self.auth_switch.setText("АВТОРИЗАЦИЯ >")

        # Очищаем файл с ID профиля
        with open('data/profile.txt', 'w', encoding='utf-8') as f:
            f.write("None")

        # Установка иконки приложения
        # Ui.setWindowIcon(QtGui.QIcon('data/img/icon.ico'))
    
# Метод переключения на окно регистрации
    def switch_to_reg(self):
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
    
# Метод переключения на авторизацию
    def switch_to_auth(self):
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

# Проверка времени и вывод надписи в соответствии со временем суток
    def timeUpd(self):
        date = datetime.now()
        hour = date.hour
        if hour >= 0 and hour < 6:
            self.welcome_lbl.setText("Доброй ночи, пользователь.")
        
        if hour >= 6 and hour < 12:
            self.welcome_lbl.setText("Доброе утро, пользователь.")

        if hour >= 12 and hour < 18:
            self.welcome_lbl.setText("Добрый день, пользователь.")

        if hour >= 18 and hour < 24:
            self.welcome_lbl.setText("Добрый вечер, пользователь.")

# Графическое обозначение ошибки в EditLine
    def errEdit(self,element):
        with open("data/stylesheet/editLineError.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")

    def normalEdit(self,element):
        with open("data/stylesheet/editLineNormal.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
        
# Срабатывает при нажатии кнопки регистрация
    def registration(self):
        textNull = 0
        nullLines = []
        lines = ["firstName","lastName","class_2","loginR","passwordR"]
        
        # Удаляем все пробелы из полей ввода
        for i in lines:
            line = eval(f"self.{i}.text()")
            while ' ' in line:
                line = line.replace(' ','')
            exec(f"self.{i}.setText('{line}')")

        # Проверяем не являются ли поля регистрации пустыми. Если пустые, то подсвечиваем их и выводим сообщение об ошибке с именами полей, которые необходимо заполнить
        if self.firstName.text() == '':
            self.errEdit("firstName")
            textNull += 1
            nullLines.append("Имя")
        if self.lastName.text() == '':
            self.errEdit("lastName")
            textNull += 1
            nullLines.append("Фамилия")
        if self.class_2.text() == '':
            self.errEdit("class_2")
            textNull += 1
            nullLines.append("Класс")
        if self.loginR.text() == '':
            self.errEdit("loginR")
            textNull += 1
            nullLines.append("Логин")
        if self.passwordR.text() == '':
            self.errEdit("passwordR")
            textNull += 1
            nullLines.append("Пароль")
        
        if textNull == 1:
            attention3 = QMessageBox()
            attention3.setWindowTitle("Ошибка")
            attention3.setText(f"Заполните следующее поле:\n{nullLines[0]}")
            attention3.setIcon(QMessageBox.Critical)
            attention3.setStandardButtons(QMessageBox.Ok)
            attention3.exec_()
            return
        
        elif textNull > 1:
            attention4 = QMessageBox()
            attention4.setWindowTitle("Ошибка")
            attention4.setText(f"Заполните следующее поле:\n")
            for i in nullLines:
                attention4.setText(attention4.text()+i+'\n')
            attention4.setIcon(QMessageBox.Critical)
            attention4.setStandardButtons(QMessageBox.Ok)
            attention4.exec_()
            return
    
        else:
            try:
                # Вносим данные о пользователе в базу данных
                with sq.connect("data/database.db") as db:
                    cur = db.cursor()
                    cur.execute(
                        f""" INSERT INTO accounts (Login, Password) VALUES ("{self.loginR.text()}", "{self.passwordR.text()}") """
                    )
                    cur.execute(f""" INSERT INTO students (FirstName, LastName, Class2) VALUES ("{self.firstName.text()}", "{self.lastName.text()}", "{self.class_2.text()}") """)
                    cur.execute(f""" INSERT INTO stats (eqTrue,eqFalse,eqSkip,graps) VALUES (0,0,0,0) """)
                    db.commit()
                # Выводим сообщение, что пользователь зарегистрирован успешно
                information1 = QMessageBox()
                information1.setWindowTitle("Регистрация")
                information1.setText(f"Пользователь с логином {self.loginR.text()} успешно зарегистрирован")
                information1.setIcon(QMessageBox.Information)
                information1.setStandardButtons(QMessageBox.Ok)
                information1.exec_()

                # Автоматически перебрасываем пользователя на окно авторизации
                self.switch_to_auth()

            except:
                # Если не получилось зарегестрировать пользователя, то выводится ошибка, что пользователеть с таким именем уже существует
                self.loginR.selectAll()
                attention5 = QMessageBox()
                attention5.setWindowTitle("Регистрация")
                attention5.setText(f"Пользователь с логином {self.loginR.text()} уже существует\nВ случае, если это ошибка, обратитесь к преподавателю")
                attention5.setIcon(QMessageBox.Critical)
                attention5.setStandardButtons(QMessageBox.Ok)
                attention5.exec_()
                
                return

# Срабатывает при нажатии кнопки авторизация
    def authentication(self):
        # Проверяем на пустоту поля логин и пароль и запоминаем, что они пустые
        textNull = 0
        if self.login.text() == '':
            self.errEdit("login")
            textNull += 1
        if self.password.text() == '':
            self.errEdit("password")
            textNull += 1
        
        if textNull == 1:
            attention1 = QMessageBox()
            attention1.setWindowTitle("Авторизация")
            attention1.setText("Заполните подсвечиваемое поле")
            attention1.setIcon(QMessageBox.Critical)
            attention1.setStandardButtons(QMessageBox.Ok)
            attention1.exec_()
            return
        elif textNull == 2:
            attention2 = QMessageBox()
            attention2.setWindowTitle("Авторизация")
            attention2.setText("Заполните подсвечиваемые поля")
            attention2.setIcon(QMessageBox.Critical)
            attention2.setStandardButtons(QMessageBox.Ok)
            attention2.exec_()
        else:
            try:
                with sq.connect("data/database.db") as db:
                    cur = db.cursor()
                    cur.execute(f""" SELECT Id, Login, Password FROM accounts WHERE Login == "{self.login.text()}" AND Password == "{self.password.text()}" """)
                    data = cur.fetchall()
                    print(data[0][0])
                if data[0][1] == self.login.text() and data[0][2] == self.password.text():
                    with open('data/profile.txt', 'w', encoding='utf-8') as f:
                        f.write(str(data[0][0]))
                    QApplication.quit()
            except:
                attention6 = QMessageBox()
                attention6.setWindowTitle("Авторизация")
                attention6.setText("Неверный логин или пароль")
                attention6.setIcon(QMessageBox.Critical)
                attention6.setStandardButtons(QMessageBox.Ok)
                attention6.exec_()
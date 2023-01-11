from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
import sqlite3 as sq
from PyQt5.QtCore import QTimer
from datetime import datetime
from PyQt5.QtGui import QPixmap
import math

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("GUI/main.ui", self)
        self.show()
        self.logic()
        self.loadProfile()
        self.timeUpd()
        self.startPreset()
        self.update()
        
        self.hintLevel = 0
        self.correct = 0
        self.incorrect = 0
        self.skipped = 0

    def loadProfile(self):
        with open('data/profile.txt', 'r', encoding='utf-8') as f:
            id = f.read()
        try:
            with sq.connect('data/database.db') as db:
                cur = db.cursor()
                cur.execute(f""" SELECT Login FROM accounts WHERE Id == {id} """)
                self.profileId = id
                self.profileLogin = cur.fetchall()[0][0]
                
                cur.execute(f""" SELECT FirstName, LastName, Class2 FROM students WHERE Id == {id} """)
                data = cur.fetchall()
                self.profileFristName = data[0][0]
                self.profileLastName = data[0][1]
                self.profileClass = data[0][2]
                
                self.errorAuth = False

                cur.execute(f""" SELECT eqTrue FROM stats WHERE Id == {id} """)

                self.eqTrue = cur.fetchall()[0][0]


        except:
            self.errorAuth = True
            self.profileId = "unknown"
            self.profileFristName = "Неизвестный пользователь"

            self.idLblMain.setText("ID:" + str(self.profileId))
            self.weclomeLblMain.setText("Вход не выполнен, произошла ошибка авторизации, перезапустите программу")
            self.profileLblTitle.hide()
            self.tutorialLbl.hide()

            navBtn = ('equationSwitch','graphicSwitch','tutorialSwitch','statSwitch')
            for i in navBtn:
                self.inactiveBtn(i)


    def startPreset(self):
        self.tabW.setCurrentIndex(0)
        if self.errorAuth:
            return
        self.profileLblTitle.setText("Вход выполнен, профиль: " + self.profileLogin)
        
        self.idLblMain.setText("ID:" + str(self.profileId))

        if self.eqTrue >= 1:
            self.tutorialLbl.hide()

    def inactiveBtn(self,element):
        with open("data/stylesheet/btnInactive.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
            exec(f"""self.{element}.setEnabled(False)""")

    def activeBtn(self, element):
        with open("data/stylesheet/btnActive.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
            exec(f"""self.{element}.setEnabled(True)""")

    def navigateArrow(self,element):
        self.equationSwitch.setText("УРАВНЕНИЯ")
        self.graphicSwitch.setText("ГРАФИКИ")
        self.tutorialSwitch.setText("ОБУЧЕНИЕ")
        self.statSwitch.setText("СТАТИСТИКА")
        
        navBtn = ('equationSwitch','graphicSwitch','tutorialSwitch','statSwitch')
        for i in navBtn:
            exec(f"""self.{i}.setEnabled(True)""")

        exec(f"self.{element}.setText(self.{element}.text() + ' >')")
        exec(f"self.{element}.setEnabled(False)")

    def root_search(self,b,c):
        a = 1
        self.discr = b ** 2 - 4 * a * c
        if self.discr > 0:
            x1 = (-b + math.sqrt(self.discr)) / (2 * a)
            x2 = (-b - math.sqrt(self.discr)) / (2 * a)
            return x1, x2
        elif self.discr == 0:
            x = -b / (2 * a)
            return x
        else:
            return False
    
    def update(self):
        from random import randint
        self.c1 = randint(1,20)
        self.c2 = randint(1,20)
        self.equation.setText(f"x²+{self.c1}x+{self.c2}=0")
        self.roots = self.root_search(self.c1,self.c2)
        if self.roots == False:
            self.update()
            return
        else:
            try:
                self.roots[0]; self.roots[1]
                self.hintReset()
                if (self.roots[0].is_integer()) == False or (self.roots[1].is_integer()) == False:
                    self.update()
            except:
                self.update()
                return
    
    
    def answer(self):
        try:
            if int(self.x1_line.text()) == int(self.roots[0]) and int(self.x2_line.text()) == int(self.roots[1]) or int(self.x1_line.text()) == int(self.roots[1]) and int(self.x2_line.text()) == int(self.roots[0]):
                self.correct += 1
                self.correct_lbl.setText(f"Решены верно: {self.correct}")
                mb = QMessageBox()
                mb.setWindowTitle("Уравнения")
                mb.setText("Значения корней совпадают с Вашим решением!")
                mb.setIcon(QMessageBox.Information)
                mb.setStandardButtons(QMessageBox.Ok)
                mb.exec_()
                self.update()
                
                with sq.connect('data/database.db') as db:
                    cur = db.cursor()
                    cur.execute(f"UPDATE stats SET eqTrue = (eqTrue + 1) WHERE Id == {self.profileId}")
                    db.commit()
                
            else:
                self.incorrect += 1
                self.incorrect_lbl.setText(f"Решены неверно: {self.incorrect}")
                mb = QMessageBox()
                mb.setWindowTitle("Уравнения")
                mb.setText("Значения корней не совпадают с Вашим решением!")
                mb.setIcon(QMessageBox.Critical)
                mb.setStandardButtons(QMessageBox.Ok)
                mb.exec_()
                self.update()

                with sq.connect('data/database.db') as db:
                    cur = db.cursor()
                    cur.execute(f"UPDATE stats SET eqFalse = (eqFalse + 1) WHERE Id == {self.profileId}")
                    db.commit()

        except:
                mb = QMessageBox()
                mb.setWindowTitle("Уравнения")
                mb.setText("Неверный формат данных!")
                mb.setIcon(QMessageBox.Critical)
                mb.setStandardButtons(QMessageBox.Ok)
                mb.exec_()
        finally:
            self.x1_line.setText('')
            self.x2_line.setText('')

    def skip(self):
        self.skipped+=1
        self.skip_lbl.setText(f"Пропущены: {self.skipped}")
        self.update()

        self.x1_line.setText('')
        self.x2_line.setText('')

        with sq.connect('data/database.db') as db:
                    cur = db.cursor()
                    cur.execute(f"UPDATE stats SET eqSkip = (eqSkip + 1) WHERE Id == {self.profileId}")
                    db.commit()
        return
    
    def hintReset(self):
        self.dHint.setText("D=?")
        self.x1Hint.setText("x1=?")
        self.x2Hint.setText("x2=?")
        self.hint_btn.setText("Подсказка (0/3)")
        
        self.hintLevel = 0
        
        self.activeBtn("hint_btn")
        self.activeBtn("ans_btn")
        return


    def hint(self):
        if self.hintLevel == 0:
            self.dHint.setText(f"D={self.discr}")
            self.hint_btn.setText("Подсказка (1/3)")
            self.hintLevel = 1
            return

        if self.hintLevel == 1:
            self.x1Hint.setText(f"x1={int(self.roots[0])}")
            self.hint_btn.setText("Подсказка (2/3)")
            self.hintLevel = 2
            return

        if self.hintLevel == 2:
            self.x2Hint.setText(f"x2={int(self.roots[1])}")
            self.hint_btn.setText("Подсказка (3/3)")
            self.inactiveBtn("ans_btn")
            self.inactiveBtn("hint_btn")
            return


# Проверка времени и вывод надписи в соответствии со временем суток
    def timeUpd(self):
        date = datetime.now()
        hour = date.hour
        if hour >= 0 and hour < 6:
            self.welcome_lbl.setText(f"Доброй ночи, {self.profileFristName}.")
        
        if hour >= 6 and hour < 12:
            self.welcome_lbl.setText(f"Доброе утро, {self.profileFristName}.")

        if hour >= 12 and hour < 18:
            self.welcome_lbl.setText(f"Добрый день, {self.profileFristName}.")

        if hour >= 18 and hour < 24:
            self.welcome_lbl.setText(f"Добрый вечер, {self.profileFristName}.")

    
    def logic(self):
        self.exitBtn.clicked.connect(self.exit)

        self.equationSwitch.clicked.connect(self.switchEquations)
        self.graphicSwitch.clicked.connect(self.switchGraphics)
        self.tutorialSwitch.clicked.connect(self.switchTutorial)
        self.statSwitch.clicked.connect(self.switchStatistics)

        self.ans_btn.clicked.connect(self.answer)
        self.rand_btn.clicked.connect(self.skip)
        self.hint_btn.clicked.connect(self.hint)

        self.createGraphBtn.clicked.connect(self.createGraph)
        self.clearGraphBtn.clicked.connect(self.clearGraph)

        self.saveStat.clicked.connect(self.saveStatistic)

    def createGraph(self):
        from graphic import graphic
        try:
            graphic(self.graphLine.text())
            self.graphicLbl.setPixmap(QPixmap('data/img/graphic.png'))
            with sq.connect('data/database.db') as db:
                    cur = db.cursor()
                    cur.execute(f"UPDATE stats SET graps = (graps + 1) WHERE Id == {self.profileId}")
                    db.commit()
        except:
            self.graphicLbl.setPixmap(QPixmap('data/img/graphicError.png'))
        finally:
            self.graphLine.setText('')

    def clearGraph(self):
        self.graphicLbl.setPixmap(QPixmap())
        self.graphLine.setText('')
    
    def switchEquations(self):
        self.tabW.setCurrentIndex(1)
        self.navigateArrow("equationSwitch")

    def switchGraphics(self):
        self.tabW.setCurrentIndex(2)
        self.navigateArrow("graphicSwitch")

    def switchTutorial(self):
        self.tabW.setCurrentIndex(3)
        self.navigateArrow("tutorialSwitch")

    def switchStatistics(self):
        self.tabW.setCurrentIndex(4)
        self.navigateArrow("statSwitch")

        with sq.connect('data/database.db') as db:
                cur = db.cursor()
                cur.execute(f""" SELECT eqTrue, eqFalse, eqSkip, graps FROM stats WHERE Id == {self.profileId} """)
                data = cur.fetchall()
                eqTrue = data[0][0]
                eqFalse = data[0][1]
                eqSkip1 = data[0][2]
                graps = data[0][3]
        
        self.idStat.setText(f"ID: {self.profileId}")
        self.loginStat.setText(f"Логин: {self.profileLogin}")
        self.nameStat.setText(f"Имя: {self.profileFristName}")
        self.lastnameStat.setText(f"Фамилия: {self.profileLastName}")
        self.classStat.setText(f"Класс: {self.profileClass}")

        self.eqTrueStat.setText(f"Решено верно всего: {str(eqTrue)}")
        self.eqFalseStat.setText(f"Решено неверно всего: {str(eqFalse)}")
        self.eqSkip.setText(f"Пропущено всего: {str(eqSkip1)}")
        self.graph.setText(f"Построено графиков: {str(graps)}")
    
    def saveStatistic(self):
        import os
        homeDir = os.path.expanduser('~')
        with open(f'{homeDir}\Desktop\Статистика {self.profileLogin}.txt', 'w', encoding='utf-8') as f:
            f.write(
f"""{datetime.now()}
Статистика пользователя:
ID: {self.profileId}
Логин: {self.profileLogin}
Имя: {self.profileFristName}
Фамилия: {self.profileLastName}
Класс: {self.profileClass}

{self.eqTrueStat.text()}
{self.eqFalseStat.text()}
{self.eqSkip.text()}
{self.graph.text()}
"""
            )
        mb = QMessageBox()
        mb.setWindowTitle("Статистика")
        mb.setText("Статистика профиля сохранена на рабочий стол")
        mb.setIcon(QMessageBox.Information)
        mb.setStandardButtons(QMessageBox.Ok)
        mb.exec_()


    
    def exit(self):
        with open('data/profile.txt', 'w', encoding='utf-8') as f:
            f.write("None")
        QApplication.quit()
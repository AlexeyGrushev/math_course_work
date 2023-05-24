import os
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

from scripts.equations import Equations
from scripts.dbms import DBHelper
from scripts.phrase_time_upd import hello_phrase
from scripts.equations import Equations


class Ui(QMainWindow):
    def __init__(self) -> None:
        super(Ui, self).__init__()
        uic.loadUi("GUI/main.ui", self)
        self.show()
        self.initial_setup()
        pass

    def initial_setup(self) -> None:
        self.db = DBHelper()
        self.errorAuth = False
        self.load_profile()
        if self.errorAuth:
            return
        self.buttons()
        self.equation_update()

        self.welcome_lbl.setText(hello_phrase().replace(
            "пользователь",
            f"{self.profileFristName}"
        ))

        self.x1_line.setValidator(QtGui.QIntValidator())
        self.x2_line.setValidator(QtGui.QIntValidator())

        self.hintLevel = 0
        self.correct = 0
        self.incorrect = 0
        self.skipped = 0
        pass
    
    def load_profile(self) -> None:
        with open("data/profile.txt", 'r', encoding='utf-8') as f:
            self.id = f.read()
        try:
            self.profileLogin = self.db.user_profile_load(self.id)[0][0]
            
            data = self.db.user_profile_info_load(self.id)
            self.profileFristName = data[0][0]
            self.profileLastName = data[0][1]
            self.profileClass = data[0][2]

            self.idLblMain.setText("ID:" + str(self.id))
            self.profileLblTitle.setText(
                "Вход выполнен, профиль: " + self.profileLogin
                )

            if self.db.user_eqTrue_stat_load(self.id) >= 1:
                self.tutorialLbl.hide()

        except Exception:
            self.errorAuth = True
            self.welcome_lbl.setText("Неизвестный пользователь")

            self.idLblMain.setText("ID:" + "unknown")
            self.weclomeLblMain.setText(
                "Вход не выполнен, произошла ошибка авторизации, перезапустите программу"
                )
            self.profileLblTitle.hide()
            self.tutorialLbl.hide()

            navBtn = ('equationSwitch','graphicSwitch','tutorialSwitch','statSwitch')
            for i in navBtn:
                self.inactiveBtn(i)
        pass

    def buttons(self) -> None:
        self.equationSwitch.clicked.connect(self.switchEquations)
        self.graphicSwitch.clicked.connect(self.switchGraphics)
        self.tutorialSwitch.clicked.connect(self.switchTutorial)
        self.statSwitch.clicked.connect(self.switchStatistics)

        self.ans_btn.clicked.connect(self.answer)
        self.rand_btn.clicked.connect(self.skip)
        self.hint_btn.clicked.connect(self.hint)

        self.createGraphBtn.clicked.connect(self.create_graphic)
        self.clearGraphBtn.clicked.connect(self.clear_graphic)

        self.exitBtn.clicked.connect(self.exit)
        self.saveStat.clicked.connect(self.saveStatistic)
        pass

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
    
    def inactiveBtn(self,element):
        with open("data/stylesheet/btnInactive.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
            exec(f"""self.{element}.setEnabled(False)""")

    def activeBtn(self, element):
        with open("data/stylesheet/btnActive.txt", "r", encoding="UTF-8") as f:
            exec(f"""self.{element}.setStyleSheet({f.read()})""")
            exec(f"""self.{element}.setEnabled(True)""")
    
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

        stats = self.db.user_statistics_load(self.id)

        self.idStat.setText(f"ID: {self.id}")
        self.loginStat.setText(f"Логин: {self.profileLogin}")
        self.nameStat.setText(f"Имя: {self.profileFristName}")
        self.lastnameStat.setText(f"Фамилия: {self.profileLastName}")
        self.classStat.setText(f"Класс: {self.profileClass}")

        self.eqTrueStat.setText(f"Решено верно всего: {str(stats[0][0])}")
        self.eqFalseStat.setText(f"Решено неверно всего: {str(stats[0][1])}")
        self.eqSkip.setText(f"Пропущено всего: {str(stats[0][2])}")
        self.graph.setText(f"Построено графиков: {str(stats[0][3])}")

    def equation_update(self) -> None:
        self.x1_line.setText('')
        self.x2_line.setText('')
        self.hintReset()
        
        data = Equations().get_equation()
        self.equation.setText(data[0])
        self.discriminant = data[1]
        self.root1 = data[2]
        self.root2 = data[3]
        pass

    def answer(self) -> None:
        try:
            if (
                int(
                self.x1_line.text()
                ) == int(
                self.root1
                ) and
                int(
                self.x2_line.text()
                ) == int(
                self.root2
                ) or
                int(
                self.x1_line.text()
                ) == int(
                self.root2
                ) and
                int(
                self.x2_line.text()
                ) == int(
                self.root1
                )
            ):
                self.correct += 1
                self.correct_lbl.setText(
                    f"Решены верно: {self.correct}"
                )
                QMessageBox.information(
                    self,
                    "Уравнения",
                    "Значения корней совпадают с решением!"
                )
                self.db.user_correct_eq_update(self.id)
                self.equation_update()
            else:
                self.incorrect += 1
                self.incorrect_lbl.setText(
                    f"Решены неверно: {self.incorrect}"
                )
                QMessageBox.critical(
                    self,
                    "Уравнения",
                    "Значения корней не совпадают с решением!"
                )
                self.db.user_incorrect_eq_update(self.id)
                self.equation_update()
        except Exception:
            QMessageBox.warning(
                self,
                "Уравнения",
                "Заполните поля для ответа!"
            )
        pass

    def skip(self) -> None:
        self.skipped += 1
        self.skip_lbl.setText(
            f"Пропущены: {self.skipped}"
        )
        self.equation_update()
        self.db.user_skip_eq_update(self.id)
        pass

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
            self.dHint.setText(f"D={self.discriminant}")
            self.hint_btn.setText("Подсказка (1/3)")
            self.hintLevel = 1
            return

        if self.hintLevel == 1:
            self.x1Hint.setText(f"x1={int(self.root1)}")
            self.hint_btn.setText("Подсказка (2/3)")
            self.hintLevel = 2
            return

        if self.hintLevel == 2:
            self.x2Hint.setText(f"x2={int(self.root2)}")
            self.hint_btn.setText("Подсказка (3/3)")
            self.inactiveBtn("ans_btn")
            self.inactiveBtn("hint_btn")
            return
    
    def create_graphic(self):
        from scripts.graphic import graphic_module
        if self.graphLine.text() == '':
            QMessageBox.critical(
                self,
                "Графики",
                "Поле не должно быть пустым!"
            )
            return
        try:
            graphic_module(self.graphLine.text().lower())
            self.graphicLbl.setPixmap(
                QPixmap("data/img/graphic.png")
            )
            self.db.user_graphic_update(self.id)
        except Exception:
            self.graphicLbl.setPixmap(QPixmap('data/img/graphicError.png'))
        finally:
            self.graphLine.setText('')
    
    def clear_graphic(self):
        self.graphicLbl.setPixmap(QPixmap())
        self.graphLine.setText('')

    def saveStatistic(self):
        try:
            homeDir = os.path.expanduser('~')
            with open(f'{homeDir}\Desktop\Статистика {self.profileLogin}.txt', 'w', encoding='utf-8') as f:
                f.write(
f"""{datetime.now()}
Статистика пользователя:
ID: {self.id}
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
            QMessageBox.information(
                self,
                "Статистика",
                "Статистика профиля сохранена на рабочий стол"
            )
        except Exception:
            QMessageBox.critical(
                self,
                "Статистика",
                "Не удалось сохранить статистику!"
            )
    def exit(self):
        with open('data/profile.txt', 'w', encoding='utf-8') as f:
            f.write("None")
        QApplication.quit()

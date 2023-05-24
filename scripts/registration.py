from PyQt5.QtWidgets import QMessageBox


def reg_module(self):
        textNull = 0
        nullLines = []
        lines = ["firstName","lastName","class_2","loginR","passwordR"]
        
        for i in lines:
            line = eval(f"self.{i}.text()")
            while ' ' in line:
                line = line.replace(' ','')
            exec(f"self.{i}.setText('{line}')")

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
            QMessageBox.critical(
                self,
                "Ошибка",
                "Заполните следующие поле:\n" +
                f"{nullLines[0]}"
            )
            return
        
        elif textNull > 1:
            attention = QMessageBox()
            attention.setWindowTitle("Ошибка")
            attention.setText(f"Заполните следующие поля:\n")
            for i in nullLines:
                attention.setText(attention.text() + i + '\n')
            attention.setIcon(QMessageBox.Critical)
            attention.exec_()
            return
    
        else:
            user_data = [
                self.loginR.text(),
                self.passwordR.text(),
                self.firstName.text(),
                self.lastName.text(),
                self.class_2.text()
            ]
            try:
                self.db.user_registration(user_data)
                QMessageBox.information(
                    self,
                    "Регистрация",
                    f"Пользователь с логином {user_data[0]} успешно зарегистрирован"
                )
                self.switch_to_auth()
            except Exception:
                QMessageBox.critical(
                    self,
                    "Регистрация",
                    f"Пользователь с логином {user_data[0]} уже существует"
                )
        pass

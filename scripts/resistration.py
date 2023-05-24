from PyQt5.QtWidgets import QMessageBox


def test_scr():
    from auth import Ui
    win = Ui()
    win.welcome_lbl.setText("TEST")
    QMessageBox(
        win,
        "TEST",
        "TEST"
    )
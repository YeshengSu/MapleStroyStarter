import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTabWidget, QMainWindow, QWidget, QDialog

from Script import Utils, Language
from Script.MainWindow import Ui_MainWindow
from Script.NewAccount import Ui_NewAccountWidget
from Script.ResetPassword import Ui_ResetPasswordWidget


class NewAccountWidget(QDialog, Ui_NewAccountWidget):
    def __init__(self, parent=None):
        super(NewAccountWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        def cb():
            print ('confirm')
            print('account:', self.AccountEdit.text())
            print('password:', self.NewPasswordEdit.text())

        Utils.popup_confirm(self, Language.NEW_ACCOUNT_POPUP_TITLE, Language.NEW_ACCOUNT_POPUP_CONTENT, cb)

    def on_clicked_return(self):
        self.close()



class ResetPasswordWindow(QDialog, Ui_ResetPasswordWidget):
    def __init__(self, parent=None):
        super(ResetPasswordWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        def cb():
            print('confirm')
            print('account:', self.AccountEdit.text())
            print('old password:', self.OldPasswordEdit.text())
            print('new password:', self.NewPasswordEdit.text())

        Utils.popup_confirm(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.RESET_PASSWORD_POPUP_CONTENT, cb)

    def on_clicked_return(self):
        self.close()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.LoginButton.clicked.connect(self.on_clicked_login)
        self.ResetButton.clicked.connect(self.on_clicked_reset)
        self.RegisterButton.clicked.connect(self.on_clicked_register)

    def on_clicked_login(self):
        print ('login')

    def on_clicked_reset(self):
        widget = ResetPasswordWindow()
        widget.exec()

    def on_clicked_register(self):
        widget = NewAccountWidget()
        widget.exec()


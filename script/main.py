import webbrowser

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QDialog, QTreeWidgetItem, QLineEdit

from script import utils, language
from ui.MainWindow import Ui_MainWindow
from ui.NewAccount import Ui_NewAccountWidget
from ui.ResetPassword import Ui_ResetPasswordWidget
from ui.TopUp import Ui_TopUp

_translate = QtCore.QCoreApplication.translate

TEST_IP = '47.241.186.78 9595'

ORANGE_COLOR = QColor(255, 193, 37)
RED_COLOR = QColor(238, 99, 99)
GREEN_COLOR = QColor(0, 255, 127)
YELLOW_COLOR = QColor(255, 200, 0)

class NewAccountWidget(QDialog, Ui_NewAccountWidget):
    def __init__(self, parent=None):
        super(NewAccountWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(utils.HEAD_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.NewPasswordEdit.setEchoMode(QLineEdit.Password)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        if not self.AccountEdit.text():
            utils.popup_warning(self, language.RESET_PASSWORD_POPUP_TITLE, language.EMPTY_ACCOUNT)
            return

        if not self.NewPasswordEdit.text():
            utils.popup_warning(self, language.RESET_PASSWORD_POPUP_TITLE, language.EMPTY_PASSWORD)
            return

        def cb1():
            def cb2():
                print('new account')
                print('account:', self.AccountEdit.text())
                print('password:', self.NewPasswordEdit.text())
                self.close()
            utils.popup_infomation(self, language.NEW_ACCOUNT_POPUP_TITLE, language.NEW_ACCOUNT_POPUP_SUCCEED, cb2)

        utils.popup_confirm(self, language.NEW_ACCOUNT_POPUP_TITLE, language.NEW_ACCOUNT_POPUP_CONTENT, cb1)

    def on_clicked_return(self):
        self.close()



class ResetPasswordWidget(QDialog, Ui_ResetPasswordWidget):
    def __init__(self, parent=None):
        super(ResetPasswordWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(utils.HEAD_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.NewPasswordEdit.setEchoMode(QLineEdit.Password)
        self.OldPasswordEdit.setEchoMode(QLineEdit.Password)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        if not self.AccountEdit.text():
            utils.popup_warning(self, language.RESET_PASSWORD_POPUP_TITLE, language.EMPTY_ACCOUNT)
            return

        if not self.OldPasswordEdit.text() or not self.NewPasswordEdit.text():
            utils.popup_warning(self, language.RESET_PASSWORD_POPUP_TITLE, language.EMPTY_PASSWORD)
            return

        if self.OldPasswordEdit.text() == self.NewPasswordEdit.text():
            utils.popup_warning(self, language.RESET_PASSWORD_POPUP_TITLE, language.CONSISTENT_PASSWORD)
            return

        def cb1():
            print('reset password')
            print('account:', self.AccountEdit.text())
            print('old password:', self.OldPasswordEdit.text())
            print('new password:', self.NewPasswordEdit.text())
            self.close()

        utils.popup_confirm(self, language.RESET_PASSWORD_POPUP_TITLE, language.RESET_PASSWORD_POPUP_CONTENT, cb1)

    def on_clicked_return(self):
        self.close()


class TopUpWidget(QDialog, Ui_TopUp):
    def __init__(self, parent=None):
        super(TopUpWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(utils.HEAD_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)
        self.Top6Button.clicked.connect(self.on_clicked_top_up)
        self.Top25Button.clicked.connect(self.on_clicked_top_up)
        self.Top50Button.clicked.connect(self.on_clicked_top_up)
        self.Top98Button.clicked.connect(self.on_clicked_top_up)
        self.Top328Button.clicked.connect(self.on_clicked_top_up)
        self.Top648Button.clicked.connect(self.on_clicked_top_up)

        self.top_up_button_dict = {
            self.Top6Button  : 6,
            self.Top25Button : 25,
            self.Top50Button : 50,
            self.Top98Button : 98,
            self.Top328Button: 328,
            self.Top648Button: 648,
        }

    def on_clicked_top_up(self):
        top_up_value = 0
        for button, value in self.top_up_button_dict.items():
            if button.isChecked():
                top_up_value = value
                break

        self.Tipslabel.setText(language.TOP_UP_TIPS.format(top_up_value, top_up_value*500))

    def on_clicked_confirm(self):
        if not self.AccountEdit.text():
            utils.popup_warning(self, language.TOP_UP_POPUP_TITLE, language.EMPTY_ACCOUNT)
            return

        top_up_value = 0
        for button, value in self.top_up_button_dict.items():
            if button.isChecked():
                top_up_value = value
                break

        if top_up_value == 0:
            utils.popup_warning(self, language.TOP_UP_POPUP_TITLE, language.TOP_UP_POPUP_NOT_SELECTED)
            return

        def cb1():
            # webbrowser.open(utils.MAPLE_STORY_URL, new=0)
            print('top up')
            print('account:', self.AccountEdit.text())
            print('top up:', top_up_value)
            self.close()

        utils.popup_confirm(self, language.TOP_UP_POPUP_TITLE,
                            language.TOP_UP_POPUP_CONTENT.format(self.AccountEdit.text(), top_up_value), cb1)

    def on_clicked_return(self):
        self.close()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(utils.HEAD_ICON_PATH))
        self.setWindowTitle(_translate("MainWindow", "{} -V{}".format(language.WINDOW_TITLE, utils.VERSION)))
        self.RefreshServerButton.setIcon(QIcon(utils.REFRESH_ICON_PATH))
        self.RefreshServerButton.setIconSize(self.RefreshServerButton.size())
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.ServerList.setColumnCount(2)
        self.ServerList.setColumnWidth(0, 200)
        self.ServerList.setColumnWidth(1, 30)
        self.ServerList.setHeaderLabels([language.SERVER_ITEM, language.SERVER_SITUATION])
        self.ServerList.itemClicked.connect(self.on_clicked_server_item)

        self.LoginButton.clicked.connect(self.on_clicked_login)
        self.ResetButton.clicked.connect(self.on_clicked_reset)
        self.RegisterButton.clicked.connect(self.on_clicked_register)
        self.TopUpButton.clicked.connect(self.on_clicked_top_up)
        self.RefreshServerButton.clicked.connect(self.on_clicked_refresh)
        self.ReceptionButton.clicked.connect(self.on_clicked_reception)
        self.ShortCutButton.clicked.connect(self.on_clicked_short_cut)

        self.current_selected_ip = None
        self.current_selected_item = None

        self.get_info()
        self.on_clicked_refresh()

        #not develop
        self.ReceptionButton.setVisible(False)
        self.ShortCutButton.setVisible(False)
        self.InfoBrowser.setVisible(False)

    def add_server_item(self, name, situation, ip):
        ft1 = QFont()
        ft1.setPointSize(12)

        server_item = QTreeWidgetItem(self.ServerList)
        server_item.setCheckState(0, Qt.Unchecked)
        server_item.setFont(0, ft1)
        server_item.setText(0, name)
        server_item.setToolTip(0, ip)
        server_item.setData(0, 1, ip)

        if situation == utils.SERVER_NORMAL:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, GREEN_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_NORMAL)
            server_item.setData(1, 1, True)
        elif situation == utils.SERVER_BUSY:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, YELLOW_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_BUSY)
            server_item.setData(1, 1, True)
        elif situation == utils.SERVER_STOP:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, RED_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_STOP)
            server_item.setData(1, 1, False)

    def get_info(self):
        self.InfoBrowser.setAcceptRichText(True)
        self.InfoBrowser.setText(language.WELCOME_CONTENT)

    def start_maple_story(self):
        import os
        import subprocess
        if not os.path.exists(utils.EXECUTION):
            utils.popup_critical(self, language.OPEN_GAME_TITLE, language.OPEN_GAME_ERROR_CONTENT)
        else:
            command = utils.EXECUTION + ' ' + self.current_selected_ip
            subprocess.Popen(command, shell=True)
            print('start maple story')
            print(command)

    def on_clicked_server_item(self, item, column):
        print('server IP:', item.data(0, 1),'connectable:', item.data(1, 1))
        if self.current_selected_item and self.current_selected_item is not item:
            self.current_selected_item.setCheckState(0, Qt.Unchecked)
        self.current_selected_item = item
        self.current_selected_item.setCheckState(0, Qt.Checked)
        if item.data(1, 1):
            self.current_selected_ip = item.data(0, 1)
        else:
            self.current_selected_ip = ''

    def on_clicked_refresh(self):
        print('get server list')
        self.current_selected_ip = None
        self.ServerList.clear()

        self.add_server_item('超神服务器', utils.SERVER_NORMAL, TEST_IP)
        self.add_server_item('超神服务器', utils.SERVER_BUSY, TEST_IP)
        self.add_server_item('超神服务器', utils.SERVER_STOP, TEST_IP)

    def on_clicked_login(self):
        if self.current_selected_ip == '':
            utils.popup_critical(self, language.SERVER_ITEM, language.CANT_ENTER_SERVER)
        elif self.current_selected_ip is None:
            utils.popup_critical(self, language.SERVER_ITEM, language.SELECT_SERVER)
        else:
            print('login in server', self.current_selected_ip)
            self.start_maple_story()

    def on_clicked_reset(self):
        widget = ResetPasswordWidget()
        widget.exec()

    def on_clicked_register(self):
        widget = NewAccountWidget()
        widget.exec()

    def on_clicked_top_up(self):
        widget = TopUpWidget()
        widget.exec()

    def on_clicked_reception(self):
        print('reception')

    def on_clicked_short_cut(self):
        print('short cut')




from PyQt5.QtCore import Qt, QFileInfo, QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QDialog, QTreeWidgetItem

from Script import Utils, Language
from UI.MainWindow import Ui_MainWindow
from UI.NewAccount import Ui_NewAccountWidget
from UI.ResetPassword import Ui_ResetPasswordWidget

TEST_IP = '47.241.186.78 9595'

default_color = QColor()

class NewAccountWidget(QDialog, Ui_NewAccountWidget):
    def __init__(self, parent=None):
        super(NewAccountWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(Utils.HEAD_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(Utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        if not self.AccountEdit.text():
            Utils.popup_warning(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.EMPTY_ACCOUNT)
            return

        if not self.NewPasswordEdit.text():
            Utils.popup_warning(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.EMPTY_PASSWORD)
            return

        def cb1():
            def cb2():
                print('new account')
                print('account:', self.AccountEdit.text())
                print('password:', self.NewPasswordEdit.text())
                self.close()
            Utils.popup_infomation(self, Language.NEW_ACCOUNT_POPUP_TITLE, Language.NEW_ACCOUNT_POPUP_SUCCEED, cb2)

        Utils.popup_confirm(self, Language.NEW_ACCOUNT_POPUP_TITLE, Language.NEW_ACCOUNT_POPUP_CONTENT, cb1)

    def on_clicked_return(self):
        self.close()



class ResetPasswordWindow(QDialog, Ui_ResetPasswordWidget):
    def __init__(self, parent=None):
        super(ResetPasswordWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(Utils.HEAD_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(Utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.ConfirmButton.clicked.connect(self.on_clicked_confirm)
        self.ReturnButton.clicked.connect(self.on_clicked_return)

    def on_clicked_confirm(self):
        if not self.AccountEdit.text():
            Utils.popup_warning(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.EMPTY_ACCOUNT)
            return

        if not self.OldPasswordEdit.text() or not self.NewPasswordEdit.text():
            Utils.popup_warning(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.EMPTY_PASSWORD)
            return

        if self.OldPasswordEdit.text() == self.NewPasswordEdit.text():
            Utils.popup_warning(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.CONSISTENT_PASSWORD)
            return

        def cb1():
            print('reset password')
            print('account:', self.AccountEdit.text())
            print('old password:', self.OldPasswordEdit.text())
            print('new password:', self.NewPasswordEdit.text())
            self.close()

        Utils.popup_confirm(self, Language.RESET_PASSWORD_POPUP_TITLE, Language.RESET_PASSWORD_POPUP_CONTENT, cb1)

    def on_clicked_return(self):
        self.close()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(Utils.HEAD_ICON_PATH))
        self.RefreshServerButton.setIcon(QIcon(Utils.REFRESH_ICON_PATH))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(Utils.BACKGROUND_ICON_PATH)))
        self.setPalette(palette)

        self.Information.setVisible(False)

        self.ServerList.setColumnCount(2)
        self.ServerList.setColumnWidth(0, 200)
        self.ServerList.setColumnWidth(1, 30)
        self.ServerList.setHeaderLabels([Language.SERVER_ITEM, Language.SERVER_SITUATION])
        self.ServerList.itemClicked.connect(self.on_clicked_server_item)

        self.LoginButton.clicked.connect(self.on_clicked_login)
        self.ResetButton.clicked.connect(self.on_clicked_reset)
        self.RegisterButton.clicked.connect(self.on_clicked_register)
        self.RefreshServerButton.clicked.connect(self.on_clicked_refresh)

        self.current_selected_ip = None

        self.on_clicked_refresh()

        # self.ServerList
    def on_clicked_server_item(self, item, column):
        print('server IP:', item.data(0, 1),'situation:', item.data(1, 1))
        if item.data(1, 1):
            self.current_selected_ip = item.data(0, 1)

    def on_clicked_refresh(self):
        self.current_selected_ip = None
        self.ServerList.clear()

        def add_server_item(name, situation, ip, allow_connected):
            ft1 = QFont()
            ft1.setPointSize(12)

            server_item = QTreeWidgetItem(self.ServerList)
            server_item.setFont(0, ft1)
            server_item.setFont(1, ft1)
            server_item.setText(0, name)
            server_item.setText(1, situation)
            server_item.setToolTip(0, ip)
            server_item.setData(0, 1, ip)
            server_item.setData(1, 1, allow_connected)

        add_server_item('超神服务器', Language.SERVER_SITUATION_BUSY, TEST_IP, True)

    def on_clicked_login(self):
        if self.current_selected_ip:
            print ('login in server', self.current_selected_ip)
        elif self.current_selected_ip == '':
            Utils.popup_critical(self, Language.SERVER_ITEM, Language.CANT_ENTER_SERVER)
        elif self.current_selected_ip is None:
            Utils.popup_critical(self, Language.SERVER_ITEM, Language.SELECT_SERVER)

    def on_clicked_reset(self):
        widget = ResetPasswordWindow()
        widget.exec()

    def on_clicked_register(self):
        widget = NewAccountWidget()
        widget.exec()

    def start_maple_story(self):
        print('start maple story')




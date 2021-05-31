# -*- coding: utf-8 -*-
import json
import webbrowser

import requests
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, QUrl, QTimer, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QBrush, QColor, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog, QTreeWidgetItem, QLineEdit

from script import utils, language, protocol
from ui.MainWindow import Ui_MainWindow
from ui.NewAccount import Ui_NewAccountWidget
from ui.ResetPassword import Ui_ResetPasswordWidget
from ui.TopUp import Ui_TopUp

_translate = QtCore.QCoreApplication.translate

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

        # 限制只能输入数字和子母
        reg = QRegExp('[a-zA-z0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.AccountEdit.setValidator(validator)
        self.NewPasswordEdit.setValidator(validator)

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
            print('new account')
            print('account:', self.AccountEdit.text())
            print('password:', self.NewPasswordEdit.text())

            ret_dict = protocol.create_account_request(self.AccountEdit.text(), self.NewPasswordEdit.text())
            print('response: ', ret_dict)

            if ret_dict['code'] == -1:
                utils.popup_critical(self, language.NEW_ACCOUNT_POPUP_TITLE, ret_dict['data'])
            else:
                def cb2():
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

        # 限制只能输入数字和子母
        reg = QRegExp('[a-zA-z0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.AccountEdit.setValidator(validator)
        self.NewPasswordEdit.setValidator(validator)
        self.OldPasswordEdit.setValidator(validator)

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

            ret_dict = protocol.update_account_request(self.AccountEdit.text(), self.NewPasswordEdit.text(), self.OldPasswordEdit.text())
            print('response: ', ret_dict)

            if ret_dict['code'] == -1:
                utils.popup_critical(self, language.RESET_PASSWORD_POPUP_TITLE, ret_dict['data'])
            else:
                def cb2():
                    self.close()
                utils.popup_infomation(self, language.RESET_PASSWORD_POPUP_TITLE, language.RESET_PASSWORD_POPUP_SUCCEED, cb2)

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

        self.timer = QTimer()
        self.current_selected_ip_port = None
        self.current_selected_item = None

        self.get_info()
        self.on_clicked_refresh()

        #not develop
        self.ReceptionButton.setVisible(False)
        self.ShortCutButton.setVisible(False)
        self.TopUpButton.setVisible(False)

    def add_server_item(self, name, situation, ip_port):
        print('server name:{}, situation:{}, ip_port:{}'.format(name, int(situation), ip_port))
        ft1 = QFont()
        ft1.setPointSize(10)

        server_item = QTreeWidgetItem(self.ServerList)
        server_item.setCheckState(0, Qt.Unchecked)
        server_item.setFont(0, ft1)
        server_item.setText(0, name)
        server_item.setToolTip(0, ip_port)
        server_item.setData(0, 1, ip_port)

        if situation == utils.SERVER_NORMAL:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, GREEN_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_CONTENT.get(situation))
            server_item.setData(1, 1, True)
        elif situation == utils.SERVER_BUSY:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, YELLOW_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_CONTENT.get(situation))
            server_item.setData(1, 1, True)
        elif situation == utils.SERVER_STOP:
            server_item.setFont(1, ft1)
            server_item.setForeground(1, RED_COLOR)
            server_item.setText(1, language.SERVER_SITUATION_CONTENT.get(situation))
            server_item.setData(1, 1, False)

    def get_info(self):
        self.InfoBrowser.setAcceptRichText(True)
        ret_text = protocol.server_notice_request()
        print('notice:', ret_text)
        self.InfoBrowser.setText(ret_text)

    def start_maple_story(self):
        import os
        import subprocess
        if not os.path.exists(utils.EXECUTION):
            utils.popup_critical(self, language.OPEN_GAME_TITLE, language.OPEN_GAME_ERROR_CONTENT)
        else:
            command = utils.EXECUTION + ' ' + self.current_selected_ip_port
            subprocess.Popen(command, shell=True)
            print('start maple story')
            print(command)

            self.LoginButton.setEnabled(False)
            self.LoginButton.setText(language.STARTING_GAME)
            self.timer.timeout.connect(self.timer_update)
            self.timer.start(10000)

    def timer_update(self):
        self.LoginButton.setText(language.START_GAME)
        self.LoginButton.setEnabled(True)
        self.timer.stop()

    def on_clicked_server_item(self, item, column):
        print('server IP_Port:', item.data(0, 1),'connectable:', item.data(1, 1))
        if self.current_selected_item and self.current_selected_item is not item:
            self.current_selected_item.setCheckState(0, Qt.Unchecked)
        self.current_selected_item = item
        self.current_selected_item.setCheckState(0, Qt.Checked)
        if item.data(1, 1):
            self.current_selected_ip_port = item.data(0, 1)
        else:
            self.current_selected_ip_port = ''

    def on_clicked_refresh(self):
        print('get server list')

        self.current_selected_ip_port = None
        self.current_selected_item = None
        self.ServerList.clear()

        ret_text = protocol.server_list_request()
        print('response: ', ret_text)

        content_list = utils.parse_cfg_str_to_list_of_list(ret_text)
        for ip, port, server_name, situation in content_list:
            ip_port = ip + ' ' + port
            self.add_server_item(server_name, int(situation), ip_port)

    def on_clicked_login(self):
        if self.current_selected_ip_port == '':
            utils.popup_critical(self, language.SERVER_ITEM, language.CANT_ENTER_SERVER)
        elif self.current_selected_ip_port is None:
            utils.popup_critical(self, language.SERVER_ITEM, language.SELECT_SERVER)
        else:
            print('login in server', self.current_selected_ip_port)
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




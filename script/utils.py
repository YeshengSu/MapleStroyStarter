from PyQt5.QtWidgets import QMessageBox

EXECUTION = 'MapleStory.exe'

HEAD_ICON_PATH = 'res/MapleStory.ico'
REFRESH_ICON_PATH = 'res/Refresh.png'
BACKGROUND_ICON_PATH = 'res/BackGround.jpg'
MAPLE_STORY_URL = 'http://www.baidu.com'

SERVER_NORMAL = 1
SERVER_BUSY = 2
SERVER_STOP = 3

def popup_warning(widget, title, content, callback=None):
	choice = QMessageBox.warning(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_critical(widget, title, content, callback=None):
	choice = QMessageBox.critical(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_infomation(widget, title, content, callback=None):
	choice = QMessageBox.information(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_confirm(widget, title, content, callback=None):
	choice = QMessageBox.question(widget, title, content, QMessageBox.Yes | QMessageBox.Cancel)

	if choice == QMessageBox.Yes:
		if callback:
			callback()

from PyQt5.QtWidgets import QMessageBox

EXECUTION = 'MapleStory.exe'

HEAD_ICON_PATH = 'Res/MapleStory.ico'
REFRESH_ICON_PATH = 'Res/Refresh.png'
BACKGROUND_ICON_PATH = 'Res/BackGround.jpg'
MAPLE_STORY_URL = 'http://www.baidu.com'

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

from PyQt5.QtWidgets import QMessageBox

def popup_warning(widget, title, content, callback=None):
	choice = QMessageBox.warning(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback():
			callback()

def popup_critical(widget, title, content, callback=None):
	choice = QMessageBox.critical(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback():
			callback()


def popup_confirm(widget, title, content, callback=None):
	choice = QMessageBox.question(widget, title, content, QMessageBox.Yes|QMessageBox.Cancel)

	if choice == QMessageBox.Yes:
		if callback():
			callback()
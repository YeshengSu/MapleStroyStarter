# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from script.main import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
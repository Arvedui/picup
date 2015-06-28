# -*- coding:utf8 -*-
"""
main module does some logging and qt setup and hands over to MainWindow
"""

from picup.globals import __version__

import sys


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

from picup.main_window import MainWindow

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)


def main():
    """
    app main function
    """
    app = QApplication(sys.argv)
    app.setOrganizationName('Arvedui')
    app.setApplicationName('picup')
    QSettings.setDefaultFormat(QSettings.IniFormat)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

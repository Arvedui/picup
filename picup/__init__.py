# -*- coding:utf8 -*-
######################## BEGIN LICENSE BLOCK ########################
# picup - small gui tool for uploading pictures to picflash
# Copyright (C) 2014  Arvedui
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA
######################### END LICENSE BLOCK #########################

from picup.globals import __version__

import sys

PYQT_VERSION = None

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
PYQT_VERSION = 5

from picup.main_window import MainWindow

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

logger.propagete = False
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('using PyQt version %i', PYQT_VERSION)

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName('Arvedui')
    app.setApplicationName('picup')
    QSettings.setDefaultFormat(QSettings.IniFormat)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

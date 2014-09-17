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

__version__ = '0.1.3'

import sys

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QSettings
except ImportError:
    # setting PyQt apiversion to 2, where possible
    import sip
    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QString', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
    sip.setapi('QVariant', 2)


    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QSettings

from picup.main_window import MainWindow

import logging
logger = logging.getLogger('picup')
logger.setLevel(logging.DEBUG)

logger.propagete = False
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName('Arvedui')
    app.setApplicationName('picup')
    QSettings.setDefaultFormat(QSettings.IniFormat)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

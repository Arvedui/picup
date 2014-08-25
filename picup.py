#!/usr/bin/env python3
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

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

from picup import MainWindow

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName('Arvedui')
    app.setApplicationName('picup')
    QSettings.setDefaultFormat(QSettings.IniFormat)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

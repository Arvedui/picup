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
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QFileDialog

from picup.functions import load_ui
from picup.functions import get_api_key
#import picup.model.key_request

from picup.globals import SUPPORTED_FILE_TYPES

import logging


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_ui('MainWindow.ui', self)
        self.apikey = get_api_key(self)

        self.files = []

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_add_picture.clicked.connect(self.add_file)
        print()


    def add_file(self,):
        dialog = QFileDialog(parent=self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilters(SUPPORTED_FILE_TYPES)

        if dialog.exec_():
            self.files.extend(dialog.selectedFiles())


class FileListModel():
    pass

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
from PyQt5.QtWidgets import (QMainWindow, QInputDialog, QFileDialog,
                             QProgressDialog)
from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QThread

from picup.functions import load_ui
from picup.functions import get_api_key
from picup.upload import Upload
from picup.globals import SUPPORTED_FILE_TYPES
from picup.dialogs import ShowLinks

import logging


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_ui('MainWindow.ui', self)
        apikey = get_api_key(self)
        self.upload_thread = QThread()
        self.upload = Upload(apikey=apikey)
        self.upload.moveToThread(self.upload_thread)
        self.upload_thread.start()


        self.listView_files.setModel(FileListModel())

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_add_picture.clicked.connect(self.add_file)
        self.pushButton_upload.clicked.connect(self.start_upload)

        self.upload.picture_uploaded.connect(self.update_status_dialog)

        self.dialog = QFileDialog(parent=self)
        self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.setNameFilters(SUPPORTED_FILE_TYPES)



    def add_file(self):

        if self.dialog.exec_():
            files = self.dialog.selectedFiles()
            model = self.listView_files.model()
            model.add_files(files)

    def start_upload(self,):
        model = self.listView_files.model()
        link_dialog = ShowLinks(self.upload, len(model.files), parent=self)
        link_dialog.show()

        self.upload.upload_pictures.emit(model.files)



class FileListModel(QAbstractListModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.files = []

    def rowCount(self, parent):
        return len(self.files)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.files[index.row()]


    def add_files(self, files):
        prev_len = len(self.files)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + len(files))
        self.files.extend(files)
        self.endInsertRows()

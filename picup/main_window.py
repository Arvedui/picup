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
try:
    from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
    from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QThread
except ImportError:
    from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox
    from PyQt4.QtCore import QAbstractListModel, Qt, QModelIndex, QThread

from picup.functions import load_ui
from picup.functions import get_api_key
from picup.upload import Upload
from picup.globals import SUPPORTED_FILE_TYPES
from picup.dialogs.show_links import ShowLinks

import logging


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        load_ui('MainWindow.ui', self)

        apikey = get_api_key(self)
        self.upload_in_progress = False
        self.upload_thread = QThread()
        self.upload = Upload(apikey=apikey)
        self.upload.moveToThread(self.upload_thread.thread())
        self.upload_thread.start()

        self.listView_files_model = FileListModel()
        self.listView_files.setModel(self.listView_files_model)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_add_picture.clicked.connect(self.add_file)
        self.pushButton_upload.clicked.connect(self.start_upload)

        self.upload.upload_finished.connect(self.upload_finished)

        self.dialog = QFileDialog(parent=self)
        self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.setNameFilters(SUPPORTED_FILE_TYPES)



    def add_file(self):

        if self.dialog.exec_():
            files = self.dialog.selectedFiles()
            self.listView_files_model.add_files(files)

    def start_upload(self,):
        if (len(self.listView_files_model.files)
            and not self.upload_in_progress):
            self.upload_in_progress = True
            link_dialog = ShowLinks(self.upload,
                                    len(self.listView_files_model.files),
                                    parent=self)
            link_dialog.show()

            self.upload.upload_pictures.emit(self.listView_files_model.files)
            self.clear_list()
        elif self.upload_in_progress:
            logging.debug('Upload already in progress.')
            QMessageBox.warning(self, 'Upload Läuft', 'Es läuft beraits ein Upload Prozess.')

        else:
            logging.debug('There is nothing to upload.')
            QMessageBox.information(self, 'Nüx da', 'Es würden keine bilder zum hochladen hinzugefügt')

    def clear_list(self):
        self.listView_files_model.clear_list()

    def upload_finished(self):
        self.upload_in_progress = False


class FileListModel(QAbstractListModel):
    def __init__(self, **kwargs):
        super(FileListModel, self).__init__(**kwargs)

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

    def clear_list(self,):
        self.beginRemoveRows(QModelIndex(), 0, len(self.files)-1)
        del self.files[:] # for python2 compatibility
        self.endRemoveRows()

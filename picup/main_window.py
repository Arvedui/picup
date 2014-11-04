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
from __future__ import unicode_literals

try:
    from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox,
                                 QMessageBox)
    from PyQt5.QtCore import (QAbstractListModel, Qt, QModelIndex, QThread,
                              pyqtSlot, pyqtSignal)
except ImportError:
    from PyQt4.QtGui import (QMainWindow, QFileDialog, QMessageBox, QMessageBox,
                             QInputDialog)
    from PyQt4.QtCore import (QAbstractListModel, Qt, QModelIndex, QThread,
                              pyqtSlot, pyqtSignal)

from picuplib.globals import ALLOWED_RESIZE, ALLOWED_ROTATION

from picup.functions import load_ui
from picup.functions import get_api_key, set_api_key
from picup.upload import Upload
from picup.globals import SUPPORTED_FILE_TYPES, __version__, DEFAULT_API_KEY
from picup.dialogs import ShowLinks, UrlInput, KeyRequest

import logging
logger = logging.getLogger(__name__)

try:
    from urllib.parse import urlparse, urlunparse
except:
    from urlparse import urlparse, urlunparse


class MainWindow(QMainWindow):

    upload_pictures = pyqtSignal(list)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        load_ui('MainWindow.ui', self)
        self.setWindowTitle('Picup - {}'.format(__version__))

        apikey = get_api_key()
        if not apikey:
            apikey = self.request_api_key()

        self.upload_in_progress = False
        self.upload_thread = QThread()
        self.upload = Upload(apikey=apikey)
        self.upload_thread.start()
        self.upload.moveToThread(self.upload_thread)


        self.listView_files_model = FileListModel()
        self.listView_files.setModel(self.listView_files_model)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_add_picture.clicked.connect(self.add_file)
        self.pushButton_add_links.clicked.connect(self.add_url)
        self.pushButton_upload.clicked.connect(self.start_upload)
        self.pushButton_clear_list.clicked.connect(
            self.listView_files_model.clear_list)
        self.pushButton_remove_selected.clicked.connect(self.remove_selected)

        self.upload.upload_finished.connect(self.upload_finished)
        self.upload.upload_error.connect(self.handle_error)

        self.upload_pictures.connect(self.upload.upload_multiple)

        self.dialog = QFileDialog(parent=self)
        self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.setNameFilters(SUPPORTED_FILE_TYPES)

        self.comboBox_resize_options.activated['QString'].connect(
                    self.upload.change_default_resize)
        self.comboBox_rotate_options.activated['QString'].connect(
                    self.upload.change_default_rotation)
        self.checkBox_delete_exif.toggled.connect(
                    self.upload.change_default_exif)

        self.comboBox_resize_options.addItem('')
        for item in ALLOWED_RESIZE:
            if item == 'og':
                continue
            self.comboBox_resize_options.addItem(item)

        self.comboBox_rotate_options.addItems(ALLOWED_ROTATION)

    def __del__(self):
        logger.debug('begin cleanup threads')
        try:
            self.upload_thread.quit()
        except:
            logger.exception('Exception while cleanup')
        logger.debug('thread cleanup finished')

    def request_api_key(self,):
        window = KeyRequest(parent=self)
        if window.exec_():
            apikey = window.lineEdit_apikey.text()
            if apikey:
                set_api_key(apikey)
                return apikey
            return DEFAULT_API_KEY

        sys.exit(0)


    @pyqtSlot()
    def add_file(self):
        if self.dialog.exec_():
            files = self.dialog.selectedFiles()
            self.listView_files_model.add_files([(file_, 'file') for file_ in files])

    @pyqtSlot()
    def add_url(self,):
        url_input = UrlInput()
        code = url_input.exec_()
        urls = url_input.text()

        new_entrys = []
        not_added = []

        if code and urls != '':
            for url in urls.split('\n'):
                parsed_url = urlparse(url, scheme='http')
                scheme = parsed_url.scheme.lower()
                if scheme in ['http', 'https', 'ftp']:
                    new_entrys.append((urlunparse(parsed_url), 'url'))

                else:
                    not_added.append(url)

            if not_added:
                message = QMessageBox(QMessageBox.Warning, 'Fehler',
                                      'Ein oder mehrere link(s) konnten nicht hinzugefügt werden.',
                                      buttons=QMessageBox.Ok,
                                      parent=self)
                message.setDetailedText('\n'.join(not_added))



            self.listView_files_model.add_files(new_entrys)

    @pyqtSlot()
    def start_upload(self,):
        if (len(self.listView_files_model.files)
                and not self.upload_in_progress):
            self.upload_in_progress = True
            files = self.listView_files_model.files[:]

            link_dialog = ShowLinks(self.upload, len(files), parent=self)
            link_dialog.show()

            logger.debug('emitting upload signal with arguments: %s', files)
            self.upload_pictures.emit(files)

            logger.debug('cleanup main window')
            self.listView_files_model.clear_list()
        elif self.upload_in_progress:
            logger.debug('Upload already in progress.')
            QMessageBox.warning(self, 'Upload Läuft', 'Es läuft bereits ein Upload Prozess.')

        else:
            logger.info('There is nothing to upload.')
            QMessageBox.information(self, 'Nüx da', 'Es wurden keine bilder zum hochladen hinzugefügt')

    @pyqtSlot()
    def upload_finished(self, ):
        self.upload_in_progress = False

    @pyqtSlot(type, tuple)
    def handle_error(self, exception_type, args):
        message = QMessageBox(QMessageBox.Warning, 'Fehler',
                              'Fehler beim upload.', buttons=QMessageBox.Ok,
                              parent=self)
        message.setDetailedText(repr(exception_type) + '\n' + repr(args))

        message.exec_()

    @pyqtSlot()
    def remove_selected(self,):
        for item in self.listView_files.selectedIndexes():
            self.listView_files_model.remove_element(item.row(), item.row())


class FileListModel(QAbstractListModel):
    def __init__(self, **kwargs):
        super(FileListModel, self).__init__(**kwargs)

        self.files = []

    def rowCount(self, parent):
        return len(self.files)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.files[index.row()][0]


    def add_files(self, files):
        prev_len = len(self.files)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + len(files))
        self.files.extend(files)
        self.endInsertRows()

    @pyqtSlot()
    def clear_list(self,):
        self.beginRemoveRows(QModelIndex(), 0, len(self.files)-1)
        del self.files[:] # for python2 compatibility
        self.endRemoveRows()

    def remove_element(self, first, last):
        self.beginRemoveRows(QModelIndex(), first, last)
        del self.files[first:last+1]
        self.endRemoveRows()

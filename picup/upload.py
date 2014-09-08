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

from picuplib import Upload as PicflashUpload
try:
    from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PyQt4.QtCore import QThread, pyqtSignal, Qt, QObject
    from PyQt4.QtGui import QApplication

import logging


class Upload(QObject):

    upload_pictures = pyqtSignal(list)
    picture_uploaded = pyqtSignal(tuple)
    upload_finished = pyqtSignal()
    upload_error = pyqtSignal(type, tuple)


    def __init__(self, apikey):
        QObject.__init__(self, parent=None,)
        self.upload = PicflashUpload(apikey=apikey)

        self.upload_pictures.connect(self.upload_multiple)

    def upload_multiple(self, files):
        instance = QApplication.instance()

        for file_ in files:
            instance.processEvents()
            try:
                links = self.upload.upload(file_)[0]
                self.picture_uploaded.emit((file_, links))
                logging.info('Uploaded %s', file_)
            except Exception as e: # yes in know its bad, but catching every possbile exception is necessary here
                self.upload_error.emit(type(e), e.args)
                return False

            instance.processEvents()

        self.upload_finished.emit()


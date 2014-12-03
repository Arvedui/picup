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


from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot


from picup.functions import load_ui


import logging
logger = logging.getLogger(__name__)


class UrlInput(QDialog):

    def __init__(self, **kwargs):
        super(UrlInput, self).__init__(**kwargs)
        load_ui('link_input.ui', self)

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

    @pyqtSlot()
    def reject(self,):
        self.done(False)

    @pyqtSlot()
    def accept(self,):
        self.done(True)

    def text(self,):
        return self.plainTextEdit.toPlainText()

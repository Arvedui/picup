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

from os import path
from requests import get
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QWidget, QApplication,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSlot, QAbstractListModel, QModelIndex
from PyQt5.QtGui import QPixmap, QClipboard

from picup.functions import load_ui, load_ui_factory
from picup.globals import BB_TEMPLTATE, LINKTYPES, LINKTYPE_ORDER

LINK_WIDGET_UI_CLASS, LINK_WIDGET_BASE_CLASS = load_ui_factory('LinkWidget.ui')

import logging
logger = logging.getLogger(__name__)


class ShowLinks(QDialog):

    def __init__(self, upload_thread, amount_links, **kwargs):
        super().__init__(**kwargs)
        load_ui('LinkDialog.ui', self)

        self.linkmodel = LinkListModel()
        self.listView_links.setModel(self.linkmodel)
        self.clipboard = QApplication.clipboard()

        self.upload_thread = upload_thread
        self.central_widget = QWidget(self)
        self.scrollArea.setWidget(self.central_widget)
        self.progressBar_upload.setMaximum(amount_links)
        self.scroll_area_layout = QVBoxLayout()
        self.central_widget.setLayout(self.scroll_area_layout)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.upload_thread.picture_uploaded.connect(self.add_entry)
        self.upload_thread.upload_finished.connect(self.upload_finished)
        self.comboBox_link_output.activated['QString'].connect(
            self.linkmodel.set_linktype)
        self.pushButton_to_clipboard.clicked.connect(self.copy_to_clipboard)
        self.pushButton_to_file.clicked.connect(self.copy_to_file)

        self.comboBox_link_output.addItems(LINKTYPE_ORDER)

    def update_progress(self):
        value = self.progressBar_upload.value()
        self.progressBar_upload.setValue(value+1)

    @pyqtSlot(list)
    def upload_finished(self, failed):
        logger.debug('recieved upload finished signal. beginn cleanup')

        self.progressBar_upload.hide()

        if failed:
            logger.info("%s upload(s) failed", len(failed))
            message = QMessageBox()
            message.setText('Eine oder mehrere Dateien konnten nicht hochgaladen werden.')
            message.setDetailedText('\n'.join(failed))
            message.exec_()

        self.upload_thread.picture_uploaded.disconnect(self.add_entry)
        self.upload_thread.upload_finished.disconnect(self.upload_finished)
        logger.debug('finished cleanup')

    @pyqtSlot(tuple)
    def add_entry(self, data):
        self.update_progress()

        links = data[2]
        links['bb_hotlink'] = BB_TEMPLTATE.format(links['sharelink'],
                                                  links['hotlink'])
        links['bb_thumbnail'] = BB_TEMPLTATE.format(links['sharelink'],
                                                    links['thumbnail'])

        self.linkmodel.add_link(data)
        widget = LinkWidget(data, parent=self.central_widget)

        self.scroll_area_layout.addWidget(widget)

    def gen_string(self,):
        selection_text = []
        selection = self.listView_links.selectedIndexes()
        if selection:
            for index in self.listView_links.selectedIndexes():
                data = self.linkmodel.data(index)
                selection_text.append(data)

        else:
            selection_text = self.linkmodel.get_all_rows()

        return "\n".join(selection_text) + '\n'

    @pyqtSlot()
    def copy_to_clipboard(self,):
        string = self.gen_string()

        self.clipboard.setText(string)

    @pyqtSlot()
    def copy_to_file(self,):
        filename = QFileDialog.getSaveFileName(self, 'test')
        if type(filename) == tuple:
            filename = filename[0]
        if filename:
            with open(filename, 'w') as file_obj:
                file_obj.write(self.gen_string())


class LinkWidget(LINK_WIDGET_BASE_CLASS, LINK_WIDGET_UI_CLASS):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        filename, type_, links = data

        pixmap = QPixmap()

        if type_ == 'url':
            logger.debug('load thumbnail from picflash')
            thumbnail = get(links['thumbnail'])
            pixmap.loadFromData(thumbnail.content)
        else:
            logger.debug('generate thumbnail from file %s', filename)
            pixmap.load(filename)

        self.pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        self.label_picture.setPixmap(self.pixmap)

        filename = path.split(filename)[1]
        if len(filename) > 50:
            filename = filename[:50] + ' … ' + filename[-4:]
        self.groupBox.setTitle(filename)

        self.lineEdit_sharelink.setText(links['sharelink'])
        self.lineEdit_hotlink.setText(links['hotlink'])
        self.lineEdit_deletelink.setText(links['delete_url'])
        self.lineEdit_preview.setText(links['thumbnail'])
        self.lineEdit_bb_preview.setText(links['bb_thumbnail'])
        self.lineEdit_bb_hotlink.setText(links['bb_hotlink'])

        self.lineEdit_sharelink.setCursorPosition(0)
        self.lineEdit_hotlink.setCursorPosition(0)
        self.lineEdit_deletelink.setCursorPosition(0)
        self.lineEdit_preview.setCursorPosition(0)
        self.lineEdit_bb_hotlink.setCursorPosition(0)
        self.lineEdit_bb_preview.setCursorPosition(0)


class LinkListModel(QAbstractListModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.links = []
        self.linktype = "sharelink"

    def rowCount(self, parent):
        return len(self.links)

    def data(self, index, role=None):
        if role == Qt.DisplayRole or not role:
            return self.links[index.row()][2][self.linktype]

    def get_all_rows(self,):
        return [item[2][self.linktype] for item in self.links]

    def add_link(self, data):
        prev_len = len(self.links)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + 1)
        self.links.append(data)
        self.endInsertRows()

    @pyqtSlot(str)
    def set_linktype(self, linktype):
        self.beginResetModel()
        self.linktype = LINKTYPES[linktype]
        self.endResetModel()

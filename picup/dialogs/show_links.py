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

from os import path
from PyQt5.QtWidgets import QDialog, QAbstractItemDelegate, QListView, QVBoxLayout, QWidget
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QPixmap

from picup.functions import load_ui, load_ui_factory

LINK_WIDGET_UI_CLASS, LINK_WIDGET_BASE_CLASS = load_ui_factory('LinkWidget.ui')

class ShowLinks(QDialog):

    def __init__(self, upload_thread, amount_links, **kwargs):
        super().__init__(**kwargs)
        load_ui('LinkDialog.ui', self)

        self.entrys = []
        self.upload_thread = upload_thread
        self.central_widget = QWidget(self)
        self.scrollArea.setWidget(self.central_widget)
        self.progressBar_upload.setMaximum(amount_links)
        self.scroll_area_layout = QVBoxLayout()
        self.central_widget.setLayout(self.scroll_area_layout)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.upload_thread.picture_uploaded.connect(self.update_progress)
        self.upload_thread.picture_uploaded.connect(self.add_entry)
        self.upload_thread.upload_finished.connect(self.upload_finished)

    def update_progress(self):
        value = self.progressBar_upload.value()
        self.progressBar_upload.setValue(value+1)

    def upload_finished(self):
        self.progressBar_upload.hide()

        self.upload_thread.picture_uploaded.disconnect(self.update_progress)
        self.upload_thread.upload_finished.disconnect(self.upload_finished)

    def add_entry(self, data):
        self.entrys.append(data)
        widget = LinkWidget(data, parent=self.central_widget)

        self.scroll_area_layout.addWidget(widget)

class LinkWidget(LINK_WIDGET_BASE_CLASS, LINK_WIDGET_UI_CLASS):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        filename, links = data

        self.groupBox.setTitle(path.split(filename)[1])

        pixmap = QPixmap()
        pixmap.load(filename)
        self.pixmap = pixmap.scaled(139, 139, Qt.KeepAspectRatio)
        self.label_picture.setPixmap(self.pixmap)

        self.lineEdit_sharelink.setText(links['sharelink'])
        self.lineEdit_hotlink.setText(links['hotlink'])
        self.lineEdit_deletelink.setText(links['delete_url'])
        self.lineEdit_preview.setText(links['thumbnail'])

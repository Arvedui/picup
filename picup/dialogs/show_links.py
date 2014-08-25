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

from PyQt5.QtWidgets import QDialog, QAbstractItemDelegate, QListView
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QPixmap

from picup.functions import load_ui, load_ui_factory


class ShowLinks(QDialog):

    def __init__(self, upload_thread, amount_links, **kwargs):
        super().__init__(**kwargs)
        load_ui('LinkDialog.ui', self)

        self.upload_thread = upload_thread
        self.progressBar_upload.setMaximum(amount_links)

        self.upload_thread.picture_uploaded.connect(self.update_progress)
        self.upload_thread.upload_finished.connect(self.upload_finished)

        self.listView_links.setModel(LinkDisplayModel(self.upload_thread))
        self.listView_links.setItemDelegate(LinkDisplayDelegate())
        self.listView_links.setVerticalScrollMode(QListView.ScrollPerPixel)

    def update_progress(self):
        value = self.progressBar_upload.value()
        self.progressBar_upload.setValue(value+1)

    def upload_finished(self):
        self.progressBar_upload.hide()

        self.upload_thread.picture_uploaded.disconnect(self.update_progress)
        self.upload_thread.upload_finished.disconnect(self.upload_finished)


class LinkDisplayModel(QAbstractListModel):

    def __init__(self, upload_thread, **kwargs):
        super().__init__(**kwargs)
        self.upload_thread = upload_thread
        self.file_links = []

        self.upload_thread.picture_uploaded.connect(self.add_entry)
        self.upload_thread.upload_finished.connect(self.upload_finished)

    def upload_finished(self,):
        self.upload_thread.picture_uploaded.disconnect(self.add_entry)
        self.upload_thread.upload_finished.disconnect(self.upload_finished)

    def add_entry(self, entry):
        prev_len = len(self.file_links)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + 1)
        self.file_links.append(entry)
        self.endInsertRows()

    def rowCount(self, parent):
        return len(self.file_links)

    def data(self, index, role):

        if role == Qt.DisplayRole:
            return self.file_links[index.row()]


class LinkDisplayDelegate(QAbstractItemDelegate):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ui_factory, self.widget_base_class = load_ui_factory('LinkWidget.ui')
        self.ui_factory = ui_factory()

        self.size = self.get_widget().size()

    def get_widget(self,):
        widget = self.widget_base_class()
        self.ui_factory.setupUi(widget)

        return widget

    def sizeHint(self, item, index):
        return self.size

    def paint(self, painter, option, index):
        widget = self.get_widget()
        file_name, links = index.data()
        pixmap = QPixmap()
        pixmap.load(file_name)

        #widget.label_picture.setPixmap(pixmap)
        #widget.lineEdit_sharelink.setText(links[0]['sharelink'])

        widget.render(painter)

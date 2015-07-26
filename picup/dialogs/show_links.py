# -*- coding:utf8 -*-
"""
Module for everything related to showing the links and the upload status.
"""

from __future__ import unicode_literals

from os import path
from requests import get
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QWidget, QApplication,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QAbstractListModel,
                          QModelIndex)
from PyQt5.QtGui import QPixmap

from picup.functions import load_ui, load_ui_factory
from picup.globals import BB_TEMPLTATE, LINKTYPES, LINKTYPE_ORDER
import logging

LINK_WIDGET_UI_CLASS, LINK_WIDGET_BASE_CLASS = load_ui_factory('LinkWidget.ui')


LOGGER = logging.getLogger(__name__)


class ShowLinks(QDialog):
    """
    Dialog which contains the upload status and the links returned by the api
    """

    readd_pictures = pyqtSignal(list)

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
        """
        updates the upload progess widget
        """
        value = self.progressBar_upload.value()
        self.progressBar_upload.setValue(value+1)

    @pyqtSlot(list)
    def upload_finished(self, failed):
        """
        cleans up stuff after the upload finished
        """
        LOGGER.debug('recieved upload finished signal. beginn cleanup')

        self.progressBar_upload.hide()

        if failed:
            LOGGER.info("%s upload(s) failed", len(failed))
            text = ('Eine oder mehrere Dateien '
                    'konnten nicht hochgeladen werden.\n'
                    'Bilder in der Liste behalten?')
            message = QMessageBox(QMessageBox.Warning, "Fehler beim upload",
                                  text, parent=self,
                                  buttons=QMessageBox.Yes | QMessageBox.No)
            url_list = [x[0] for x in failed]
            message.setDetailedText('\n'.join(url_list))
            if message.exec_() == QMessageBox.Yes:
                LOGGER.debug('readding %s link(s)', len(failed))
                self.readd_pictures.emit(failed)

        self.upload_thread.picture_uploaded.disconnect(self.add_entry)
        self.upload_thread.upload_finished.disconnect(self.upload_finished)
        LOGGER.debug('finished cleanup')

    @pyqtSlot(tuple)
    def add_entry(self, data):
        """
        adds an entry for an uploded picture.
        """
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
        """
        generets a string containing all links seperated by newlines.
        """
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
        """
        generates a string using gen_string()
        and writes it to the clipboard
        """
        string = self.gen_string()

        self.clipboard.setText(string)

    @pyqtSlot()
    def copy_to_file(self,):
        """
        generetes a string using gen_string()
        and writes it to a file named by the user.
        """
        filename = QFileDialog.getSaveFileName(self, 'test')
        if isinstance(filename, tuple):
            filename = filename[0]
        if filename:
            with open(filename, 'w') as file_obj:
                file_obj.write(self.gen_string())


# pylint: disable=no-member,too-few-public-methods
# gets many of its members at runtime through the "magic" base classes
class LinkWidget(LINK_WIDGET_BASE_CLASS, LINK_WIDGET_UI_CLASS):
    """
    widget for upload pictures, one for each picture.
    contains some links as well as a thumbnail
    """

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        filename, type_, links = data

        pixmap = QPixmap()


        LOGGER.debug('load thumbnail from picflash')
        thumbnail = get(links['thumbnail'])
        pixmap.loadFromData(thumbnail.content)

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
    """
    model for the links of uploaded pictures
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.links = []
        self.linktype = "sharelink"


    # pylint: disable=invalid-name,unused-argument
    # this name is neccacary for a working ListModel implementation
    # same counts for the argument
    def rowCount(self, parent):
        """
        returns the amount of rows
        Required for a ListModel implementation.
        """
        return len(self.links)

    def data(self, index, role=None):
        """
        returns requestet data.
        Required for a ListModel implementation.
        """
        if role == Qt.DisplayRole or not role:
            return self.links[index.row()][2][self.linktype]

    def get_all_rows(self,):
        """
        returns a list containing all rows.
        """
        return [item[2][self.linktype] for item in self.links]

    def add_link(self, data):
        """
        adds a link to the model
        """
        prev_len = len(self.links)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + 1)
        self.links.append(data)
        self.endInsertRows()

    @pyqtSlot(str)
    def set_linktype(self, linktype):
        """
        sets a diferent linktype to be displayed
        """
        self.beginResetModel()
        self.linktype = LINKTYPES[linktype]
        self.endResetModel()

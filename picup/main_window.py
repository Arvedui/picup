# -*- coding:utf8 -*-
"""
Handels everthing related to the main Window
"""

from __future__ import unicode_literals

import sys

from urllib.parse import urlparse, urlunparse
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QMessageBox
from PyQt5.QtCore import (QAbstractListModel, Qt, QModelIndex, QThread,
                          pyqtSlot, pyqtSignal, QCoreApplication)

from picuplib.globals import ALLOWED_ROTATION

from picup.functions import load_ui
from picup.functions import get_api_key, set_api_key
from picup.upload import Upload
from picup.globals import SUPPORTED_FILE_TYPES, __version__, DEFAULT_API_KEY
from picup.dialogs import ShowLinks, UrlInput, KeyRequest

import logging
LOGGER = logging.getLogger(__name__)





class MainWindow(QMainWindow):
    """
    Main window class.
    Includes the main window itself as well as handling of it's signals
    """

    upload_pictures = pyqtSignal(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_ui('MainWindow.ui', self)
        self.setWindowTitle('Picup - {}'.format(__version__))

        apikey = get_api_key()
        if not apikey:
            apikey = self.request_api_key()

        self.legal_resize = True
        self.upload_in_progress = False
        self.upload_thread = QThread(parent=self)
        self.upload = Upload(apikey=apikey)
        self.upload_thread.start()
        self.upload.moveToThread(self.upload_thread)


        self.list_view_files_model = FileListModel(parent=self)
        self.list_view_files.setModel(self.list_view_files_model)

        self.pushButton_close.clicked.connect(self.shutdown)
        self.pushButton_add_picture.clicked.connect(self.add_file)
        self.pushButton_add_links.clicked.connect(self.add_url)
        self.pushButton_upload.clicked.connect(self.start_upload)
        self.pushButton_clear_list.clicked.connect(
                self.list_view_files_model.clear_list)
        self.pushButton_remove_selected.clicked.connect(self.remove_selected)

        self.upload.upload_finished.connect(self.upload_finished)
        self.upload.upload_error.connect(self.handle_error)

        self.upload_pictures.connect(self.upload.upload_multiple)

        self.dialog = QFileDialog(parent=self)
        self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.setNameFilters(SUPPORTED_FILE_TYPES)

        self.resize_container.hide()
        self.resize_container_percentual.hide()
        self.check_box_resize.clicked.connect(
                self.set_resize_box_visibility
                )
        self.radio_button_absolute.toggled.connect(
                self.set_absolute_resize_box_visibility
                )
        self.radio_button_percentual.toggled.connect(
                self.set_percentual_resize_box_visibility
                )
        self.spin_box_width.valueChanged.connect(self.update_resize)
        self.spin_box_higth.valueChanged.connect(self.update_resize)
        self.spin_box_percentual.valueChanged.connect(self.update_resize)
        self.comboBox_rotate_options.activated['QString'].connect(
                self.upload.change_default_rotation
                )
        self.checkBox_delete_exif.toggled.connect(
                self.upload.change_default_exif
                )

        self.comboBox_rotate_options.addItems(ALLOWED_ROTATION)

    def request_api_key(self,):
        """
        requests and stores an api key from the user, if non is stores yet.
        If none is given a default one is used.
        """
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
        """
        add file(s) to the upload list.
        using Qts file dialog.
        """
        if self.dialog.exec_():
            files = self.dialog.selectedFiles()
            files = [(file_, 'file') for file_ in files]
            self.list_view_files_model.add_files(files)

    @pyqtSlot()
    def add_url(self,):
        """
        add url(s) to the upload list.
        using a text box.
        """
        url_input = UrlInput()
        code = url_input.exec_()
        urls = url_input.text()

        new_entrys = []
        not_added = []

        if code and urls != '':
            for url in urls.split('\n'):
                # skip empty lines
                if url == '':
                    continue
                parsed_url = urlparse(url, scheme='http')
                scheme = parsed_url.scheme.lower()
                if scheme in ['http', 'https', 'ftp']:
                    new_entrys.append((urlunparse(parsed_url), 'url'))

                else:
                    not_added.append(url)

            if not_added:
                message = QMessageBox(QMessageBox.Warning, 'Fehler',
                                      ('Ein oder mehrere link(s) konnten '
                                       'nicht hinzugefügt werden.'),
                                      buttons=QMessageBox.Ok,
                                      parent=self)
                message.setDetailedText('\n'.join(not_added))

            self.list_view_files_model.add_files(new_entrys)

    @pyqtSlot()
    def start_upload(self,):
        """
        starts the upload and does some setup for the status/result dialog.
        As well as some cleanup afterwards.
        It locks the application for any further uploads until this one is \
        finished.
        """
        if (len(self.list_view_files_model.files) and not
                    self.upload_in_progress and
                    self.legal_resize):
            self.upload_in_progress = True
            files = self.list_view_files_model.files.copy()

            link_dialog = ShowLinks(self.upload, len(files), parent=self)
            link_dialog.readd_pictures.connect(
                    self.list_view_files_model.add_files
                    )
            link_dialog.show()

            LOGGER.debug('emitting upload signal with arguments: %s', files)
            self.upload_pictures.emit(files)

            LOGGER.debug('cleanup main window')
            self.list_view_files_model.clear_list()

        elif self.upload_in_progress:
            LOGGER.debug('Upload already in progress.')
            QMessageBox.warning(self, 'Upload Läuft',
                                'Es läuft bereits ein Upload Prozess.')

        elif not self.legal_resize:
            LOGGER.debug('illegal resize string will not upload.')
            # pylint: disable=line-too-long
            # would harm readability
            QMessageBox.warning(self, 'Auflösung ungültig',
                                ('Die für die Skalierung angegebene Auflösung ist ungültig. '
                                 'Bitte gib diese im folgendem format an: breite x höhe')
                               )

        else:
            LOGGER.info('There is nothing to upload.')
            QMessageBox.information(self, 'Nüx da',
                                    ('Es wurden keine bilder zum hochladen '
                                     'hinzugefügt'))

    @pyqtSlot()
    def upload_finished(self,):
        """
        called through a signal after upload is finished to release the lock.
        """
        self.upload_in_progress = False

    @pyqtSlot(type, tuple)
    def handle_error(self, exception_type, args):
        """
        displays informations about an exception.
        """
        message = QMessageBox(QMessageBox.Warning, 'Fehler',
                              'Fehler beim upload.', buttons=QMessageBox.Ok,
                              parent=self)
        message.setDetailedText(repr(exception_type) + '\n' + repr(args))

        message.exec_()

    @pyqtSlot()
    def update_resize(self,):
        if (self.check_box_resize.isChecked() and
            self.radio_button_absolute.isChecked()):
            width = self.spin_box_width.value()
            higth = self.spin_box_higth.value()

            self.upload.change_default_resize("{}x{}".format(width, higth))

        elif (self.check_box_resize.isChecked() and
              self.radio_button_percentual.isChecked()):

            percentage = self.spin_box_percentual.value()
            self.upload.change_default_resize("{}%".format(percentage))

        else:
            self.upload.change_default_resize(None)

    @pyqtSlot(bool)
    def set_resize_box_visibility(self, visible):
        if visible:
            LOGGER.debug('show resize box')
            self.update_resize()
        else:
            LOGGER.debug('hide resize box')
            self.update_resize()

        self.resize_container.setVisible(visible)

    @pyqtSlot(bool)
    def set_absolute_resize_box_visibility(self, visible):
        if visible:
            LOGGER.debug('show absolute resize box')
            self.update_resize()
        else:
            LOGGER.debug('hide absolute resize box')

        self.resize_container_absolute.setVisible(visible)

    @pyqtSlot(bool)
    def set_percentual_resize_box_visibility(self, visible):
        if visible:
            LOGGER.debug('show percentual resize box')
            self.update_resize()
        else:
            LOGGER.debug('hide percentual resize box')

        self.resize_container_percentual.setVisible(visible)

    @pyqtSlot()
    def remove_selected(self,):
        """
        remove selected files from the upload list.
        """
        for item in self.list_view_files.selectedIndexes():
            self.list_view_files_model.remove_element(item.row(), item.row())

    @pyqtSlot()
    def display_about_qt(self,):
        """
        displays the about qt dialog
        """
        QMessageBox.aboutQt(self,)

    @pyqtSlot()
    def shutdown(self,):
        """shut down Qapp"""
        self.thread_cleanup()

        QCoreApplication.instance().quit()

    def thread_cleanup(self):
        """
        shuts down the upload thread at exit.
        """
        LOGGER.debug('begin cleanup threads')
        try:
            self.upload_thread.quit()
            self.upload_thread.wait()
        # pylint: disable=bare-except
        # I do want to catch them all here, to be able to log them.
        except:
            LOGGER.exception('Exception while cleanup')
        LOGGER.debug('thread cleanup finished')


class FileListModel(QAbstractListModel):
    """
    Qt Model for the file/upload list.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.files = []

    # pylint: disable=invalid-name,unused-argument
    # this name is neccacary for a working ListModel implementation
    # same counts for the argument
    def rowCount(self, parent):
        """
        returns the amount of rows
        Required for a ListModel implementation.
        """
        return len(self.files)

    def data(self, index, role):
        """
        returns requestet data.
        Required for a ListModel implementation.
        """
        if role == Qt.DisplayRole:
            return self.files[index.row()][0]

    @pyqtSlot(list)
    def add_files(self, files):
        """
        add elements to the model
        """
        prev_len = len(self.files)

        self.beginInsertRows(QModelIndex(), prev_len, prev_len + len(files))
        self.files.extend(files)
        self.endInsertRows()

    @pyqtSlot()
    def clear_list(self,):
        """
        remove all elements from the model
        """
        self.beginRemoveRows(QModelIndex(), 0, len(self.files)-1)
        self.files.clear()
        self.endRemoveRows()

    def remove_element(self, first, last):
        """
        remove elements from the model
        """
        self.beginRemoveRows(QModelIndex(), first, last)
        del self.files[first:last+1]
        self.endRemoveRows()

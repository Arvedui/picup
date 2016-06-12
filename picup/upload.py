# -*- coding:utf8 -*-

"""
Module for upload abstraction
"""


from picuplib import Upload as PicflashUpload
from picuplib.exceptions import MallformedResize

from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot


import logging
LOGGER = logging.getLogger(__name__)


class Upload(QObject):
    """
    handels the upload abstraction
    """

    picture_uploaded = pyqtSignal(tuple)
    upload_finished = pyqtSignal(list)
    upload_error = pyqtSignal(type, tuple)
    legal_resize_string = pyqtSignal(bool)

    def __init__(self, apikey, **kwargs):
        super().__init__(**kwargs)
        self.uploader = PicflashUpload(apikey=apikey)

    @pyqtSlot(list)
    def upload_multiple(self, files):
        """
        Handels upload of multiple files

        files is a list of tuples (filename, type)
        """
        LOGGER.info('starting upload process')
        LOGGER.debug('recived file paths: %s', files)

        failed = []

        for file_, type_ in files:
            try:
                links = self.upload(file_, type_)

                self.picture_uploaded.emit((file_, type_, links))
                LOGGER.info('Uploaded %s', file_)
            # pylint: disable=broad-except
            # the amount of possible exceptions is just to big
            except Exception:  # yes in know its bad, …
                failed.append((file_, type_))
                LOGGER.exception(
                        'An exception happend durring the upload of %s.',
                        file_
                        )

        self.upload_finished.emit(failed)
        logging.info('upload finished')

    def upload(self, file_, type_):
        """
        hands over the upload to picuplib
        """
        if type_ == 'file':
            links = self.uploader.upload(file_)
        if type_ == 'url':
            links = self.uploader.remote_upload(file_)

        return links

    @pyqtSlot(str)
    def change_default_rotation(self, rotation):
        """
        changes the default rotation in the underlying Upload class
        """
        LOGGER.debug('Default rotation changed to %s', rotation)
        self.uploader.rotation = rotation

    @pyqtSlot(str)
    def change_default_resize(self, resize):
        """
        changes the default resize parameter in the underlying Upload class
        """
        if resize == '':
            resize = None

        LOGGER.debug('Default resize changed to %s', resize)

        try:
            self.uploader.resize = resize
            self.legal_resize_string.emit(True)
        except MallformedResize:
            LOGGER.debug('illegal resize string.')
            self.legal_resize_string.emit(False)

    @pyqtSlot(bool)
    def change_default_exif(self, delete_exif):
        """
        chages the default exif parameter in the underlying Upload class
        """
        LOGGER.debug('Default exif deletion changed to %s', delete_exif)
        self.uploader.noexif = delete_exif

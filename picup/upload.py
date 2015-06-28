# -*- coding:utf8 -*-

"""
Module for upload abstraction
"""


from picuplib import Upload as PicflashUpload

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication


import logging
logger = logging.getLogger(__name__)


class Upload(QObject):
    """
    handels the upload abstraction
    """

    picture_uploaded = pyqtSignal(tuple)
    upload_finished = pyqtSignal(list)
    upload_error = pyqtSignal(type, tuple)

    def __init__(self, apikey):
        super().__init__()
        self.uploader = PicflashUpload(apikey=apikey)

    @pyqtSlot(list)
    def upload_multiple(self, files):
        """
        Handels upload of multiple files

        files is a list of tuples (filename, type)
        """
        logger.info('starting upload process')
        logger.debug('recived file paths: %s', files)

        failed = []

        for file_, type_ in files:
            try:
                links = self.upload(file_, type_)

                self.picture_uploaded.emit((file_, type_, links))
                logger.info('Uploaded %s', file_)
            except Exception as e:  # yes in know its bad, …
                #self.upload_error.emit(type(e), e.args)
                failed.append((file_, type_))
                logger.exception('An exception happend durring the upload of %s.', file_)

        self.upload_finished.emit(failed)
        logging.info('upload finished')

    def upload(self, file_, type_):
        """
        hands over the upload to picuplib will retry three times
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
        logger.debug('Default rotation changed to %s', rotation)
        self.uploader.rotation = rotation

    @pyqtSlot(str)
    def change_default_resize(self, resize):
        """
        changes the default resize parameter in the underlying Upload class
        """
        if resize == '':
            resize = 'og'

        logger.debug('Default resize changed to %s', resize)

        self.uploader.resize = resize

    @pyqtSlot(str)
    def change_default_exif(self, delete_exif):
        """
        chages the default exif parameter in the underlying Upload class
        """
        logger.debug('Default exif deletion changed to %s', delete_exif)
        self.uploader.noexif = delete_exif

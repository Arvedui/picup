# -*- coding:utf8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot


from picup.functions import load_ui


import logging
logger = logging.getLogger(__name__)


class UrlInput(QDialog):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

# -*- coding:utf8 -*-
"""
module for the UrlInput dialog
"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot


from picup.functions import load_ui


import logging
LOGGER = logging.getLogger(__name__)


class UrlInput(QDialog):
    """
    Dialog for entering text.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        load_ui('link_input.ui', self)

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

    @pyqtSlot()
    def reject(self,):
        """
        closes dialog and returns an error
        """
        LOGGER.debug('Abborted by user.')
        self.done(False)

    @pyqtSlot()
    def accept(self,):
        """
        closses dialog
        """
        LOGGER.debug('Closed graceful by user.')
        self.done(True)

    def text(self,):
        """
        return the text entered into the dialog
        """
        return self.plainTextEdit.toPlainText()

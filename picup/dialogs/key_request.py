# -*- coding:utf8 -*-
"""
module for the KeyRequest dialog
"""

from PyQt5.QtWidgets import QDialog


from picup.functions import load_ui


class KeyRequest(QDialog):
    """
    KeyRequest dialog.
    gets an api key from the user.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_ui('KeyRequest.ui', self)

        self.pushButton_cancel.clicked.connect(self.reject)
        self.pushButton_ok.clicked.connect(self.accept)

# -*- coding:utf8 -*-
"""
misc funtions
"""

import logging
import sys
import os.path

from PyQt5.QtCore import QSettings

from pkg_resources import resource_filename

LOGGER = logging.getLogger(__name__)


def get_QSettings():
    """
    return a QSettings instanze
    """
    settings = QSettings()
    settings.setIniCodec('utf-8')
    LOGGER.debug('QSettings format set to: %s', settings.format())
    return settings


def get_file_path(relativ_path):
    """
    file path abstraction for pyinstaller
    """

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativ_path)
    else:
        return resource_filename('picup', relativ_path)

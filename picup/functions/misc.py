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


def get_settings():
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
    # pylint: disable=no-member,protected-access
    # _MEIPASS is there if executed in a pyinstaller package
    # and access to private member is necacary to get he folder
    # where pyinstaller extracted the application files
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativ_path)
    else:
        return resource_filename('picup', relativ_path)

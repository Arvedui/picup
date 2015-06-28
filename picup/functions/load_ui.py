# -*- coding:utf8 -*-
"""
module for loding ui files
"""

import logging

from os import path
from PyQt5.uic import loadUi, loadUiType

from picup.functions.misc import get_file_path

LOGGER = logging.getLogger(__name__)


def load_ui(file_name, baseinstance=None):
    """
    loads a ui file und return the resulting object
    """
    file_path = get_file_path(path.join('ui_files', file_name))

    LOGGER.debug('load ui file %s', file_path)

    return loadUi(file_path, baseinstance)


def load_ui_factory(file_name):
    """
    loads a ui factory
    """
    file_path = get_file_path(path.join('ui_files', file_name))

    LOGGER.debug('create factory from %s', file_name)

    return loadUiType(file_path)

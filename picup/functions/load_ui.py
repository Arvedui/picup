# -*- coding:utf8 -*-
######################## BEGIN LICENSE BLOCK ########################
# picup - small gui tool for uploading pictures to picflash
# Copyright (C) 2014  Arvedui
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA
######################### END LICENSE BLOCK #########################
"""
module for loding ui files
"""

import logging

from os import path
try:
    from PyQt5.uic import loadUi, loadUiType
except ImportError:
    from PyQt4.uic import loadUi, loadUiType
from pkg_resources import resource_filename

from picup.functions.misc import get_file_path

logger = logging.getLogger(__name__)

def load_ui(file_name, baseinstance=None):
    """
    loads a ui file und return the resulting object
    """
    file_path = get_file_path(path.join('ui_files', file_name))

    logger.debug('load ui file %s', file_path)

    return loadUi(file_path, baseinstance)

def load_ui_factory(file_name):
    file_path = get_file_path(path.join('ui_files', file_name))

    logger.debug('create factory from %s', file_name)

    return loadUiType(file_path)

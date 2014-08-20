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

import sys
import logging

from os import path
from PyQt5.uic import loadUi

from picup.globals import BASEDIR

UI_DIR = path.join(BASEDIR, 'picup', 'ui_files')


def load_ui(file_name, baseinstance = None):
    """
    loads a ui file und return the resulting object
    """

    file_path = path.join(UI_DIR, file_name)

    logging.info('load ui file %s' % file_path)

    return loadUi(file_path, baseinstance)

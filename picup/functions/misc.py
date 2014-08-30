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

import logging
import sys
import os.path

try:
    from PyQt5.QtCore import QSettings
except:
    from PyQt4.QtCore import QSettings

from pkg_resources import resource_filename



def get_QSettings():
    settings = QSettings()
    settings.setIniCodec('utf-8')
    logging.info('QSettings format set to: %s' % settings.format())
    return settings

def get_file_path(relativ_path):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativ_path)
    else:
        return resource_filename('picup', relativ_path)

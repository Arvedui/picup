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
from __future__ import unicode_literals

import sys

from os import path

__version__ = '0.3'

BASEDIR = path.dirname(path.abspath(sys.argv[0]))

DEFAULT_API_KEY = 'f4Shgrf6E'

SUPPORTED_FILE_TYPES = (
    'Erlaubte Formate (*.png *.jpg *.jpeg *.gif *.pdf)',
    'Alle Dateien (*)'
    )


BB_TEMPLTATE = '[url={}][img]{}[/img][/url]'

LINKTYPES = {'Sharelink': 'sharelink',
             'Direktlink':'hotlink',
             'Vorschau':'thumbnail',
             'BB Direktlink': 'bb_hotlink',
             'BB Vorschau': 'bb_thumbnail',
             'Lösch Link': 'delete_url'}

LINKTYPE_ORDER = ('Sharelink', 'Direktlink', 'Vorschau', 'BB Direktlink',
                  'BB Vorschau', 'Lösch Link', )

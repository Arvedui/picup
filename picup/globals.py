# -*- coding:utf8 -*-

from __future__ import unicode_literals

import sys

from os import path

__version__ = '0.4'

BASEDIR = path.dirname(path.abspath(sys.argv[0]))

DEFAULT_API_KEY = 'f4Shgrf6E'

SUPPORTED_FILE_TYPES = (
    'Erlaubte Formate (*.png *.jpg *.jpeg *.gif *.pdf)',
    'Alle Dateien (*)'
    )


BB_TEMPLTATE = '[url={}][img]{}[/img][/url]'

LINKTYPES = {'Sharelink': 'sharelink',
             'Direktlink': 'hotlink',
             'Vorschau': 'thumbnail',
             'BB Direktlink': 'bb_hotlink',
             'BB Vorschau': 'bb_thumbnail',
             'Lösch Link': 'delete_url'}

LINKTYPE_ORDER = ('Sharelink', 'Direktlink', 'Vorschau', 'BB Direktlink',
                  'BB Vorschau', 'Lösch Link', )

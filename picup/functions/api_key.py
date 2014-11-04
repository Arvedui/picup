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
some apikey related functions
"""


from picup.functions.misc import get_QSettings

import logging
LOGGER = logging.getLogger(__name__)

def get_api_key():
    """
    reads apikey from Qt Settings, if not present return None
    """
    settings = get_QSettings()
    if settings.contains('apikey'):
        apikey = settings.value('apikey')
    else:
        apikey = None

    LOGGER.debug('Using api key: %s', apikey)
    return apikey


def set_api_key(apikey):
    """
    writes apikey into Qt Settings
    """
    settings = get_QSettings()
    settings.setValue('apikey', apikey)

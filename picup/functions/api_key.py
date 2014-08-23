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

import json

import picup

from picup.functions.misc import get_QSettings
from picup.globals import DEFAULT_API_KEY
from picup.dialogs import KeyRequest
#import picup.model.key_request
#import picup.model.key_request

#picup.KeyRequest


#print(json.dumps(str(locals())))

import logging

def get_api_key(parent):
    #return '4UK55Y0D'
    settings = get_QSettings()
    if settings.contains('apikey'):
        apikey = settings.value('apikey')
    else:
        apikey = request_api_key(parent, settings)

    logging.debug('Using api key: %s' % apikey)
    return apikey


def request_api_key(parent, settings):
    window = KeyRequest(parent=parent)
    if window.exec_():
        apikey = window.lineEdit_apikey.text()
        settings.setValue('apikey', apikey)
        return apikey

    return DEFAULT_API_KEY




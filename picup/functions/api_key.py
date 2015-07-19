# -*- coding:utf8 -*-
"""
some apikey related functions
"""


from picup.functions.misc import get_settings

import logging
LOGGER = logging.getLogger(__name__)


def get_api_key():
    """
    reads apikey from Qt Settings, if not present return None
    """
    settings = get_settings()
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
    settings = get_settings()
    settings.setValue('apikey', apikey)

# -*- coding: utf-8 -*-

import logging
logging.getLogger('restnuage').addHandler(logging.NullHandler())

from ConfigParser import ConfigParser
config = ConfigParser()
config.read('./settings.cfg')

try:
    DEFAULT_USER = config.get('default', 'user')
    DEFAULT_PASSWORD = config.get('default', 'password')
    DEFAULT_ENTERPRISE = config.get('default', 'enterprise')
    DEFAULT_URL = config.get('default', 'url')
except:
    raise Exception('Configuration is missing. Please create your settings.cfg that determines your [default] section')

__all__ = ['NURESTBasicUser', 'NURESTConnection', 'NURESTFetcher', 'NURESTLoginController', 'NURESTObject', 'NURESTPushCenter', 'NURESTRequest', 'NURESTResponse']

from restnuage.nurest_user import NURESTBasicUser
from restnuage.nurest_connection import NURESTConnection
from restnuage.nurest_fetcher import NURESTFetcher
from restnuage.nurest_login_controller import NURESTLoginController
from restnuage.nurest_object import NURESTObject
from restnuage.nurest_push_center import NURESTPushCenter
from restnuage.nurest_request import NURESTRequest
from restnuage.nurest_response import NURESTResponse

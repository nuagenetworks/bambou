# -*- coding: utf-8 -*-

import logging

# NullHandler is only available for python >= 2.7
logging.getLogger('bambou').addHandler(logging.NullHandler())

__all__ = ['NURESTBasicUser', 'NURESTConnection', 'NURESTFetcher', 'NURESTLoginController', 'NURESTObject', 'NURESTPushCenter', 'NURESTRequest', 'NURESTResponse']

from bambou.nurest_user import NURESTBasicUser
from bambou.nurest_connection import NURESTConnection
from bambou.nurest_fetcher import NURESTFetcher
from bambou.nurest_login_controller import NURESTLoginController
from bambou.nurest_object import NURESTObject
from bambou.nurest_push_center import NURESTPushCenter
from bambou.nurest_request import NURESTRequest
from bambou.nurest_response import NURESTResponse

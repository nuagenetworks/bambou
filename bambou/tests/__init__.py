# -*- coding: utf-8 -*-

import logging

from bambou import bambou_logger
from bambou.nurest_session import _NURESTSessionCurrentContext
from bambou.tests.models import User, Enterprise, NURESTTestSession

bambou_logger.setLevel(logging.ERROR)


def start_session(username="user", password="password", enterprise="enterprise", api_url="https://vsd:8443", version="3.2"):
    """ Log in and fetch api key """

    session = NURESTTestSession(username=username, password=password, enterprise=enterprise, api_url=api_url, version=version)

    user = User()
    user.api_key = u"51f31042-b047-48ca-a88b-68368608e3da"
    user.email = u"john.doe@enterprse.com"
    user.enterprise_id = u"<enterprise_id>"
    user.enterprise_name = u"enterprise"
    user.firstname = u"John",
    user.id = u"<user_id>"
    user.lastname = u"Doe"
    user.role = u"ROLE"

    # Set API KEY
    session._login_controller.api_key = user.api_key

    # Activate session
    _NURESTSessionCurrentContext.session = session

    return session


def get_valid_enterprise(id, name):
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.id = id
    enterprise.name = name

    return enterprise

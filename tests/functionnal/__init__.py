# -*- coding: utf-8 -*-

import logging

from bambou import bambou_logger
from bambou.nurest_session import _NURESTSessionCurrentContext

from tests.models import User, Enterprise, Group, NURESTTestSession

bambou_logger.setLevel(logging.ERROR)


def start_session(username="user", password="password", enterprise="enterprise", api_url="https://vsd:8443", version="3.2", api_prefix="api"):
    """ Log in and fetch api key """

    session = NURESTTestSession(username=username, password=password, enterprise=enterprise, api_url=api_url, version=version, api_prefix=api_prefix)

    user = User()
    user.api_key ="51f31042-b047-48ca-a88b-68368608e3da"
    user.email ="john.doe@enterprse.com"
    user.enterprise_id ="<enterprise_id>"
    user.enterprise_name ="enterprise"
    user.firstname ="John",
    user.id ="<user_id>"
    user.lastname ="Doe"
    user.role ="ROLE"

    # Set API KEY
    session._login_controller.api_key = user.api_key

    # Activate session
    _NURESTSessionCurrentContext.session = session

    return user


def get_valid_enterprise(id, name):
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.id = id
    enterprise.name = name

    return enterprise

def get_valid_group(id, name):
    """ Returns a valid group object """

    group = Group()
    group.id = id
    group.name = name

    return group

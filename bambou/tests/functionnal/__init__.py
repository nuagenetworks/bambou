# -*- coding: utf-8 -*-

import logging

from bambou import bambou_logger, NURESTLoginController
from bambou.tests import User, Enterprise

bambou_logger.setLevel(logging.ERROR)


def get_login_as_user():
    """ Log in and fetch api key """

    controller = NURESTLoginController()
    controller.reset()  # Force cleaning previous session

    controller.user = u"user"
    controller.password = u"password"
    controller.enterprise = u"enterprise"
    controller.url = u"https://<host>:<port>/nuage/api/v3_0"

    user = User()
    user.api_key = u"51f31042-b047-48ca-a88b-68368608e3da"
    user.email = u"john.doe@enterprse.com"
    user.enterprise_id = u"<enterprise_id>"
    user.enterprise_name = controller.enterprise
    user.firstname = u"John",
    user.id = u"<user_id>"
    user.lastname = u"Doe"
    user.role = u"ROLE"

    controller.api_key = user.api_key

    return user


def get_valid_enterprise(id, name):
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.id = id
    enterprise.name = name

    return enterprise

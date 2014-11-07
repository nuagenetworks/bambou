# -*- coding: utf-8 -*-

import logging

from bambou import bambou_logger, NURESTLoginController
from bambou.tests import User, Enterprise

bambou_logger.setLevel(logging.INFO)

def login_as_csproot():
    """ Log in and fetch api key """

    controller = NURESTLoginController()
    controller.reset()  # Force cleaning previous session

    controller.user = u"csproot"
    controller.password = u"csproot"
    controller.enterprise = u"csp"
    controller.url = u"https://135.227.220.152:8443/nuage/api/v3_0"

    csproot = User()
    csproot.fetch()
    controller.api_key = csproot.api_key

    return csproot


def delete_enterprises(user):
    """ Delete all enterprises of the given user """

    user.enterprises_fetcher.fetch_objects()

    for enterprise in user.enterprises:
        if enterprise.name != "Triple A":
            enterprise.delete(response_choice=1)

def create_enterprises(user, count):
    """ Creates a number of enterprise for the given user

        Args:
            user: User to attach enterprises
            count: Number of enterprises to create
    """

    for index in range(0, count):
        enterprise = Enterprise()
        enterprise.name = u"AutoTesting Enterprise %s" % str(index)
        user.add_child_object(enterprise)
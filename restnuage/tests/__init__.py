# -*- coding: utf-8 -*-

from restnuage import NURESTLoginController
from restnuage.tests.models import Enterprise, User

def build_login_controller(user, password, enterprise):
    """ Init and returns login controller """

    controller = NURESTLoginController()
    controller.user = user
    controller.password = password
    controller.enterprise = enterprise
    controller.url = u"https://135.227.220.152:8443/nuage/api/v1_0"

    return controller


def authenticate_with_user(user_info):
    """ Authenticate user """

    controller = build_login_controller(user=user_info['user'], password=user_info['password'], enterprise=user_info['enterprise'])

    user = User()
    user.fetch()

    # Set API Key
    controller.api_key = user.api_key

    return user


def create_enterprise(name=u'Random Name', description=None):
    """ Returns an enterprise """

    enterprise = Enterprise()
    enterprise.name = name
    enterprise.description = description

    return enterprise
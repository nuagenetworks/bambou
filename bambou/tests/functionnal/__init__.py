# -*- coding: utf-8 -*-

import logging

from mock import MagicMock

from bambou import bambou_logger, NURESTLoginController, NURESTConnection, NURESTResponse
from bambou.tests import User, Enterprise

bambou_logger.setLevel(logging.INFO)


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


def build_mock_response(status_code, data, filter=None, order_by=None, page=None, error=None):
    """ Build a fake response

        Args:
            status_code: the status code
            data: the NURESTObject
            filter: a string representing a filter
            order_by: a string representing an order by
            page: a page number

    """
    connection = NURESTConnection(request=None, async=False)

    result = None
    if type(data) == list:
        result = list()
        for obj in data:
            result.append(obj.to_dict())
    else:
        connection.user_info = data
        result = data.to_dict()

    headers = dict()
    if filter:
        headers['X-Nuage-Filter'] = str(filter)

    if order_by:
        headers['X-Nuage-OrderBy'] = str(order_by)

    if page:
        headers['X-Nuage-Page'] = page

    print result
    connection.response = NURESTResponse(status_code=status_code, data=result, headers=headers)

    if error:
        connection.response.errors['Error'] = error

    return MagicMock(return_value=connection)


def get_mock_arg(mock, name):
    """ Get the argument of a mock call

        Args:
            mock: the mock that has been called
            name: the name of the argument

    """
    args = mock.call_args[1]

    if name in args:
        return args[name]

    return None

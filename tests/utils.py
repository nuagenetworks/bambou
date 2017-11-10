# -*- coding: utf-8 -*-

import json

from requests.models import Response
from mock import MagicMock


class MockUtils(object):

    @classmethod
    def create_mock_response(cls, status_code, data, filter=None, order_by=None, page=None, error=None, headers=None):
        """ Build a fake response

            Args:
                status_code: the status code
                data: the NURESTObject
                filter: a string representing a filter
                order_by: a string representing an order by
                page: a page number

        """

        content = None
        if type(data) == list:
            content = list()
            for obj in data:
                content.append(obj.to_dict())
        elif data:
            content = data.to_dict()

        response = Response()
        response.status_code = status_code
        response._content = json.dumps(content).encode('utf-8')

        if headers:
            response.headers = headers

        return MagicMock(return_value=response)

    @classmethod
    def get_mock_parameter(cls, mock, name):
        """ Get the argument of a mock call

            Args:
                mock: the mock that has been called
                name: the name of the argument

        """
        args = mock.call_args[1]

        if name in args:
            return args[name]

        return None

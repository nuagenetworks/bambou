# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import get_login_as_user, get_valid_enterprise


class Create(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = get_login_as_user()

    @classmethod
    def tearDownClass(self):
        pass

    def test_create(self):
        """ POST /enterprises create enterprise """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = MockUtils.create_mock_response(status_code=201, data=enterprise)

        with patch('requests.request', mock):
            (obj, connection) = user.add_child_object(enterprise)

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(method, u'POST')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.name, enterprise.name)
        self.assertEqual(connection.response.status_code, 201)

    def test_create_raise_error(self):
        """ POST /enterprises create enterprise raises an error """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = MockUtils.create_mock_response(status_code=409, data=enterprise, error=u"Name already exists")

        with patch('requests.request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = user.add_child_object(enterprise)

# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from tests.utils import MockUtils
from tests.functionnal import start_session, get_valid_enterprise


class Create(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = start_session()

    @classmethod
    def tearDownClass(self):
        pass

    def test_create(self):
        """ POST /enterprises create enterprise """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = MockUtils.create_mock_response(status_code=201, data=enterprise)

        with patch('requests.request', mock):
            (obj, connection) = user.create_child(enterprise)

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, 'https://vsd:8443/api/v3_2/enterprises')
        self.assertEqual(method, 'POST')
        self.assertEqual(headers['Authorization'], 'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], 'enterprise')
        self.assertEqual(headers['Content-Type'], 'application/json')

        self.assertEqual(connection.response.status_code, 201)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.name, enterprise.name)
        self.assertIn(obj, user.enterprises)
        self.assertIn(enterprise, user.enterprises)

        user.enterprises.flush()

    def test_create_without_commit(self):
        """ POST /enterprises create enterprise without commit """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = MockUtils.create_mock_response(status_code=201, data=enterprise)

        with patch('requests.request', mock):
            (obj, connection) = user.create_child(enterprise, commit=False)

        self.assertNotIn(obj, user.enterprises)
        self.assertNotIn(enterprise, user.enterprises)

    def test_create_raise_error(self):
        """ POST /enterprises create enterprise raises an error """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = MockUtils.create_mock_response(status_code=409, data=enterprise, error=u"Name already exists")

        with patch('requests.request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = user.create_child(enterprise)

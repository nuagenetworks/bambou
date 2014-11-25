# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests.functionnal import get_login_as_user, build_mock_response, get_mock_arg, get_valid_enterprise


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
        mock = build_mock_response(status_code=201, data=enterprise)

        with patch('bambou.NURESTObject.send_request', mock):
            (obj, connection) = user.add_child_object(enterprise)

        request = get_mock_arg(mock, 'request')

        self.assertEqual(connection.response.status_code, 201)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(request.method, u'POST')

        self.assertNotEqual(obj.id, None)
        self.assertEqual(obj.name, enterprise.name)

    def test_create_raise_error(self):
        """ POST /enterprises create enterprise raises an error """

        user = self.user
        enterprise = get_valid_enterprise(id=1, name=u"Enterprise")
        mock = build_mock_response(status_code=409, data=enterprise, error=u"Name already exists")

        with patch('bambou.NURESTObject.send_request', mock):
            with self.assertRaises(Exception):
                (obj, connection) = user.add_child_object(enterprise)

        request = get_mock_arg(mock, 'request')
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(request.method, u'POST')

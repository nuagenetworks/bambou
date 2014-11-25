# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from bambou.tests.functionnal import get_login_as_user, build_mock_response, get_mock_arg, get_valid_enterprise


class Delete(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = get_login_as_user()
        cls.enterprise = get_valid_enterprise(id=1, name=u"Enterprise")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_delete(self):
        """ DELETE /enterprises delete enterprise """

        mock = build_mock_response(status_code=204, data=self.enterprise)

        with patch('bambou.NURESTObject.send_request', mock):
            (obj, connection) = self.enterprise.delete(response_choice=1)

        request = get_mock_arg(mock, 'request')

        self.assertEqual(connection.response.status_code, 204)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises/%s?responseChoice=1' % self.enterprise.id)
        self.assertEqual(request.method, u'DELETE')

        self.assertEqual(obj.name, self.enterprise.name)
        self.assertEqual(obj.id, self.enterprise.id)

    def test_delete_raise_error(self):
        """ DELETE /enterprises delete enterprise raise error """

        mock = build_mock_response(status_code=400, data=self.enterprise, error=u"Internal error")

        with patch('bambou.NURESTObject.send_request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = self.enterprise.delete(response_choice=1)

        request = get_mock_arg(mock, 'request')
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises/%s?responseChoice=1' % self.enterprise.id)
        self.assertEqual(request.method, u'DELETE')

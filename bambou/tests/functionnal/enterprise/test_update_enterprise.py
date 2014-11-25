# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from bambou.tests.functionnal import get_login_as_user, build_mock_response, get_mock_arg, get_valid_enterprise


class Update(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = get_login_as_user()
        cls.enterprise = get_valid_enterprise(id=1, name=u"Enterprise")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_update(self):
        """ PUT /enterprises update enterprise """

        enterprise = self.enterprise
        enterprise.name = u"Another name"
        mock = build_mock_response(status_code=200, data=enterprise)

        with patch('bambou.NURESTObject.send_request', mock):
            (obj, connection) = enterprise.save()

        request = get_mock_arg(mock, 'request')

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises/%s' % enterprise.id)
        self.assertEqual(request.method, u'PUT')

        self.assertEqual(obj.name, u"Another name")
        self.assertEqual(enterprise.name, u"Another name")

    def test_update_raise_error(self):
        """ PUT /enterprises update enterprise raise error """

        enterprise = self.enterprise
        enterprise.name = u"Another name"
        mock = build_mock_response(status_code=404, data=enterprise, error=u"Enterprise not found")

        with patch('bambou.NURESTObject.send_request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = enterprise.save()

        request = get_mock_arg(mock, 'request')
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises/%s' % enterprise.id)
        self.assertEqual(request.method, u'PUT')

# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import get_login_as_user, get_valid_enterprise


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
        mock = MockUtils.create_mock_response(status_code=200, data=enterprise)

        with patch('requests.request', mock):
            (obj, connection) = enterprise.save()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, u'https://<host>:<port>/nuage/api/v3_0/enterprises/%s' % enterprise.id)
        self.assertEqual(method, u'PUT')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(obj.name, u"Another name")
        self.assertEqual(enterprise.name, u"Another name")
        self.assertEqual(connection.response.status_code, 200)

    def test_update_raise_error(self):
        """ PUT /enterprises update enterprise raise error """

        enterprise = self.enterprise
        enterprise.name = u"Another name"
        mock = MockUtils.create_mock_response(status_code=404, data=enterprise, error=u"Enterprise not found")

        with patch('requests.request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = enterprise.save()

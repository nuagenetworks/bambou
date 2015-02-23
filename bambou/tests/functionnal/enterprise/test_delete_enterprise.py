# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import start_session, get_valid_enterprise


class Delete(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = start_session()
        cls.enterprise = get_valid_enterprise(id=1, name=u"Enterprise")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_delete(self):
        """ DELETE /enterprises delete enterprise """

        mock = MockUtils.create_mock_response(status_code=204, data=self.enterprise)

        with patch('requests.request', mock):
            (obj, connection) = self.enterprise.delete(response_choice=1)

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, u'https://vsd:8443/nuage/api/v3_2/enterprises/%s?responseChoice=1' % self.enterprise.id)
        self.assertEqual(method, u'DELETE')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(obj.name, self.enterprise.name)
        self.assertEqual(obj.id, self.enterprise.id)
        self.assertEqual(connection.response.status_code, 204)

    def test_delete_raise_error(self):
        """ DELETE /enterprises delete enterprise raise error """

        mock = MockUtils.create_mock_response(status_code=400, data=self.enterprise, error=u"Internal error")

        with patch('requests.request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = self.enterprise.delete(response_choice=1)

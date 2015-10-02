# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import start_session


class Update(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = start_session()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_update(self):
        """ PUT /me update current user """

        self.user.prepare_change_password('test')

        mock = MockUtils.create_mock_response(status_code=204, data=None)

        with patch('requests.request', mock):
            (obj, connection) = self.user.save()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(connection.response.status_code, 204)
        self.assertEqual(url, u'https://vsd:8443/api/v3_2/me')
        self.assertEqual(method, u'PUT')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjp0ZXN0')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(self.user.password, u"a94a8fe5ccb19ba61c4c0873d391e987982fbbd3")  # Encrypted password

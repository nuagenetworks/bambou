# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError, InternalConsitencyError
from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import start_session, get_valid_enterprise
from bambou.tests.models import Enterprise

class Fetch(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = start_session()
        cls.enterprise = get_valid_enterprise(id=1, name=u"Enterprise")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_fetch(self):
        """ GET /enterprises/id fetch enterprise """

        enterprise = Enterprise(id=1)
        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprise)

        with patch('requests.request', mock):
            (obj, connection) = enterprise.fetch()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, 'https://vsd:8443/api/v3_2/enterprises/%s' % enterprise.id)
        self.assertEqual(method, 'GET')
        self.assertEqual(headers['Authorization'], 'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], 'enterprise')
        self.assertEqual(headers['Content-Type'], 'application/json')

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(enterprise.name, obj.name)


    def test_fetch_without_id(self):
        """ GET /enterprises fetch enterprise without id will fail """

        enterprise = Enterprise()

        with self.assertRaises(InternalConsitencyError):
            (obj, connection) = enterprise.fetch()

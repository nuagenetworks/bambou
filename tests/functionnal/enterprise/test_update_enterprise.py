# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.exceptions import BambouHTTPError
from tests.utils import MockUtils
from tests.functionnal import start_session, get_valid_enterprise


class Update(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = start_session()
        cls.enterprise = get_valid_enterprise(id=1, name=u"Enterprise")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_update(self):
        """ PUT /enterprises update enterprise """

        enterprise = self.enterprise
        enterprise.name ="Another name"
        mock = MockUtils.create_mock_response(status_code=200, data=enterprise)

        with patch('requests.Session.request', mock):
            (obj, connection) = enterprise.save()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, 'https://vsd:8443/api/v3_2/enterprises/%s' % enterprise.id)
        self.assertEqual(method, 'PUT')
        self.assertEqual(headers['Authorization'], 'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], 'enterprise')
        self.assertEqual(headers['Content-Type'], 'application/json')

        self.assertEqual(obj.name,"Another name")
        self.assertEqual(enterprise.name,"Another name")
        self.assertEqual(connection.response.status_code, 200)

    def test_update_raise_error(self):
        """ PUT /enterprises update enterprise raise error """

        enterprise = self.enterprise
        enterprise.name ="Another name"
        mock = MockUtils.create_mock_response(status_code=404, data=enterprise, error=u"Enterprise not found")

        with patch('requests.Session.request', mock):
            with self.assertRaises(BambouHTTPError):
                (obj, connection) = enterprise.save()

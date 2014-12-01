# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import get_login_as_user, get_valid_enterprise


class Fetch(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = get_login_as_user()
        cls.enterprises = list()
        cls.enterprises.append(get_valid_enterprise(id=1, name=u"Enterprise 1"))
        cls.enterprises.append(get_valid_enterprise(id=2, name=u"Enterprise 2"))
        cls.enterprises.append(get_valid_enterprise(id=3, name=u"Enterprise 3"))
        cls.enterprises.append(get_valid_enterprise(id=4, name=u"Enterprise 4"))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_fetch_all(self):
        """ GET /enterprises retrieve all enterprises """

        user = self.user
        enterprises = self.enterprises

        mock = MockUtils.create_mock_response(status_code=200, data=enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(method, u'GET')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 4)
        self.assertEqual(connection.response.status_code, 200)

    def test_fetch_with_filter(self):
        """ GET /enterprises retrieve enterprises with filters """

        user = self.user
        enterprises = self.enterprises

        mock = MockUtils.create_mock_response(status_code=200, data=[enterprises[1]])

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects(filter=u"name == 'Enterprise 2'")

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-Filter'], u"name == 'Enterprise 2'")
        self.assertEqual(len(enterprises), 1)
        self.assertEqual(enterprises[0].name, u"Enterprise 2")

    def test_fetch_with_page(self):
        """ GET /enterprises retrieve enterprises with page """

        user = self.user
        enterprises = self.enterprises

        mock = MockUtils.create_mock_response(status_code=200, data=enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects(page=2)

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-Page'], 2)

    def test_fetch_all_should_not_raise_exception(self):
        """ GET /enterprises retrieve all enterprises should not raise exception """

        user = self.user
        enterprises = self.enterprises

        mock = MockUtils.create_mock_response(status_code=500, data=[], error=u"Internal error")

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')

        self.assertEqual(url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(method, u'GET')
        self.assertEqual(enterprises, None)
        self.assertEqual(connection.response.status_code, 500)

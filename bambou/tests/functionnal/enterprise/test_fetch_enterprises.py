# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests.utils import MockUtils
from bambou.tests.functionnal import start_session, get_valid_enterprise


class Fetch(TestCase):

    def setUp(self):
        self.user = start_session()
        self.enterprises = list()
        self.enterprises.append(get_valid_enterprise(id=1, name=u"Enterprise 1"))
        self.enterprises.append(get_valid_enterprise(id=2, name=u"Enterprise 2"))
        self.enterprises.append(get_valid_enterprise(id=3, name=u"Enterprise 3"))
        self.enterprises.append(get_valid_enterprise(id=4, name=u"Enterprise 4"))

    def tearDown(self):
        self.user = None
        self.enterprises = None

    def test_fetch_all(self):
        """ GET /enterprises fetch all enterprises """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')
        headers = MockUtils.get_mock_parameter(mock, 'headers')

        self.assertEqual(url, u'https://vsd:8443/nuage/api/v3_2/enterprises')
        self.assertEqual(method, u'GET')
        self.assertEqual(headers['Authorization'], u'XREST dXNlcjo1MWYzMTA0Mi1iMDQ3LTQ4Y2EtYTg4Yi02ODM2ODYwOGUzZGE=')
        self.assertEqual(headers['X-Nuage-Organization'], u'enterprise')
        self.assertEqual(headers['Content-Type'], u'application/json')

        self.assertEqual(fetcher, self.user.enterprises)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 4)
        self.assertEqual(connection.response.status_code, 200)

    def test_fetch_all_without_commit(self):
        """ GET /enterprises retrieve all enterprises without commit """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(commit=False)

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(len(enterprises), 4)
        self.assertEqual(len(self.user.enterprises), 0)


    def test_fetch_with_filter(self):
        """ GET /enterprises retrieve enterprises with filters """

        mock = MockUtils.create_mock_response(status_code=200, data=[self.enterprises[1]])

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(filter=u"name == 'Enterprise 2'")

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-Filter'], u"name == 'Enterprise 2'")
        self.assertEqual(len(enterprises), 1)
        self.assertEqual(enterprises[0].name, u"Enterprise 2")

    def test_fetch_with_group_by(self):
        """ GET /enterprises retrieve enterprises with group_by """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(group_by=['field1', 'field2'])

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-GroupBy'], 'true')
        self.assertEqual(headers['X-Nuage-Attributes'], 'field1, field2')

    def test_fetch_with_order_by(self):
        """ GET /enterprises retrieve enterprises with order_by """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(order_by='name ASC')

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-OrderBy'], 'name ASC')

    def test_fetch_with_page(self):
        """ GET /enterprises retrieve enterprises with page """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(page=2)

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-Page'], 2)

    def test_fetch_with_page_size(self):
        """ GET /enterprises retrieve enterprises with page size """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch(page_size=10)

        headers = MockUtils.get_mock_parameter(mock, 'headers')
        self.assertEqual(headers['X-Nuage-PageSize'], 10)

    def test_fetch_all_should_not_raise_exception(self):
        """ GET /enterprises retrieve all enterprises should not raise exception """

        mock = MockUtils.create_mock_response(status_code=500, data=[], error=u"Internal error")

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch()

        method = MockUtils.get_mock_parameter(mock, 'method')
        url = MockUtils.get_mock_parameter(mock, 'url')

        self.assertEqual(url, u'https://vsd:8443/nuage/api/v3_2/enterprises')
        self.assertEqual(method, u'GET')
        self.assertEqual(enterprises, None)
        self.assertEqual(connection.response.status_code, 500)

    def test_refetch_all(self):
        """ GET /enterprises refetch all enterprises """

        mock = MockUtils.create_mock_response(status_code=200, data=self.enterprises)

        with patch('requests.request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch()

            enterprise = self.user.enterprises[2]
            enterprise.name = u'This name should not appear because we will refetch everything!'

            (fetcher, user, enterprises, connection) = self.user.enterprises.fetch()

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(fetcher, self.user.enterprises)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 4)
        self.assertEqual(self.user.enterprises[2].name, "Enterprise 3")


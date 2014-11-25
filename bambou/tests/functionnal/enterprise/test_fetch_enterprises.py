# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests.functionnal import get_login_as_user, build_mock_response, get_mock_arg, get_valid_enterprise


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

        mock = build_mock_response(status_code=200, data=enterprises)

        with patch('bambou.NURESTObject.send_request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        request = get_mock_arg(mock, 'request')

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(request.method, u'GET')

        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 4)

    def test_fetch_with_filter(self):
        """ GET /enterprises retrieve enterprises with filters """

        user = self.user
        enterprises = self.enterprises

        mock = build_mock_response(status_code=200, data=[enterprises[1]])

        with patch('bambou.NURESTObject.send_request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects(filter=u"name == 'Enterprise 2'")

        request = get_mock_arg(mock, 'request')

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(request.method, u'GET')
        self.assertEqual(request.headers['X-Nuage-Filter'], u"name == 'Enterprise 2'")

        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 1)
        self.assertEqual(enterprises[0].name, u"Enterprise 2")

    def test_fetch_all_should_not_raise_exception(self):
        """ GET /enterprises retrieve all enterprises should not raise exception """

        user = self.user
        enterprises = self.enterprises

        mock = build_mock_response(status_code=500, data=[], error=u"Internal error")

        with patch('bambou.NURESTObject.send_request', mock):
            (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        request = get_mock_arg(mock, 'request')
        self.assertEqual(connection.response.status_code, 500)
        self.assertEqual(request.url, u'https://<host>:<port>/nuage/api/v3_0/enterprises')
        self.assertEqual(request.method, u'GET')

        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertEqual(enterprises, None)

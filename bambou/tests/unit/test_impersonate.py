# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou.tests import start_session
from bambou.tests.models import User
from bambou.tests.utils import MockUtils


class Impersonate(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_impersonate(self):
        """ GET /enterprises with impersonation

        """
        session = start_session()

        session.impersonate(username=u'johndoe', enterprise=u'enterprise')

        mock = MockUtils.create_mock_response(status_code=200, data=[])

        user = User()

        with patch('requests.request', mock):
            user.enterprises.fetch()

        headers = MockUtils.get_mock_parameter(mock=mock, name='headers')

        self.assertIn('X-Nuage-ProxyUser', headers)
        self.assertEquals(headers['X-Nuage-ProxyUser'], u'johndoe@enterprise')
        self.assertEquals(session.is_impersonating, True)

        session.stop_impersonate()
        self.assertEquals(session.is_impersonating, False)

        with patch('requests.request', mock):
            user.enterprises.fetch()

        headers = MockUtils.get_mock_parameter(mock=mock, name='headers')
        self.assertNotIn('X-Nuage-ProxyUser', headers)

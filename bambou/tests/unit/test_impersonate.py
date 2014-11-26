# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from bambou import NURESTLoginController
from bambou.tests import User
from bambou.tests.utils import MockUtils


class Impersonate(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_impersonate(self):
        """ GET /enterprises with impersonation """

        ctrl = NURESTLoginController()
        ctrl.user = u'christophe'
        ctrl.password = u'password'
        ctrl.url = u'http://www.google.fr'
        ctrl.api_key = u'12345'
        ctrl.enterprise = u'Alcatel'

        ctrl.impersonate(user=u'johndoe', enterprise=u'enterprise')

        mock = MockUtils.create_mock_response(status_code=200, data=[])

        user = User()

        with patch('requests.request', mock):
            user.enterprises_fetcher.fetch_objects()

        headers = MockUtils.get_mock_parameter(mock=mock, name='headers')

        self.assertIn('X-Nuage-ProxyUser', headers)
        self.assertEquals(headers['X-Nuage-ProxyUser'], u'johndoe@enterprise')

        ctrl.stop_impersonate()

        with patch('requests.request', mock):
            user.enterprises_fetcher.fetch_objects()

        headers = MockUtils.get_mock_parameter(mock=mock, name='headers')
        self.assertNotIn('X-Nuage-ProxyUser', headers)

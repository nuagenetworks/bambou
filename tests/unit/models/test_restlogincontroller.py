# -*- coding:utf-8 -*-

from unittest import TestCase

from restnuage.restlogincontroller import RESTLoginController


class LoginControllerSingleton(TestCase):

    def test_login_controller_is_singleton(self):
        """ login controller is singleton """
        ctrl_a = RESTLoginController(user=u'Christophe')
        ctrl_b = RESTLoginController(user=u'Toto')

        self.assertEquals(ctrl_a, ctrl_b)


class GetAuthenticationHeader(TestCase):

    def test_get_authentication_header_without_api_key(self):
        """ Get authentication header without api key """

        controller = RESTLoginController(user=u'christophe', password=u'tuCr0IsKoi?', api_key=None)

        header = controller.get_authentication_header()
        self.assertEquals(header, 'XREST Y2hyaXN0b3BoZTp0dUNyMElzS29pPw==')

    def test_get_authentication_header_with_api_key(self):
        """ Get authentication header with api key """

        controller = RESTLoginController(user=u'christophe', password=None, api_key=u'12345ABCD')

        header = controller.get_authentication_header()
        self.assertEquals(header, 'XREST Y2hyaXN0b3BoZTpOb25l')


class ResetLoginController(TestCase):

    def test_reset_login_controller(self):
        """ Reset login controller """

        controller = RESTLoginController(user=u'christophe', password=u'password', url=u'http://www.google.fr', api_key=u'12345', company=u'Alcatel')
        controller.reset()

        self.assertEquals(controller.user, None)
        self.assertEquals(controller.password, None)
        self.assertEquals(controller.url, None)
        self.assertEquals(controller.company, None)
        self.assertEquals(controller.api_key, None)


class ImpersonateLoginController(TestCase):

    def setUp(self):
        """ Set up the context """
        RESTLoginController(user=u'christophe', password=u'password', url=u'http://www.google.fr', api_key=u'12345', company=u'Alcatel')

    def tearDown(self):
        """ Cleaning context """
        ctrl = RESTLoginController()
        ctrl.reset()


    def test_impersonate(self):
        """ Start impersonate """

        controller = RESTLoginController()
        controller.impersonate(user=u'Alex', company=u'Google')

        self.assertEquals(controller.is_impersonating, True)
        self.assertEquals(controller.impersonation, 'Alex@Google')
        # TODO : Test notification

    def test_stop_impersonate(self):
        """ Stop impersonate """
        controller = RESTLoginController()
        controller.impersonate(user=u'Alex', company=u'Google')
        self.assertEquals(controller.is_impersonating, True)

        controller.stop_impersonate()
        self.assertEquals(controller.is_impersonating, False)
        self.assertEquals(controller.impersonation, None)
        # TODO : Test notification

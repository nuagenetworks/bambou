from unittest import TestCase
from mock import patch

from bambou import NURESTLoginController

class GetAuthenticationHeader(TestCase):

    def test_get_authentication_header_as_string(self):
        """ Get authentication header as string """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = 'password'
        controller.api_key = None

        self.assertEquals(controller.get_authentication_header() , 'XREST dXNlcm5hbWU6cGFzc3dvcmQ=')


    def test_get_authentication_header_as_unicode(self):
        """ Get authentication header as unicode """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = 'password'
        controller.api_key = None

        self.assertEquals(controller.get_authentication_header() , 'XREST dXNlcm5hbWU6cGFzc3dvcmQ=')

    def test_get_authentication_header_with_tilde(self):
        """ Get authentication header with tilde """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = 'p~ass~wor~d'
        controller.api_key = None

        self.assertEquals(controller.get_authentication_header() , 'XREST dXNlcm5hbWU6cH5hc3N+d29yfmQ=')

    def test_get_authentication_header_with_api_key(self):
        """ Get authentication header with api key """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = 'password'
        controller.api_key = '123456'

        self.assertEquals(controller.get_authentication_header() , 'XREST dXNlcm5hbWU6MTIzNDU2')

    def test_get_authentication_header_with_api_key_param(self):
        """ Get authentication header with api key parameter """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = 'password'
        controller.api_key = None

        self.assertEquals(controller.get_authentication_header(api_key='123456') , 'XREST dXNlcm5hbWU6MTIzNDU2')

    def test_get_authentication_header_with_api_key_param(self):
        """ Get authentication header with api key parameter """

        controller = NURESTLoginController()
        controller.user = 'username'
        controller.password = None
        controller.api_key = None

        self.assertEquals(controller.get_authentication_header(password='password') , 'XREST dXNlcm5hbWU6cGFzc3dvcmQ=')

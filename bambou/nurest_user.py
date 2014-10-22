# -*- coding: utf-8 -*-

from .nurest_connection import NURESTConnection
from .nurest_login_controller import NURESTLoginController
from .nurest_object import NURESTObject

from .utils import Sha1


class NURESTBasicUser(NURESTObject):
    """ Defines a basic user """

    _DEFAULT_USER = None

    def __init__(self):
        """ Initializes user """

        super(NURESTBasicUser, self).__init__()

        self._user_name = None
        self._password = None
        self._api_key = None

        self._new_password = None

        self.expose_attribute(local_name='user_name', remote_name='userName', attribute_type=str)
        self.expose_attribute(local_name='password', attribute_type=str)
        self.expose_attribute(local_name='api_key', remote_name='APIKey', attribute_type=str)

    # Properties

    def _get_user_name(self):
        """ Get user_name """
        return self._user_name

    def _set_user_name(self, user_name):
        """ Set user_name """
        self._user_name = user_name

    user_name = property(_get_user_name, _set_user_name)

    def _get_password(self):
        """ Get password """
        return self._password

    def _set_password(self, password):
        """ Set password """
        self._password = password

    password = property(_get_password, _set_password)

    def _get_api_key(self):
        """ Get API Key """
        return self._api_key

    def _set_api_key(self, api_key):
        """ Set API Key """
        self._api_key = api_key

    api_key = property(_get_api_key, _set_api_key)

    @classmethod
    def get_default_user(cls):
        """ Get default user """
        if not cls._DEFAULT_USER:
            NURESTBasicUser._DEFAULT_USER = cls()

        return NURESTBasicUser._DEFAULT_USER

    # Methods

    def prepare_change_password(self, new_password):
        """ Prepares password modification """

        self._new_password = new_password

    def save(self, callback=None):
        """ Updates the user and perform the callback method """

        if self._new_password:
            self.password = Sha1.encrypt(self._new_password)

        controller = NURESTLoginController()
        controller.password = self._new_password
        controller.api_key = None

        connection = NURESTConnection()
        connection.save(self, callback=self._did_save)

    def _did_save(self):
        """ Launched when save has been successfully executed """

        self._new_password = None
        controller = NURESTLoginController()
        controller.password = None
        controller.api_key = self.api_key

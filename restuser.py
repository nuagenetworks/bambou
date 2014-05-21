# -*- coding: utf-8 -*-

from restnuage.restconnection import RESTConnection
from restnuage.restlogincontroller import RESTLoginController
from restnuage.restobject import RESTObject

from restnuage.utils.singleton import Singleton


class RESTBasicUser(Singleton, RESTObject):
    """ Defines a basic user """

    def __init__(self, id=None,
                       username=None,
                       password=None,
                       api_key=None,
                       creation_date=None,
                       external_id=None,
                       local_id=None,
                       owner=None,
                       parent_id=None,
                       parent_type=None):
        """ Initializes user """

        super(RESTBasicUser, self).__init__(creation_date=creation_date,
                                         external_id=external_id,
                                         id=id,
                                         local_id=local_id,
                                         owner=owner,
                                         parent_id=parent_id,
                                         parent_type=parent_type)

        self._username = username
        self._password = password
        self._api_key = api_key

        self._new_password = None

        self.expose_attribute(attribute_name='username', rest_name='userName')
        self.expose_attribute(attribute_name='password')
        self.expose_attribute(attribute_name='api_key', rest_name='APIKey')

    # Properties

    def _get_username(self):
        """ Get username """
        return self._username

    def _set_username(self, username):
        """ Set username """
        self._username = username

    username = property(_get_username, _set_username)

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

    # Methods

    def prepare_change_password(self, new_password):
        """ Prepares password modification """

        self._new_password = new_password

    def save(self, callback=None):
        """ Updates the user and perform the callback method """

        if self._new_password:
            self.password = self._new_password

        controller = RESTLoginController()
        controller.password = self._new_password
        controller.api_key = None

        connection = RESTConnection()
        connection.save(self, callback=self._did_save)

    def _did_save(self):
        """ Launched when save has been successfully executed """

        self._new_password = None
        controller = RESTLoginController()
        controller.password = None
        controller.api_key = self.api_key

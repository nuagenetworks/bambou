# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""

from base64 import urlsafe_b64encode
from .utils.singleton import Singleton


class NURESTLoginController(Singleton):
    """ Singleton that holds information about the current user session """

    def __init__(self):
        """ Initiliazes the login controller """

        if not hasattr(self, '_initiliazed') or not self._initiliazed:
            self._initiliazed = True
            self._is_impersonating = False
            self._impersonation = None

            self._user = None
            self._password = None
            self._api_key = None
            self._enterprise = None
            self._url = None
            self._async = True

    def __str__(self):
        """ Prints information """

        return "[NURESTLoginController] user=%s enterprise=%s url=%s (API Key=%s)" % (self._user, self._enterprise, self._url, self._api_key)

    # Properties

    def _get_is_impersonating(self):
        """ Check if we are currently using impersonation

            Returns:
                Returns True if currently using impersonation
        """

        return self._is_impersonating

    is_impersonating = property(_get_is_impersonating, None)

    def _get_impersonation(self):
        """ Get impersonation information

            Returns:
                Returns string information about the impersonsation
        """
        return self._impersonation

    impersonation = property(_get_impersonation, None)

    def _get_user(self):
        """ Get the user name

            Returns:
                Returns the name of the user
        """

        return self._user

    def _set_user(self, user):
        """ Set the user name to connect with

            Args:
                user: name of the user
        """

        self._user = user

    user = property(_get_user, _set_user)

    def _get_password(self):
        """ Get user password

            Returns:
                Returns user password
        """

        return self._password

    def _set_password(self, password):
        """ Set user password to connect with

            Args:
                password: the password of the user
        """

        self._password = password

    password = property(_get_password, _set_password)

    def _get_api_key(self):
        """ Get API Key

            API Key is available when NURESTUser has been fetched.

            Returns:
                Returns the string containing the API Key
        """

        return self._api_key

    def _set_api_key(self, api_key):
        """ Set the API Key

            When set, the API key will be used to make all HTTP calls

            Args:
                api_key: the string that represents the API Key
        """

        self._api_key = api_key

    api_key = property(_get_api_key, _set_api_key)

    def _get_enterprise(self):
        """ Get the enterprise name

            Returns:
                Returns the name of the enterprise
        """

        return self._enterprise

    def _set_enterprise(self, enterprise):
        """ Set the enterprise name

            Args:
                enterprise: the name of the enterprise
        """

        self._enterprise = enterprise

    enterprise = property(_get_enterprise, _set_enterprise)

    def _get_url(self):
        """ Get API URL endpoint

            Returns:
                Returns the API URL endpoint
        """
        return self._url

    def _set_url(self, url):
        """ Set API URL endpoint

            Args:
                url: the url of the API endpoint
        """
        if url.endswith('/'):
            url = url[:-1]

        self._url = url

    url = property(_get_url, _set_url)

    def _get_async(self):
        """ Is asynchronous controller

            Returns:
                Returns True if the controller is asynchronous
        """

        return self._async

    def _set_async(self, async):
        """ Set asynchronous controller

            Args:
                async: Boolean to say whether or not the controller is async.
        """
        self._async = async

    async = property(_get_async, _set_async)

    # Methods

    def get_authentication_header(self, user=None, api_key=None, password=None):
        """ Return authenication string to place in Authorization Header

            If API Token is set, it'll be used. Otherwise, the clear
            text password will be sent. Users of NURESTLoginController are responsible to
            clean the password property.

            Returns:
                Returns the XREST Authentication string with API Key or user password encoded.
        """

        if user is None:
            user = self.user

        if api_key is None:
            api_key = self.api_key

        if password is None:
            password = self.password

        if api_key:
            return "XREST %s" % urlsafe_b64encode("%s:%s" % (user, api_key))

        return "XREST %s" % urlsafe_b64encode("%s:%s" % (user, password))

    def reset(self):
        """ Reset controller

            It removes all information about previous session
        """

        self._is_impersonating = False
        self._impersonation = None

        self.user = None
        self.password = None
        self.api_key = None
        self.enterprise = None
        self.url = None

    def impersonate(self, user, enterprise):
        """ Impersonate a user in a enterprise

            Args:
                user: the name of the user to impersonate
                enterprise: the name of the enterprise where to use impersonation
        """

        if not user or not enterprise:
            raise ValueError('You must set a user name and an enterprise name to begin impersonification')

        self._is_impersonating = True
        self._impersonation = "%s@%s" % (user, enterprise)

    def stop_impersonate(self):
        """ Stop impersonization """

        if self._is_impersonating:
            self._is_impersonating = False
            self._impersonation = None

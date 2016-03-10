# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from base64 import urlsafe_b64encode


class NURESTLoginController(object):
    """ Holds information about the current user session """

    def __init__(self):
        """ Initiliazes the login controller """

        if not hasattr(self, '_initiliazed') or not self._initiliazed:
            self._initiliazed = True
            self._is_impersonating = False
            self._impersonation = None

            self._certificate = None
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

    @property
    def is_impersonating(self):
        """ Check if we are currently using impersonation

            Returns:
                Returns True if currently using impersonation
        """

        return self._is_impersonating

    @property
    def impersonation(self):
        """ Get impersonation information

            Returns:
                Returns string information about the impersonsation
        """
        return self._impersonation

    @property
    def user(self):
        """ Get the user name

            Returns:
                Returns the name of the user
        """

        return self._user

    @user.setter
    def user(self, user):
        """ Set the user name to connect with

            Args:
                user: name of the user
        """

        self._user = user

    @property
    def password(self):
        """ Get user password

            Returns:
                Returns user password
        """

        return self._password

    @password.setter
    def password(self, password):
        """ Set user password to connect with

            Args:
                password: the password of the user
        """

        self._password = password

    @property
    def certificate(self):
        """ Get the certificate used for authentication

            Returns:
                Returns the certificate
        """
        return self._certificate

    @certificate.setter
    def certificate(self, certificate):
        """ Set certificate to connect with

            Args:
                certificate: the certificate
        """
        self._certificate = certificate

    @property
    def api_key(self):
        """ Get API Key

            API Key is available when root api has been fetched.

            Returns:
                Returns the string containing the API Key
        """

        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """ Set the API Key

            When set, the API key will be used to make all HTTP calls

            Args:
                api_key: the string that represents the API Key
        """

        self._api_key = api_key

    @property
    def enterprise(self):
        """ Get the enterprise name

            Returns:
                Returns the name of the enterprise
        """

        return self._enterprise

    @enterprise.setter
    def enterprise(self, enterprise):
        """ Set the enterprise name

            Args:
                enterprise: the name of the enterprise
        """

        self._enterprise = enterprise

    @property
    def url(self):
        """ Get API URL endpoint

            Returns:
                Returns the API URL endpoint
        """
        return self._url

    @url.setter
    def url(self, url):
        """ Set API URL endpoint

            Args:
                url: the url of the API endpoint
        """
        if url and url.endswith('/'):
            url = url[:-1]

        self._url = url

    @property
    def async(self):
        """ Is asynchronous controller

            Returns:
                Returns True if the controller is asynchronous
        """

        return self._async

    @async.setter
    def async(self, async):
        """ Set asynchronous controller

            Args:
                async: Boolean to say whether or not the controller is async.
        """
        self._async = async

    # Methods

    def get_authentication_header(self, user=None, api_key=None, password=None, certificate=None):
        """ Return authenication string to place in Authorization Header

            If API Token is set, it'll be used. Otherwise, the clear
            text password will be sent. Users of NURESTLoginController are responsible to
            clean the password property.

            Returns:
                Returns the XREST Authentication string with API Key or user password encoded.
        """

        if not user:
            user = self.user

        if not api_key:
            api_key = self.api_key

        if not password:
            password = self.password

        if not password:
            password = self.password

        if not certificate:
            certificate = self._certificate

        if certificate:
            return "XREST %s" % urlsafe_b64encode("%s:%s" % (user, ""))

        if api_key:
            return "XREST %s" % urlsafe_b64encode("%s:%s" % (user, api_key))

        if isinstance(password, unicode):
            password = password.encode("utf-8")

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

    def equals(self, controller):
        """ Verify if the controller corresponds
            to the current one.

        """
        if controller is None:
            return False

        return self.user == controller.user and self.enterprise == controller.enterprise and self.url == controller.url

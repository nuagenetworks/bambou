# -*- coding: utf-8 -*-

from base64 import urlsafe_b64encode

from .utils.singleton import Singleton


class NURESTLoginController(Singleton):

    def __init__(self):
        """ Initiliazes NURESTLoginController """

        if not hasattr(self, '_initiliazed') or not self._initiliazed: # TODO : Clean here
            self._initiliazed = True
            self._is_impersonating = False
            self._impersonation = None

            self._user = u"csproot"
            self._password = u"csproot"
            self._api_key = None
            self._enterprise = u"csp"
            self._url = u"https://135.227.220.152:8443/nuage/api/v1_0"
            self._async = True

    def __str__(self):
        """ Prints NURESTLoginController information """

        return "%s user=%s enterprise=%s url=%s " % (self.__class__, self._user, self._enterprise, self._url)

    # Properties

    def _get_is_impersonating(self):
        """ Getter for _is_impersonating """
        return self._is_impersonating

    is_impersonating = property(_get_is_impersonating, None)

    def _get_impersonation(self):
        """ Get impersonation string """
        return self._impersonation

    impersonation = property(_get_impersonation, None)

    def _get_user(self):
        """ Get user """

        return self._user

    def _set_user(self, user):
        """ Set user """

        self._user = user

    user = property(_get_user, _set_user)

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

    def _get_enterprise(self):
        """ Get enterprise """
        return self._enterprise

    def _set_enterprise(self, enterprise):
        """ Set enterprise """
        self._enterprise = enterprise

    enterprise = property(_get_enterprise, _set_enterprise)

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set enterprise """
        self._url = url

    url = property(_get_url, _set_url)

    def _get_async(self):
        """ Get async """
        return self._async

    def _set_async(self, async):
        """ Set async """
        self._async = async

    async = property(_get_async, _set_async)

    # Methods

    def get_authentication_header(self, user=None, api_key=None, password=None):
        """ Return authenication string to place in Authorization Header
            If API Token is set, it'll be used. Otherwise, the clear
            text password will be sent. Users of NURESTLoginController are responsible to
            clean the password property.
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
        """ Reset all """

        self._is_impersonating = False
        self._impersonation = None

        self.user = None
        self.password = None
        self.api_key = None
        self.enterprise = None
        self.url = None

    def impersonate(self, user, enterprise):
        """ Impersonate a user in a enterprise """

        if not user or not enterprise:
            raise ValueError('You must set a user name and an enterprise name to begin impersonification')

        self._is_impersonating = True
        self._impersonation = "%s@%s" % (user, enterprise)

        # TODO : Restart Push Notification

    def stop_impersonate(self):
        """ Stop impersonization """

        if self._is_impersonating:
            self._is_impersonating = False
            self._impersonation = None

        # TODO : Restart Push Notification

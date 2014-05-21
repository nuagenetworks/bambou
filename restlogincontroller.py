# -*- coding: utf-8 -*-

from base64 import urlsafe_b64encode

from restnuage.utils.singleton import Singleton


class RESTLoginController(Singleton):

    def __init__(self):
        """ Initiliazes RESTLoginController """

        if not hasattr(self, '_initiliazed') or not self._initiliazed: # TODO : Clean here
            self._initiliazed = True
            self._is_impersonating = False
            self._impersonation = None

            self._user = u"csproot"
            self._password = u"csproot"
            self._api_key = None
            self._company = u"csp"
            self._url = u"https://135.227.220.152:8443/nuage/api/v1_0"

    def __str__(self):
        """ Prints RESTLoginController information """

        return "%s user=%s company=%s url=%s " % (self.__class__, self._user, self._company, self._url)

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
        print "Setting user to %s " % user
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

    def _get_company(self):
        """ Get company """
        return self._company

    def _set_company(self, company):
        """ Set company """
        self._company = company

    company = property(_get_company, _set_company)

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set company """
        self._url = url

    url = property(_get_url, _set_url)

    # Methods

    def get_authentication_header(self):
        """ Return authenication string to place in Authorization Header
            If API Token is set, it'll be used. Otherwise, the clear
            text password will be sent. Users of RESTLoginController are responsible to
            clean the password property.
        """

        if self.api_key:
            print "Authentication for user %s with api_key %s" % (self.user, self.api_key)
            return "XREST %s" % urlsafe_b64encode("%s:%s" % (self.user, self.api_key))

        print "Authentication for user %s with password %s" % (self.user, self.password)
        return "XREST %s" % urlsafe_b64encode("%s:%s" % (self.user, self.password))

    def reset(self):
        """ Reset all """

        self._is_impersonating = False
        self._impersonation = None

        self.user = None
        self.password = None
        self.api_key = None
        self.company = None
        self.url = None

    def impersonate(self, user, company):
        """ Impersonate a user in a company """

        if not user or not company:
            raise ValueError('You must set a user name and an enterprise name to begin impersonification')

        self._is_impersonating = True
        self._impersonation = "%s@%s" % (user, company)

        # TODO : Restart Push Notification

    def stop_impersonate(self):
        """ Stop impersonization """

        if self._is_impersonating:
            self._is_impersonating = False
            self._impersonation = None

        # TODO : Restart Push Notification

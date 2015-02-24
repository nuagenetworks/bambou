
# -*- coding: utf-8 -*-

# Copyright 2014 Alcatel-Lucent USA Inc.

from .nurest_login_controller import NURESTLoginController
from peak import context
from bambou import bambou_logger
from contextlib import contextmanager
import inspect


class NURESTSession(object):

    """ Authenticated sessions used for sending ReST calls

        The session holds the credential information for a particular
        user. It is used by :class:`bambou.NURESTConnection` to get
        the authentication information needed to send the request.

        NURESTSession supports the `with` statetement.

        Note:
            NURESTSession *must* be subclassed, and the subclass *must* implement :class:`bambou.NURESTSession.create_rest_user`

        Example:
            >>> mainsession =  NUMySession(username="csproot", password="csproot", enterprise="csp", api_url="https://vsd:8443", version="3.2")
            >>> mainsession.start()
            >>> mainsession.user.entities.get()
            [<NUEntity at 1>, <NUEntity at 2>, <NUEntity at 3>]

            >>> with NUMySession(username="user", password="password", enterprise="ent", api_url="https://vsd:8443", version="3.2") as session:
            >>>     session.user.entities.get()
            [<NUEntity at 2>]
    """

    def __init__(self, username, password, enterprise, api_url, version):
        """ Initializes a new sesssion

            Args:
                username (string): the username
                password (string): the password
                enterprise (string): the enterprise
                api_url (string): the url to the api
                version (string): the version of the api to target

            Example:
                >>> mainsession =  NUMySession(username="csproot", password="csproot", enterprise="csp", api_url="https://vsd:8443", version="3.2")

        """
        self._user = None

        self._login_controller = NURESTLoginController()
        self._login_controller.user = username
        self._login_controller.password = password
        self._login_controller.user_name = username
        self._login_controller.enterprise = enterprise
        self._login_controller.url = '%s/nuage/api/v%s' % (api_url, str(version).replace('.', '_'))

    # Class Methods

    @classmethod
    def get_current_session(cls):
        """
            Get the current session

            Returns:
                (bambou.NURESTSession): the current session

        """
        return _NURESTSessionCurrentContext.session

    # Properties

    @property
    def login_controller(self):
        """
            Returns the :class:`bambou.NURESTLoginController` of the current session

            Note:
                You should not need to use this method. It's used automatically when needed
        """
        return self._login_controller

    @property
    def user(self):
        """
            Returns the user of the session

            Returns:
                (bambou.NURESTBasicUser): the REST user
        """
        return self._user

    @property
    def is_impersonating(self):
        """ Returns True if the session is currently impersonating
            a user

            Returns:
                (bool): a boolean that indicate if the session is impersonating a user

        """
        return self._login_controller.is_impersonating

    # Methods

    def create_rest_user(self):
        """
            Create a :class:`bambou.NURESTBasicUser`.

            This method *MUST* be overriden by subclasses in order to provide
            a valid :class:`bambou.NURESTBasicUser`.

            Returns:
                A instance of a subclass of :class:`bambou.NURESTBasicUser`
        """
        raise NotImplementedError('%s must define method def create_rest_user(self).' % self)

    def _authenticate(self):

        if self._user is None:
            self._user = self.create_rest_user()
            self._user.fetch()

        self.login_controller.api_key = self._user.api_key
        bambou_logger.debug("[NURESTSession] Started session with username %s in enterprise %s" % (self.login_controller._user, self.login_controller.enterprise))

    def start(self):
        """
            Starts the session.

            Starting the session will actually get the API key of the current user
        """
        callee = inspect.getouterframes(inspect.currentframe())[1][4][0]

        if callee.lstrip().startswith("with "):  # Cases 'with','\twith'. Check with other Python versions
            return _NURESTSessionContext.new(self)
        else:
            _NURESTSessionCurrentContext.session = self
            self._authenticate()
            return self

    def reset(self):
        """
            Stops the session.

            Stopping the session will reset the API stored API key. Subsequent calls will need to start it again
        """

        self._user = None
        self.login_controller.reset()

    def impersonate(self, username, enterprise):
        """
            Change the session to impersonate a user within an enterprise

            Args:
                username (string): name of the user to impersonate
                enterprise (string): name of the enterprise
        """
        self._login_controller.impersonate(username, enterprise)

    def stop_impersonate(self):
        """
            Stop impersonating a user

        """
        self._login_controller.stop_impersonate()


class _NURESTSessionContext (object):

    session = None

    @classmethod
    @contextmanager
    def new(self, session):
        with _NURESTSessionCurrentContext.new() as context:
            context.session = session
            session._authenticate()
            yield session


class _NURESTSessionCurrentContext (context.Service):

    session = None

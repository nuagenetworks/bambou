
# -*- coding: utf-8 -*-

# Copyright 2014 Alcatel-Lucent USA Inc.

from .nurest_login_controller import NURESTLoginController
from peak.context import Service, manager
from bambou import bambou_logger

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
            >>>     mainsession.user.entities.get()
            [<NUEntity at 2>]
    """

    def __init__(self, username, password, enterprise, api_url):

        self._user = None

        self._login_controller = NURESTLoginController()
        self._login_controller.user = username
        self._login_controller.password = password
        self._login_controller.user_name = username
        self._login_controller.enterprise = enterprise
        self._login_controller.url = api_url
        self._started = False


    # Contexts

    def __enter__(self):
        _NURESTSessionCurrentContext.new()
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        pass

    # Class Methods

    def create_rest_user(self):
        """
            Create a :class:`bambou.NURESTBasicUser`.

            This method *MUST* be overriden by subclasses in order to provide
            a valid :class:`bambou.NURESTBasicUser`.

            Returns:
                A instance of a subclass of :class:`bambou.NURESTBasicUser`
        """
        raise NotImplementedError('%s must define method def create_rest_user(self).' % self)

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


    def start(self):
        """
            Starts the session.

            Starting the session will actually get the API key of the current user
        """

        if self._started:
            return;

        self._started = True;

        _NURESTSessionCurrentContext.session = self

        if self._login_controller.api_key is not None:
            bambou_logger.warn("[NURESTSession] Previous session has not been terminated.\
                            Please call stop() on your previous VSD Session to stop it properly")
            return

        if self._user is None:
            self._user = self.create_rest_user()
            self._user.fetch()

        self._login_controller.api_key = self._user.api_key
        bambou_logger.debug("[NURESTSession] Started session with username %s in enterprise %s (key=%s)" % (self._login_controller._user,\
                    self._login_controller.password, self.user.api_key))

    def stop(self):
        """
            Stops the session.

            Stopping the session will reset the API stored API key. Subsequent calls will need to start it again
        """
        if not self._started:
            return;

        self._started = False;
        self._login_controller.api_key = None



class _NURESTSessionCurrentContext (Service):

    session = None

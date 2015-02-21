
# -*- coding: utf-8 -*-

# Copyright 2014 Alcatel-Lucent USA Inc.

from .nurest_login_controller import NURESTLoginController
from peak.context import Service, manager
from bambou import bambou_logger

class NURESTSession(object):

    """ REST User Session

        Session can be started and stopped whenever its needed
    """

    def __init__(self, username, password, enterprise, api_url):
        """
            @todo
        """

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
        raise NotImplementedError('%s must define method def create_rest_user(self).' % self)

    # Properties

    @property
    def login_controller(self):
        """
            @TODO
        """
        return self._login_controller

    @property
    def user(self):
        """
            @todo
        """
        return self._user


    def start(self):
        """
            @todo
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
            @TODO
        """
        if not self._started:
            return;

        self._started = False;
        self._login_controller.api_key = None



class _NURESTSessionCurrentContext (Service):

    session = None



_NURESTSessionCurrentContext.new()

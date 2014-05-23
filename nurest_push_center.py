# -*- coding: utf-8 -*-

from restnuage.nurest_connection import NURESTConnection
from restnuage.nurest_request import NURESTRequest
from utils.singleton import Singleton


class NURESTPushCenter(Singleton):
    """
        Wait for push notifications
    """

    def __init__(self, url):
        """ Initialiez push """
        self._url = url
        self._is_running = False
        self._current_connection = None

    # Properties

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set url """
        self._url = url

    url = property(_get_url, _set_url)

    # Control Methods

    def start(self):
        """ """
        pass

    def stop(self):
        """ """
        pass

    # Private methods

    def _did_receive_event(self, connection):
        """ Receive an event from connection """

        raise NotImplementedError('Missing implementation in NURESTPushCenter')

    def _listen(self, uuid):
        """ Listen a connection uuid """

        events_url = "%s/events" % self.url
        if uuid:
            events_url = "%s?%s" % (events_url, uuid)

        request = NURESTRequest(method='GET', url=events_url)

        connection = NURESTConnection(request=request, callback=self._did_receive_event)
        connection.timeout = 0
        connection.ignore_request_idle = True
        connection.start()

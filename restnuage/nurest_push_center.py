# -*- coding: utf-8 -*-

import threading

from .nurest_connection import NURESTConnection
from .nurest_request import NURESTRequest
from .utils.singleton import Singleton
from restnuage import restnuage_log

class NURESTPushCenter(Singleton):
    """
        Wait for push notifications
    """

    def __init__(self):
        """ Initialiez push """
        self._url = ''
        self._is_running = False
        self._current_connection = None
        self._last_events = list()
        self.nb_events_received = 0
        self.nb_push_received = 0
        self._thread = None

    # Properties

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set url """
        self._url = url

    url = property(_get_url, _set_url)

    # Control Methods

    def start(self, max_event_loop=0):
        """ Start push center """
        if self._is_running:
            return

        self._max_event_loop = max_event_loop
        self._is_running = True
        self._thread = threading.Thread(target=self._listen, name='push-center')
        self._thread.start()

    def stop(self):
        """ """
        if not self._is_running:
            return

        self._is_running = False
        self._thread = None
        self._current_connection = None

    def wait_until_exit(self):
        """ Wait until thread exit """

        if self._max_event_loop == 0:
            raise Exception("Thread will never exit. Use stop or specify max_event_loop when starting it!")

        self._thread.join()
        self.stop()

    # Events

    def get_last_events(self):
        """ Retrieve events that has been  """

        events = self._last_events
        self._last_events = list()
        restnuage_log.info("%s last events " % len(events))
        return events

    # Private methods

    def _did_receive_event(self, connection):
        """ Receive an event from connection """

        response = connection.response

        if response.status_code != 200:
            restnuage_log.info("** NURESTPushCenter: Connection failure URL=%s Error: [%s] %s" % (self._url, response.status_code, response.reason))
            return

        data = response.data

        if data:
            self.nb_events_received += len(data['events'])
            self.nb_push_received += 1

            restnuage_log.info("** NURESTPushCenter\nReceived Push=%s\nTotal Received events=%s" % (self.nb_push_received, self.nb_events_received))
            self._last_events.extend(data['events'])

        if self._is_running and (self._max_event_loop == 0 or self._max_event_loop > self.nb_push_received):
            print "Another round !"
            uuid = None
            if 'uuid' in data:
                uuid = data['uuid']

            self._listen(uuid)

    def _listen(self, uuid=None):
        """ Listen a connection uuid """

        restnuage_log.info("** NURESTPushCenter listening in %s" % threading.current_thread())

        events_url = "%s/events" % self.url
        if uuid:
            events_url = "%s?uuid=%s" % (events_url, uuid)

        request = NURESTRequest(method='GET', url=events_url)

        # Force async to False so the push center will have only 1 thread running
        connection = NURESTConnection(request=request, callback=self._did_receive_event, async=False)
        #connection.timeout = 0
        #connection.ignore_request_idle = True
        connection.start()

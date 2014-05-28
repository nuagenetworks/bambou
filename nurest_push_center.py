# -*- coding: utf-8 -*-

import threading

from restnuage.nurest_connection import NURESTConnection
from restnuage.nurest_request import NURESTRequest
from utils.singleton import Singleton


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
        self._debug_number_of_received_events = 0
        self._debug_number_of_received_push = 0
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

    def start(self):
        """ Start push center """
        if self._is_running:
            return

        self._is_running = True
        self._thread = threading.Thread(target=self._listen, name='push-center')
        self._thread.start()

    def stop(self):
        """ """
        if not self._is_running:
            return

        print "** NURESTPushCenter is stopping after %s push received and %s events " % (self._debug_number_of_received_push, self._debug_number_of_received_events)
        self._is_running = False
        self._thread = None
        self._current_connection = None

    def get_last_events(self):
        """ Retrieve events that has been  """
        events = self._last_events
        self._last_events = list()
        print "%s last events " % len(events)
        return events

    # Private methods

    def _did_receive_event(self, connection):
        """ Receive an event from connection """

        if not self._is_running:
            return

        print "** NURESTPushCenter received data"
        response = connection.response

        if response.status_code != 200:
            print "** NURESTPushCenter: Connection failure URL=%s Error: [%s] %s" % (self._url, response.status_code, response.reason)
            return

        data = response.data

        if data:
            self._debug_number_of_received_events += len(data['events'])
            self._debug_number_of_received_push += 1

            print "** NURESTPushCenter\nReceived Push=%s\nTotal Received events=%s" % (self._debug_number_of_received_push, self._debug_number_of_received_events)

            self._last_events.extend(data['events'])

        if self._is_running:
            uuid = None
            if 'uuid' in data:
                uuid = data['uuid']

            self._listen(uuid)

    def _listen(self, uuid=None):
        """ Listen a connection uuid """

        print "** NURESTPushCenter listening in %s" % threading.current_thread()

        events_url = "%s/events" % self.url
        if uuid:
            events_url = "%s?%s" % (events_url, uuid)

        request = NURESTRequest(method='GET', url=events_url)

        # Force async to False so the push center will have only 1 thread running
        connection = NURESTConnection(request=request, callback=self._did_receive_event, async=False)

        #connection.timeout = 0
        #connection.ignore_request_idle = True
        connection.start()

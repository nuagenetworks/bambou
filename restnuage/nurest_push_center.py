# -*- coding: utf-8 -*-

import json
import logging

pushcenter_log = logging.getLogger('pushcenter')

import threading

from time import time

from .nurest_connection import NURESTConnection
from .nurest_request import NURESTRequest


class NURESTPushCenter(object):
    """
        Wait for push notifications
    """

    _DEFAULT_INSTANCE = None

    def __init__(self):
        """ Initialiez push """
        self._url = ''
        self._is_running = False
        self._current_connection = None
        self._last_events = list()
        self.nb_events_received = 0
        self.nb_push_received = 0
        self._thread = None
        self._user = None
        self._start_time = None
        self._timeout = None
        self._delegate_methods = list()

    @classmethod
    def get_default_instance(cls):
        """ Get default push center """
        if not cls._DEFAULT_INSTANCE:
            NURESTPushCenter._DEFAULT_INSTANCE = cls()

        return NURESTPushCenter._DEFAULT_INSTANCE

    # Properties

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set url """
        self._url = url

    url = property(_get_url, _set_url)

    # Control Methods

    def start(self, timeout=None, user=None):
        """ Start push center """

        if self._is_running:
            return

        if timeout:
            self._timeout = timeout
            self._start_time = int(time())

        pushcenter_log.debug("NURESTPushCenter is starting...")
        self._is_running = True
        self._user = user
        self._thread = threading.Thread(target=self._listen, name='push-center')
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """ Stop the current thread """

        if not self._is_running:
            return

        pushcenter_log.debug("NURESTPushCenter is stopping...")

        self._is_running = False
        self._thread = None
        self._current_connection = None
        self._start_time = None
        self._timeout = None

    def wait_until_exit(self):
        """ Wait until thread exit """

        if self._timeout is None:
            raise Exception("Thread will never exit. Use stop or specify timeout when starting it!")

        self._thread.join()
        self.stop()

    # Events

    def get_last_events(self):
        """ Retrieve events that has been  """

        events = self._last_events
        self._last_events = list()
        return events

    # Private methods

    def _did_receive_event(self, connection):
        """ Receive an event from connection """

        if not self._is_running:
            return

        if connection.has_timeouted:
            return

        response = connection.response

        if response.status_code != 200:
            pushcenter_log.error("NURESTPushCenter: Connection failure on %s.\nError: [%s] %s\nConnection with user %s" % (response.errors, response.status_code, response.reason, connection.user.user_name))
            return

        data = response.data

        if len(self._delegate_methods) > 0:
            for m in self._delegate_methods:
                m(data)
        elif data:
            events = data['events']
            self.nb_events_received += len(events)
            self.nb_push_received += 1

            pushcenter_log.info("NURESTPushCenter Received Push #%s (total=%s, latest=%s)\n%s" % (self.nb_push_received, self.nb_events_received, len(events), json.dumps(events, indent=4)))
            self._last_events.extend(events)

        if self._is_running:
            uuid = None
            if 'uuid' in data:
                uuid = data['uuid']

            self._listen(uuid)

    def _listen(self, uuid=None):
        """ Listen a connection uuid """

        events_url = "%s/events" % self.url
        if uuid:
            events_url = "%s?uuid=%s" % (events_url, uuid)

        request = NURESTRequest(method='GET', url=events_url)

        # Force async to False so the push center will have only 1 thread running
        connection = NURESTConnection(request=request, callback=self._did_receive_event, async=False, user=self._user)

        if self._timeout:
            if int(time()) - self._start_time >= self._timeout:
                pushcenter_log.debug("NURESTPushCenter has timeout (timeout=%ss)." % self._timeout)
                return

            else:
                connection.timeout = self._timeout

        pushcenter_log.info('RESTNuage Sending >>>>>>\n%s %s' % (request.method, request.url))

        #connection.ignore_request_idle = True
        connection.start()

    def add_delegate(self, callback):
        """
        Registers a new delegate
        The prototype should be function(data), where data will be the decoded json push
        """
        if callback in self._delegate_methods:
            return

        self._delegate_methods.append(callback)

    def remove_delegate(self, callback):
        """
        Removes a delegate
        The prototype should be function(data), where data will be the decoded json push
        """
        if not callback in self._delegate_methods:
            return

        self._delegate_methods.remove(callback)

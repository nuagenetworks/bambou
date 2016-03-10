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


import json
import threading

from time import time

from .nurest_connection import NURESTConnection
from .nurest_request import NURESTRequest

from bambou import pushcenter_logger


class StoppableThread(threading.Thread):
    """ Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition.
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class NURESTPushCenter(object):
    """ Push center wait for push notifications.

        It has to listen a specific URL.

        Every time a notification is send, it will automatically get it
        and store it into get_last_events method.
    """

    def __init__(self):
        """ Initialize push center """

        self._url = None
        self._is_running = False
        self._current_connection = None
        self._last_events = list()
        self.nb_events_received = 0
        self.nb_push_received = 0
        self._thread = None
        self._root_object = None
        self._start_time = None
        self._timeout = None
        self._delegate_methods = list()

    # Properties

    @property
    def url(self):
        """ Get url """

        return self._url

    @url.setter
    def url(self, url):
        """ Set url """

        self._url = url

    @property
    def is_running(self):
        """ Get is_running """

        return self._is_running

    # Control Methods

    def start(self, timeout=None, root_object=None):
        """ Starts listening to events.

            Args:
                timeout (int): number of seconds before timeout. Used for testing purpose only.
                root_object (bambou.NURESTRootObject): NURESTRootObject object that is listening. Used for testing purpose only.
        """

        if self._is_running:
            return

        if timeout:
            self._timeout = timeout
            self._start_time = int(time())

        pushcenter_logger.debug("[NURESTPushCenter] Starting push center on url %s ..." % self.url)
        self._is_running = True
        self.__root_object = root_object

        from .nurest_session import NURESTSession
        current_session = NURESTSession.get_current_session()
        args_session = {'session': current_session}

        self._thread = StoppableThread(target=self._listen, name='push-center', kwargs=args_session)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """ Stops listening for events. """

        if not self._is_running:
            return

        pushcenter_logger.debug("[NURESTPushCenter] Stopping...")

        self._thread.stop()
        self._thread.join()

        self._is_running = False
        self._current_connection = None
        self._start_time = None
        self._timeout = None

    def wait_until_exit(self):
        """ Wait until thread exit

            Used for testing purpose only
        """

        if self._timeout is None:
            raise Exception("Thread will never exit. Use stop or specify timeout when starting it!")

        self._thread.join()
        self.stop()

    # Events

    def get_last_events(self):
        """ Retrieve events that has been

            Returns:
                Returns a list of events and flush existing events.
        """

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
        data = None

        if response.status_code != 200:
            pushcenter_logger.error("[NURESTPushCenter]: Connection failure [%s] %s" % (response.status_code, response.errors))

        else:
            data = response.data

            if len(self._delegate_methods) > 0:
                for m in self._delegate_methods:
                    try:
                        m(data)
                    except Exception as exc:
                        pushcenter_logger.error("[NURESTPushCenter] Delegate method %s failed:\n%s" % (m, exc))
            elif data:
                events = data['events']
                self.nb_events_received += len(events)
                self.nb_push_received += 1

                pushcenter_logger.info("[NURESTPushCenter] Received Push #%s (total=%s, latest=%s)\n%s" % (self.nb_push_received, self.nb_events_received, len(events), json.dumps(events, indent=4)))
                self._last_events.extend(events)

        if self._is_running:
            uuid = None
            if data and 'uuid' in data:
                uuid = data['uuid']

            self._listen(uuid)

    def _listen(self, uuid=None, session=None):
        """ Listen a connection uuid """
        if session:
            from .nurest_session import _NURESTSessionCurrentContext
            _NURESTSessionCurrentContext.session = session

        if self.url is None:
            raise Exception("NURESTPushCenter needs to have a valid URL. please use setURL: before starting it.")

        events_url = "%s/events" % self.url
        if uuid:
            events_url = "%s?uuid=%s" % (events_url, uuid)

        request = NURESTRequest(method='GET', url=events_url)

        # Force async to False so the push center will have only 1 thread running
        connection = NURESTConnection(request=request, async=True, callback=self._did_receive_event, root_object=self._root_object)

        if self._timeout:
            if int(time()) - self._start_time >= self._timeout:
                pushcenter_logger.debug("[NURESTPushCenter] Timeout (timeout=%ss)." % self._timeout)
                return

            else:
                connection.timeout = self._timeout

        pushcenter_logger.info('Bambou Sending >>>>>>\n%s %s' % (request.method, request.url))

        # connection.ignore_request_idle = True
        connection.start()

    def add_delegate(self, callback):
        """ Registers a new delegate callback

            The prototype should be function(data), where data will be the decoded json push

            Args:
                callback (function): method to trigger when push center receives events
        """

        if callback in self._delegate_methods:
            return

        self._delegate_methods.append(callback)

    def remove_delegate(self, callback):
        """ Unregisters a registered delegate function or a method.

            Args:
                callback(function): method to trigger when push center receives events
        """

        if callback not in self._delegate_methods:
            return

        self._delegate_methods.remove(callback)

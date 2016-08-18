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
import requests
import threading
import uuid
import logging

from .nurest_response import NURESTResponse

from bambou import bambou_logger


HTTP_CODE_ZERO = 0
HTTP_CODE_SUCCESS = 200
HTTP_CODE_CREATED = 201
HTTP_CODE_EMPTY = 204
HTTP_CODE_MULTIPLE_CHOICES = 300
HTTP_CODE_BAD_REQUEST = 400
HTTP_CODE_UNAUTHORIZED = 401
HTTP_CODE_PERMISSION_DENIED = 403
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_METHOD_NOT_ALLOWED = 405
HTTP_CODE_CONNECTION_TIMEOUT = 408
HTTP_CODE_CONFLICT = 409
HTTP_CODE_PRECONDITION_FAILED = 412
HTTP_CODE_AUTHENTICATION_EXPIRED = 419
HTTP_CODE_INTERNAL_SERVER_ERROR = 500
HTTP_CODE_SERVICE_UNAVAILABLE = 503


HTTP_METHOD_HEAD = 'HEAD'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_GET = 'GET'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'


class NURESTConnection(object):
    """ Connection that enable HTTP requests """

    def __init__(self, request, async, callback=None, callbacks=dict(), root_object=None):
        """ Intializes a new connection for a given request

            NURESTConnection object is in charge of the HTTP call. It relies on request library

            Args:
                request: the NURESTRequest to send
                callback: the method that will be fired after sending
                callbacks: a dictionary of user callbacks. Should contains local and remote callbacks
        """

        self._uses_authentication = True
        self._has_timeouted = False
        # self._is_cancelled = False
        self._ignore_request_idle = False
        self._xhr_timeout = 3000
        self._response = None
        self._error_message = None
        self._transaction_id = uuid.uuid4().hex

        self._request = request
        self._async = async
        self._callback = callback
        self._callbacks = callbacks
        self._user_info = None
        self._object_last_action_timer = None
        self._root_object = root_object

    # Properties

    @property
    def callbacks(self):
        """ Get callbacks

            Returns:
                It returns an array containing user callbacks
        """

        return self._callbacks

    @property
    def request(self):
        """ Get request. Read-only property

            Returns:
                Returns the NURESTRequest object
        """

        return self._request

    @property
    def transaction_id(self):
        """ Get transaction ID. Read-only property

            Returns:
                Returns the transaction ID
        """

        return self._transaction_id

    @property
    def response(self):
        """ Get response

            Returns:
                It returns the NURESTResponse object of the request
        """

        return self._response

    @response.setter
    def response(self, response):
        """ Set response

            Args:
                response: the NURESTResponse object

        """

        self._response = response

    @property
    def user_info(self):
        """ Get user info

            Returns:
                It returns additionnal user information
        """

        return self._user_info

    @user_info.setter
    def user_info(self, info):
        """ Set user info

            Args:
                info: Information to carry
        """

        self._user_info = info

    @property
    def timeout(self):
        """ Get timeout

            Returns:
                It returns the timeout time in seconds. Default is 3000.
        """

        return self._xhr_timeout

    @timeout.setter
    def timeout(self, timeout):
        """ Set timeout

            Args:
                timeout: Number of seconds before timeout
        """

        self._xhr_timeout = timeout

    @property
    def ignore_request_idle(self):
        """ Get ignore request idle

            Returns:
                It returns a boolean. By default ignore request idle is set to False.
        """

        return self._ignore_request_idle

    @ignore_request_idle.setter
    def ignore_request_idle(self, ignore):
        """ Set ignore request idle

            Args:
                ignore: boolean to ignore request idle
        """

        self._ignore_request_idle = ignore

    @property
    def has_timeouted(self):
        """ Get has timouted

            Returns:
                Returns True if the request has timeout.
        """

        return self._has_timeouted

    @property
    def async(self):
        """ Get async

            Returns:
                Returns True if the request is asynchronous
        """

        return self._async

    # Methods

    def has_succeed(self):
        """ Check if the connection has succeed

            Returns:
                Returns True if connection has succeed.
                False otherwise.

        """
        status_code = self._response.status_code

        if status_code in [HTTP_CODE_ZERO, HTTP_CODE_SUCCESS, HTTP_CODE_CREATED, HTTP_CODE_EMPTY, HTTP_CODE_MULTIPLE_CHOICES]:
            return True

        if status_code in [HTTP_CODE_BAD_REQUEST, HTTP_CODE_UNAUTHORIZED, HTTP_CODE_PERMISSION_DENIED, HTTP_CODE_NOT_FOUND, HTTP_CODE_METHOD_NOT_ALLOWED, HTTP_CODE_CONNECTION_TIMEOUT, HTTP_CODE_CONFLICT, HTTP_CODE_PRECONDITION_FAILED, HTTP_CODE_INTERNAL_SERVER_ERROR, HTTP_CODE_SERVICE_UNAVAILABLE]:
            return False

        raise Exception('Unknown status code %s.', status_code)

    def has_callbacks(self):
        """  Check if the request has callbacks

            Returns:
                Returns YES if there is a local or remote callbacks
        """

        return len(self._callbacks) > 0

    def handle_response_for_connection(self, should_post=False):
        """ Check if the response succeed or not.

            In case of error, this method also print messages and set
            an array of errors in the response object.

            Returns:
                Returns True if the response has succeed, False otherwise
        """

        status_code = self._response.status_code
        data = self._response.data

        # TODO : Get errors in response data after bug fix : http://mvjira.mv.usa.alcatel.com/browse/VSD-2735
        if data and 'errors' in data:
            self._response.errors = data['errors']

        if status_code in [HTTP_CODE_SUCCESS, HTTP_CODE_CREATED, HTTP_CODE_EMPTY]:
            return True

        if status_code == HTTP_CODE_MULTIPLE_CHOICES:
            return False

        if status_code in [HTTP_CODE_PERMISSION_DENIED, HTTP_CODE_UNAUTHORIZED]:

            if not should_post:
                return True

            return False

        if status_code in [HTTP_CODE_CONFLICT, HTTP_CODE_NOT_FOUND, HTTP_CODE_BAD_REQUEST, HTTP_CODE_METHOD_NOT_ALLOWED, HTTP_CODE_PRECONDITION_FAILED, HTTP_CODE_SERVICE_UNAVAILABLE]:
            if not should_post:
                return True

            return False

        if status_code == HTTP_CODE_INTERNAL_SERVER_ERROR:

            return False

        if status_code == HTTP_CODE_ZERO:
            bambou_logger.error("NURESTConnection: Connection error with code 0. Sending NUNURESTConnectionFailureNotification notification and exiting.")
            return False

        bambou_logger.error("NURESTConnection: Report this error, because this should not happen: %s" % self._response)
        return False

    # HTTP Calls

    def _did_receive_response(self, response):
        """ Called when a response is received """

        try:
            data = response.json()

        except:
            data = None

        self._response = NURESTResponse(status_code=response.status_code, headers=response.headers, data=data, reason=response.reason)

        level = logging.WARNING if self._response.status_code >= 300 else logging.DEBUG

        bambou_logger.info('< %s %s %s [%s] ' % (self._request.method, self._request.url, self._request.params if self._request.params else "", self._response.status_code))
        bambou_logger.log(level, '< headers: %s' % self._response.headers)
        bambou_logger.log(level, '< data:\n%s' % json.dumps(self._response.data, indent=4))

        self._callback(self)

        return self

    def _did_timeout(self):
        """ Called when a resquest has timeout """

        bambou_logger.debug('Bambou %s on %s has timeout (timeout=%ss)..' % (self._request.method, self._request.url, self.timeout))
        self._has_timeouted = True

        if self.async:
            self._callback(self)
        else:
            return self

    def _make_request(self, session=None):
        """ Make a synchronous request """

        from .nurest_session import _NURESTSessionCurrentContext
        _NURESTSessionCurrentContext.session = session

        self._has_timeouted = False

        # Add specific headers
        controller = session.login_controller

        enterprise = controller.enterprise
        user_name = controller.user
        api_key = controller.api_key
        certificate = controller.certificate

        if self._root_object:
            enterprise = self._root_object.enterprise_name
            user_name = self._root_object.user_name
            api_key = self._root_object.api_key

        if self._uses_authentication:
            self._request.set_header('X-Nuage-Organization', enterprise)
            self._request.set_header('Authorization', controller.get_authentication_header(user_name, api_key))

        if controller.is_impersonating:
            self._request.set_header('X-Nuage-ProxyUser', controller.impersonation)

        headers = self._request.headers
        data = json.dumps(self._request.data)

        bambou_logger.info('> %s %s %s' % (self._request.method, self._request.url, self._request.params if self._request.params else ""))
        bambou_logger.debug('> headers: %s' % headers)
        bambou_logger.debug('> data:\n  %s' % json.dumps(self._request.data, indent=4))

        response = self.__make_request(method=self._request.method, url=self._request.url, params=self._request.params, data=data, headers=headers, certificate=certificate)

        retry_request = False

        if response.status_code == HTTP_CODE_MULTIPLE_CHOICES:
            self._request.url += '?responseChoice=1'
            bambou_logger.debug('Bambou got [%s] response. Trying to force response choice' % HTTP_CODE_MULTIPLE_CHOICES)
            retry_request = True

        elif response.status_code == HTTP_CODE_AUTHENTICATION_EXPIRED and _NURESTSessionCurrentContext.session:
            bambou_logger.debug('Bambou got [%s] response . Trying to reconnect your session that has expired' % HTTP_CODE_AUTHENTICATION_EXPIRED)
            _NURESTSessionCurrentContext.session.reset()
            _NURESTSessionCurrentContext.session.start()
            retry_request = True

        if retry_request:
            response = self.__make_request(method=self._request.method, url=self._request.url, params=self._request.params, data=data, headers=headers, certificate=certificate)

        return self._did_receive_response(response)

    def __make_request(self, method, url, params, data, headers, certificate):
        """ Encapsulate requests call
        """
        verify = False
        timeout = self.timeout

        try:  # TODO : Remove this ugly try/except after fixing Java issue: http://mvjira.mv.usa.alcatel.com/browse/VSD-546
            response = requests.request(method=method,
                                        url=url,
                                        data=data,
                                        headers=headers,
                                        verify=verify,
                                        timeout=timeout,
                                        params=params,
                                        cert=certificate)
        except requests.exceptions.SSLError:
            try:
                response = requests.request(method=method,
                                            url=url,
                                            data=data,
                                            headers=headers,
                                            verify=verify,
                                            timeout=timeout,
                                            params=params,
                                            cert=certificate)
            except requests.exceptions.Timeout:
                return self._did_timeout()

        except requests.exceptions.Timeout:
            return self._did_timeout()

        return response

    def start(self):
        """ Make an HTTP request with a specific method """

        # TODO : Use Timeout here and _ignore_request_idle
        from .nurest_session import NURESTSession
        session = NURESTSession.get_current_session()

        if self.async:
            thread = threading.Thread(target=self._make_request, kwargs={'session': session})
            thread.is_daemon = False
            thread.start()
            return self.transaction_id

        return self._make_request(session=session)

    def reset(self):
        """ Reset the connection

        """
        self._request = None
        self._response = None
        self._transaction_id = uuid.uuid4().hex

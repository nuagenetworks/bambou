# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""

import json
import requests
import threading

from .nurest_login_controller import NURESTLoginController
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
HTTP_CODE_INTERNAL_SERVER_ERROR = 500
HTTP_CODE_SERVICE_UNAVAILABLE = 503


HTTP_METHOD_HEAD = 'HEAD'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_GET = 'GET'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'


class NURESTConnection(object):
    """ Connection that enable HTTP requests """

    def __init__(self, request, async, callback=None, callbacks=dict(), user=None):
        """ Intializes a new connection for a given request

            NURESTConnection object is in charge of the HTTP call. It relies on request library

            Args:
                request: the NURESTRequest to send
                async: A boolean to explain whether or not the call has to be made asynchronously
                callback: the method that will be fired after sending
                callbacks: a dictionary of user callbacks. Should contains local and remote callbacks
        """

        self._uses_authentication = True
        self._has_timeouted = False
        #self._is_cancelled = False
        self._ignore_request_idle = False
        self._xhr_timeout = 3000
        self._response = None
        self._error_message = None

        self._request = request
        self._async = async
        self._response = None
        self._callback = callback
        self._callbacks = callbacks
        self._user_info = None
        self._object_last_action_timer = None
        self._user = user

    # Properties

    def _get_callbacks(self):
        """ Get callbacks

            Returns:
                It returns an array containing user callbacks
        """

        return self._callbacks

    callbacks = property(_get_callbacks, None)

    def _get_response(self):
        """ Get response

            Returns:
                It returns the NURESTResponse object of the request
        """

        return self._response

    response = property(_get_response, None)

    def _get_user_info(self):
        """ Get user info

            Returns:
                It returns additionnal user information
        """

        return self._user_info

    def _set_user_info(self, info):
        """ Set user info

            Args:
                info: Information to carry
        """

        self._user_info = info

    user_info = property(_get_user_info, _set_user_info)

    def _get_timeout(self):
        """ Get timeout

            Returns:
                It returns the timeout time in seconds. Default is 3000.
        """

        return self._xhr_timeout

    def _set_timeout(self, timeout):
        """ Set timeout

            Args:
                timeout: Number of seconds before timeout
        """

        self._xhr_timeout = timeout

    timeout = property(_get_timeout, _set_timeout)

    def _get_ignore_request_idle(self):
        """ Get ignore request idle

            Returns:
                It returns a boolean. By default ignore request idle is set to False.
        """

        return self._ignore_request_idle

    def _set_ignore_request_idle(self, ignore):
        """ Set ignore request idle

            Args:
                ignore: boolean to ignore request idle
        """

        self._ignore_request_idle = ignore

    ignore_request_idle = property(_get_ignore_request_idle, _set_ignore_request_idle)

    def _has_timeouted(self):
        """ Get has timouted

            Returns:
                Returns True if the request has timeout.
        """

        return self._has_timeouted

    has_timeouted = property(_has_timeouted, None)

    def _get_async(self):
        """ Get async

            Returns:
                Returns True if the request is asynchronous
        """

        return self._async

    def _set_async(self, async):
        """ Set async

            Args:
                async: boolean to make asynchronous http request
        """

        self._async = async

    async = property(_get_async, None)

    # Methods

    def has_callbacks(self):
        """  Check if the request has callbacks

            Returns:
                Returns YES if there is a local or remote callbacks
        """

        return len(self._callbacks) > 0

    def has_response_success(self, should_post=False):
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
            self._print_information()
            return False

        if status_code in [HTTP_CODE_PERMISSION_DENIED, HTTP_CODE_UNAUTHORIZED]:

            if not should_post:
                return True

            self._print_information()
            return False

        if status_code in [HTTP_CODE_CONFLICT, HTTP_CODE_NOT_FOUND, HTTP_CODE_BAD_REQUEST, HTTP_CODE_METHOD_NOT_ALLOWED, HTTP_CODE_PRECONDITION_FAILED, HTTP_CODE_SERVICE_UNAVAILABLE]:
            if not should_post:
                return True

            self._print_information()
            return False

        if status_code == HTTP_CODE_INTERNAL_SERVER_ERROR:

            self._print_information()
            return False

        if status_code == HTTP_CODE_ZERO:
            bambou_logger.error("NURESTConnection: Connection error with code 0. Sending NUNURESTConnectionFailureNotification notification and exiting.")
            self._print_information()
            return False

        bambou_logger.error("NURESTConnection: Report this error, because this should not happen: %s" % self._response)
        return False

    def _print_information(self):
        """ Prints information instead of sending a confirmation """

        if len(self._response.errors) == 0:
            bambou_logger.error("NURESTConnection ERROR without error message [%s] %s" % (self._response.status_code, self._response.reason))

        else:
            bambou_logger.error("NURESTConnection (%s %s) ERROR %s:\n%s" % (self._request.method, self._request.url, self._response.status_code, json.dumps(self._response.errors, indent=4)))

    # HTTP Calls

    def _did_receive_response(self, response):
        """ Called when a response is received """

        try:
            data = response.json()

        except:
            data = None

        self._response = NURESTResponse(status_code=response.status_code, headers=response.headers, data=data, reason=response.reason)
        self._callback(self)

        return self

    def _did_timeout(self):
        """ Called when a resquest has timeout """

        bambou_logger.debug('Bambou %s on %s has timeout (timeout=%ss)..' % (self._request.method, self._request.url, self.timeout))
        self._has_timeouted = True

        if self._async and self._callback:
            self._callback(self)
        else:
            return self

    def _make_request(self):
        """ Make a synchronous request """

        self._has_timeouted = False

        # Add specific headers
        controller = NURESTLoginController()

        enterprise = controller.enterprise
        user_name = controller.user
        api_key = controller.api_key

        if self._user:
            enterprise = self._user.enterprise_name
            user_name = self._user.user_name
            api_key = self._user.api_key

        bambou_logger.debug('Bambou has been sent with user:%s within enterprise:%s (Key=%s)' % (user_name, enterprise, api_key))

        if self._uses_authentication:
            self._request.set_header('X-Nuage-Organization', enterprise)
            self._request.set_header('Authorization', controller.get_authentication_header(user_name, api_key))

        if controller.is_impersonating:
            self._request.set_header('X-Nuage-Proxy', controller.impersonation)

        headers = self._request.get_headers()

        try:  # TODO : Remove this ugly try/except after fixing Java issue: http://mvjira.mv.usa.alcatel.com/browse/VSD-546
            response = requests.request(method=self._request.method,
                                      url=self._request.url,
                                      data=json.dumps(self._request.data),
                                      headers=headers,
                                      verify=False,
                                      timeout=self.timeout)
        except requests.exceptions.SSLError:
            try:
                response = requests.request(method=self._request.method,
                                          url=self._request.url,
                                          data=json.dumps(self._request.data),
                                          headers=headers,
                                          verify=False,
                                          timeout=self.timeout)
            except requests.exceptions.Timeout:
                return self._did_timeout()

        except requests.exceptions.Timeout:
            return self._did_timeout()

        return self._did_receive_response(response)

    def start(self):
        """ Make an HTTP request with a specific method """

        # TODO : Use Timeout here and _ignore_request_idle
        if self._async:
            thread = threading.Thread(target=self._make_request)
            thread.is_daemon = False
            thread.start()

            return

        return self._make_request()

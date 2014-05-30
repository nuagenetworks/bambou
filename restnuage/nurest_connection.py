# -*- coding: utf-8 -*-

import json
import requests
import threading

from .nurest_login_controller import NURESTLoginController
from .nurest_response import NURESTResponse


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


class NURESTConnection(object):
    """ Enhances requests """

    def __init__(self, request, async, callback=None, callbacks=dict()):
        """ Intializes a new connection for a request
            :param request: the NURESTRequest to send
            :param callback: the method that will be fired after sending
            :param callbacks: a dictionary of user callbacks. Should contains local and remote callbacks
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

    # Properties

    def _get_callbacks(self):
        """ Get callbacks """
        return self._callbacks

    callbacks = property(_get_callbacks, None)

    def _get_response(self):
        """ Get response """
        return self._response

    response = property(_get_response, None)

    def _get_user_info(self):
        """ Get user info """
        return self._user_info

    def _set_user_info(self, info):
        """ Set user info """
        self._user_info = info

    user_info = property(_get_user_info, _set_user_info)

    def _get_timeout(self):
        """ Get timeout """
        return self._xhr_timeout

    def _set_timeout(self, timeout):
        """ Set timeout """
        self._xhr_timeout = timeout

    timeout = property(_get_timeout, _set_timeout)

    def _get_ignore_request_idle(self):
        """ Get ignore request idle """
        return self._ignore_request_idle

    def _set_ignore_request_idle(self, timeout):
        """ Set ignore request idle """
        self._ignore_request_idle = timeout

    ignore_request_idle = property(_get_ignore_request_idle, _set_ignore_request_idle)

    def _has_timeouted(self):
        """ Get has timouted """
        return self._has_timeouted

    has_timeouted = property(_has_timeouted, None)

    def _get_async(self):
        """ Get async """
        return self._async

    def _set_async(self, async):
        """ Set async """
        self._async = async

    async = property(_get_async, None)

    # Methods

    def has_callbacks(self):
        """ Returns YES if there is a local or remote callbacks """

        return len(self._callbacks) > 0

    def has_response_success(self, should_post=False):
        """ Return True if the response has succeed, False otherwise """

        status_code = self._response.status_code

        data = self._response.data

        error_property = None
        error_name = None
        error_description = None

        # TODO : Get errors in response data after bug fix : http://mvjira.mv.usa.alcatel.com/browse/VSD-2735
        if data and 'errors' in data:
            error_property = data['errors'][0]['property']
            error_name = data['errors'][0]['descriptions'][0]['title']
            error_description = data['errors'][0]['descriptions'][0]['description']

        if status_code in [HTTP_CODE_SUCCESS, HTTP_CODE_CREATED, HTTP_CODE_EMPTY]:
            return True

        if status_code == HTTP_CODE_MULTIPLE_CHOICES:
            self._print_information(error_property, error_name, error_description)
            return False

        if status_code in [HTTP_CODE_PERMISSION_DENIED, HTTP_CODE_UNAUTHORIZED]:

            if not should_post:
                return True

            error_name = "Permission denied"
            error_description = "You are not allowed to access this resource."

            self._print_information(error_property, error_name, error_description)
            return False

        if status_code in [HTTP_CODE_CONFLICT, HTTP_CODE_NOT_FOUND, HTTP_CODE_BAD_REQUEST, HTTP_CODE_METHOD_NOT_ALLOWED, HTTP_CODE_PRECONDITION_FAILED, HTTP_CODE_SERVICE_UNAVAILABLE]:
            if not should_post:
                return True

            self._print_information(error_property, error_name, error_description)
            return False

        if status_code == HTTP_CODE_INTERNAL_SERVER_ERROR:

            error_name = "[CRITICAL] Internal Server Error"
            error_description = "Please check the log and report this error to the server team"

            self._print_information(error_property, error_name, error_description)
            return False

        if status_code == HTTP_CODE_ZERO:
            print "NURESTConnection: Connection error with code 0. Sending NUNURESTConnectionFailureNotification notification and exiting."
            self._print_information(error_property, error_name, error_description)
            return False

        print "NURESTConnection: Report this error, because this should not happen: %s" % self._response
        return False

    def _print_information(self, error_property, error_name, error_description):
        """ Prints information instead of sending a confirmation """

        print "NURESTConnection ERROR on [%s] %s, %s" % (error_property, error_name, error_description)

    # HTTP Calls

    def _did_receive_response(self, response):
        """ Called when a response is received """

        try:
            data = response.json()
        except:
            print "** Reponse could not be decoded\n%s\n** End response\n" % response.text
            data = None

        self._response = NURESTResponse(status_code=response.status_code, headers=response.headers, data=data, reason=response.reason)
        self._callback(self)

        return self

    def _did_timeout(self):
        """ Called when a resquest has timeout """
        print "TIMEOUT"
        self._has_timeouted = True

        if self._async and self._callback:
            self._callback(self)
        else:
            return self

        # TODO : Translate this line:
        #[[CPRunLoop currentRunLoop] limitDateForMode:CPDefaultRunLoopMode];

    def _make_request(self):
        """ make an asyn request """

        self._has_timeouted = False

        # Add specific headers
        controller = NURESTLoginController()

        if self._uses_authentication:
            self._request.set_header('X-Nuage-Organization', controller.enterprise)
            self._request.set_header('Authorization', controller.get_authentication_header())

        if controller.is_impersonating:
            self._request.set_header('X-Nuage-Proxy', controller.impersonation)

        headers = self._request.get_headers()

        url = "%s%s" % (controller.url, self._request.url)

        print "** Launch %s %s" % (self._request.method, url)

        response = requests.request(method=self._request.method,
                                  url=url,
                                  data=json.dumps(self._request.data),
                                  headers=headers,
                                  verify=False,
                                  timeout=self.timeout)

        return self._did_receive_response(response)

    def start(self):  # TODO : Use Timeout here and _ignore_request_idle
        """ Make an HTTP request with a specific method """

        if self._async:
            thread = threading.Thread(target=self._make_request)
            thread.is_daemon = False
            thread.start()

            return

        return self._make_request()

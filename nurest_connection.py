# -*- coding: utf-8 -*-

import requests

from requests_futures.sessions import FuturesSession

from restnuage.http_exceptions import HTTPTimeoutException
from restnuage.nurest_login_controller import NURESTLoginController


HTTP_CODE_ZERO = 0
HTTP_CODE_CONNECTION_TIMEOUT = 43
HTTP_CODE_SUCCESS = 200
HTTP_CODE_CREATED = 201
HTTP_CODE_EMPTY = 204
HTTP_CODE_MULTIPLE_CHOICES = 300
HTTP_CODE_BAD_REQUEST = 400
HTTP_CODE_UNAUTHORIZED = 401
HTTP_CODE_PERMISSION_DENIED = 403
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_METHOD_NOT_ALLOWED = 405
HTTP_CODE_CONFLICT = 409
HTTP_CODE_PRECONDITION_FAILED = 412
HTTP_CODE_INTERNAL_SERVER_ERROR = 500
HTTP_CODE_SERVICE_UNAVAILABLE = 503


class NURESTConnection(object):
    """ Enhances requests """

    def __init__(self):
        """ Intializes a new connection for a request """

        self._uses_authentication = True
        self._has_timeouted = False
        self._is_cancelled = False
        self._ignore_request_idle = False
        self._xhr_timeout = 300000
        self._response = None
        self._error_message = None
        self._callback = None

    # Properties

    # Methods

    def _is_response_success(self, response, should_post=False):
        """ Return True if the response has succeed, False otherwise """

        status_code = response.status_code
        print response.text
        # TODO : Get errors in response data after bug fix : http://mvjira.mv.usa.alcatel.com/browse/VSD-2735
        # data = response.json()[0]
        # print "Data = %s" % data
        #
        # if 'errors' in data:
        #     error_name = data['errors'][0]['description'][0]['title'] if contains_info else None
        #     error_description = data['errors'][0]['description'][0]['description'] if contains_info else None

        # TODO : Remove following temporary error message
        error_name = response.status_code
        error_description = response.reason

        if status_code in [HTTP_CODE_SUCCESS, HTTP_CODE_CREATED, HTTP_CODE_EMPTY]:
            return True

        if status_code == HTTP_CODE_MULTIPLE_CHOICES:
            self._print_information(error_name, error_description)
            return False

        if status_code in [HTTP_CODE_PERMISSION_DENIED, HTTP_CODE_UNAUTHORIZED]:

            if not should_post:
                return True

            error_name = "Permission denied"
            error_description = "You are not allowed to access this resource."

            self._print_information(error_name, error_description)
            return False

        if status_code in [HTTP_CODE_CONFLICT, HTTP_CODE_NOT_FOUND, HTTP_CODE_BAD_REQUEST, HTTP_CODE_METHOD_NOT_ALLOWED, HTTP_CODE_PRECONDITION_FAILED, HTTP_CODE_SERVICE_UNAVAILABLE]:
            if not should_post:
                return True

            self._print_information(error_name, error_description)
            return False

        if status_code == HTTP_CODE_INTERNAL_SERVER_ERROR:

            error_name = "[CRITICAL] Internal Server Error"
            error_description = "Please check the log and report this error to the server team"

            self._print_information(error_name, error_description)
            return False

        if status_code == HTTP_CODE_ZERO:
            print "NURESTConnection: Connection error with code 0. Sending NUNURESTConnectionFailureNotification notification and exiting."
            self._print_information(error_name, error_description)
            return False

        print "NURESTConnection: Report this error, because this should not happen: [%s] %s" % (status_code, response.data)
        return False

    def _print_information(self, error_name, error_description):
        """ Prints information instead of sending a confirmation """

        print "Response information:\n%s\n%s" % (error_name, error_description)

    def _get_base_url(self):
        """ Retrieve base url """

        controller = NURESTLoginController()
        return controller.url

    def _get_headers(self, filter=None, page=None, order_by=None):
        """ Prepare headers to send """

        headers = dict()
        headers['Content-Type'] = 'application/json'

        controller = NURESTLoginController()

        if self._uses_authentication:
            headers['X-Nuage-Organization'] = controller.company
            headers['Authorization'] = controller.get_authentication_header()

        if controller.is_impersonating:
            headers['X-Nuage-Proxy'] = controller.impersonation

        if filter:
            headers['X-Nuage-Filter'] = filter

        if page:
            headers['X-Nuage-Page'] = page

        if order_by:
            headers['X-Nuage-OrderBy'] = order_by

        print "**HEADERS"
        print headers

        return headers

    # HTTP Calls

    def _did_receive_response(self, session, response):
        """ Called when a response is received """

        print "Receive response"

        # Si pas de callback => Shouldpost = True
        if self._is_response_success(response) and self._callback:
            self._callback(response)
            self._callback = None

    def _did_timeout(self):
        """ Called when a resquest has timeout """

        self._has_timeouted = True
        raise HTTPTimeoutException()

    def get(self, resource_url, params=None, callback=None, filter=None, page=None, order_by=None):
        """ Make a GET request to retrieve data """

        self._make_request(method='GET',
                           resource_url=resource_url,
                           params=params,
                           callback=callback,
                           filter=filter,
                           page=page,
                           order_by=order_by)

    def create(self, resource_url, data=None, callback=None, filter=None, page=None, order_by=None):
        """ Make a POST request to create object """

        self._make_request(method='POST',
                           resource_url=resource_url,
                           data=data,
                           callback=callback,
                           filter=filter,
                           page=page,
                           order_by=order_by)

    def save(self, resource_url, data=None, callback=None, filter=None, page=None, order_by=None):
        """ Make a PUT request to create object """

        self._make_request(method='PUT',
                           resource_url=resource_url,
                           data=data,
                           callback=callback,
                           filter=filter,
                           page=page,
                           order_by=order_by)


    def delete(self, resource_url, callback=None, filter=None, page=None, order_by=None):
        """ Make a POST request to create object """

        self._make_request(method='DELETE',
                           resource_url=resource_url,
                           callback=callback,
                           filter=filter,
                           page=page,
                           order_by=order_by)


    def _make_request(self, method, resource_url, params=None, data=None, callback=None, filter=None, page=None, order_by=None):
        """ Make an HTTP request with a specific method """

        headers = self._get_headers(filter=filter, page=page, order_by=order_by)

        url = "%s%s" % (self._get_base_url(), resource_url)

        # Prepare callback
        self._callback = callback
        self._has_timeouted = False
        print "** Launch %s %s" %  (method, url)

        # HTTP Call
        session = FuturesSession()
        promise = session.request(method=method,
                                  url=url,
                                  params=params,
                                  data=data,
                                  headers=headers,
                                  verify=False,
                                  background_callback=self._did_receive_response,
                                  timeout=self._xhr_timeout)

        print "[%s] Waiting for response..." % method

        try:
            promise.result()
        except requests.exceptions.SSLError:
            self._did_timeout()

# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""


class NURESTRequest(object):

    """ Request that will be fired by the NURESTConnection """

    def __init__(self, method, url, data=None, params=None, filter=None, page=None, order_by=None):
        """ Initializes a request """

        self._method = method
        self._url = url
        self._data = data
        self._params = params
        self._headers = dict()

        self.set_header('Content-Type', 'application/json')

        if filter:
            self.set_header('X-Nuage-Filter', filter)

        if page:
            self.set_header('X-Nuage-Page', page)

        if order_by:
            self.set_header('X-Nuage-OrderBy', order_by)

    def __str__(self):
        """ Print request """

        return "%s %s" % (self.method, self.url)

    # Properties

    def _get_method(self):
        """ Get method """
        return self._method

    def _set_method(self, method):
        """ Set method """
        self._method = method

    method = property(_get_method, _set_method)

    def _get_url(self):
        """ Get url """
        return self._url

    def _set_url(self, url):
        """ Set url """
        self._url = url

    url = property(_get_url, _set_url)

    def _get_data(self):
        """ Get data """
        return self._data

    def _set_data(self, data):
        """ Set data """
        self._data = data

    data = property(_get_data, _set_data)

    def _get_params(self):
        """ Get url """
        return self._params

    def _set_params(self, params):
        """ Set params """
        self._params = params

    params = property(_get_params, _set_params)

    # Methods

    def get_headers(self):
        """ Prepare headers to send """

        return self._headers

    def set_header(self, header, value):
        """ Set header value """

        self._headers[header] = value

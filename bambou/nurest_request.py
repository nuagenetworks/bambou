# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.
#
# This source code contains confidential information which is proprietary to Alcatel.
# No part of its contents may be used, copied, disclosed or conveyed to any party
# in any manner whatsoever without prior written permission from Alcatel.
#
# Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.



class NURESTRequest(object):
    """ Request that will be send via the connection """

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

    @property
    def method(self):
        """ Get method """

        return self._method

    @method.setter
    def method(self, method):
        """ Set method """

        self._method = method

    @property
    def url(self):
        """ Get url """

        return self._url

    @url.setter
    def url(self, url):
        """ Set url """

        self._url = url

    @property
    def data(self):
        """ Get data """

        return self._data

    @data.setter
    def data(self, data):
        """ Set data """

        self._data = data

    @property
    def params(self):
        """ Get url """

        return self._params

    @params.setter
    def params(self, params):
        """ Set params """

        self._params = params

    @property
    def headers(self):
        """ Prepare headers to send """

        return self._headers

    @headers.setter
    def headers(self, value):
        """ Set header value """

        self._headers = value

    def set_header(self, header, value):
        """ Set header value """

        self._headers[header] = value


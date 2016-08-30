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
            self.set_header('X-Nuage-Page', str(page))

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
        # requests>=2.11 only accepts `str` or `bytes` header values
        # raising an exception here, instead of leaving it to `requests` makes
        # it easy to know where we passed a wrong header type in the code.
        if isinstance(value, unicode):
            # FIXME: this is very python 2.x specific, it needs to be changed
            # when making bambou python 3.x compliant.
            value = value.encode()
        elif not isinstance(value, (str, bytes)):
            raise TypeError("header values must be str or bytes, but %s value has type %s" % (header, type(value)))
        self._headers[header] = value

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

from .nurest_connection import HTTP_METHOD_PUT, HTTP_METHOD_GET
from .nurest_request import NURESTRequest
from .nurest_object import NURESTObject
from .nurest_session import _NURESTSessionCurrentContext

from .utils import Sha1


class NURESTRootObject(NURESTObject):
    """ NURESTRootObject defines a user that can log in.

        Only one NURESTRootObject can be connected at a time.
    """

    __default_root_object = None

    def __init__(self):
        """ Initializes user """

        super(NURESTRootObject, self).__init__()

        self._api_url = None
        self._new_password = None

        self._user_name = None
        self._password = None
        self._api_key = None

        self.expose_attribute(local_name='user_name', remote_name='userName', attribute_type=str)
        self.expose_attribute(local_name='password', attribute_type=str)
        self.expose_attribute(local_name='api_key', remote_name='APIKey', attribute_type=str)

    # Properties

    @property
    def user_name(self):
        """ Get user_name """

        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """ Set user_name """

        self._user_name = user_name

    @property
    def password(self):
        """ Get password """

        return self._password

    @password.setter
    def password(self, password):
        """ Set password """

        self._password = password

    @property
    def api_key(self):
        """ Get API Key """

        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """ Set API Key """

        self._api_key = api_key

    # Class Methods

    @classmethod
    def get_default_root_object(cls):
        """ Get default user """

        if not cls.__default_root_object:
            NURESTRootObject.__default_root_object = cls()

        return NURESTRootObject.__default_root_object

    # Methods

    def get_resource_url_for_child_type(self, nurest_object_type):
        """ Get the resource url for the nurest_object type """
        return "%s/%s" % (self.rest_base_url(), nurest_object_type.resource_name)

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.resource_name
        url = self.__class__.rest_base_url()

        return "%s/%s" % (url, name)

    def prepare_change_password(self, new_password):
        """ Prepares password modification """

        self._new_password = new_password

    def save(self, async=False, callback=None, encrypted=True):
        """ Updates the user and perform the callback method """

        if self._new_password and encrypted:
            self.password = Sha1.encrypt(self._new_password)

        controller = _NURESTSessionCurrentContext.session.login_controller
        controller.password = self._new_password
        controller.api_key = None

        data = json.dumps(self.to_dict())
        request = NURESTRequest(method=HTTP_METHOD_PUT, url=self.get_resource_url(), data=data)

        if async:
            return self.send_request(request=request, async=async, local_callback=self._did_save, remote_callback=callback)
        else:
            connection = self.send_request(request=request)
            return self._did_save(connection)

    def _did_save(self, connection):
        """ Launched when save has been successfully executed """

        self._new_password = None

        controller = _NURESTSessionCurrentContext.session.login_controller
        controller.password = None
        controller.api_key = self.api_key

        if connection.async:
            callback = connection.callbacks['remote']

            if connection.user_info:
                callback(connection.user_info, connection)
            else:
                callback(self, connection)
        else:
            return (self, connection)

    def fetch(self, async=False, callback=None):
        """ Fetch all information about the current object

            Args:
                async (bool): Boolean to make an asynchronous call. Default is False
                callback (function): Callback method that will be triggered in case of asynchronous call

            Returns:
                tuple: (current_fetcher, callee_parent, fetched_bjects, connection)

            Example:
                >>> entity = NUEntity(id="xxx-xxx-xxx-xxx")
                >>> entity.fetch() # will get the entity with id "xxx-xxx-xxx-xxx"
                >>> print entity.name
                "My Entity"
        """
        request = NURESTRequest(method=HTTP_METHOD_GET, url=self.get_resource_url())

        if async:
            return self.send_request(request=request, async=async, local_callback=self._did_fetch, remote_callback=callback)
        else:
            connection = self.send_request(request=request)
            return self._did_retrieve(connection)

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

from time import time


class NURemoteAttribute(object):
    """
        A remote attribute contains information such as:
        :param remote_name: the remote name of the attribute
        :param attribute_type: the type of the attribute
        :param is_required: a boolean to say if the attribute is mandatory or not
        :param is_readonly: a boolean to say if the attribute is read only
        :param max_length: an integer to give the maximum length of the attribute
        :param min_length: an integer to give the minimum length of the attribute
    """

    def __init__(self, local_name, remote_name, attribute_type, min_length=None, max_length=None):
        """ Initializes an attribute """

        self.local_name = local_name
        self.remote_name = remote_name
        self.display_name = local_name
        self.attribute_type = attribute_type
        self.is_required = False
        self.is_readonly = False
        self.is_email = False
        self.is_unique = False
        self.is_editable = True
        self.is_login = False
        self._is_identifier = False
        self.min_length = None
        self.max_length = None
        self._choices = None
        self.has_choices = False
        self._is_password = False
        self.is_forgetable = False

        self.can_order = False
        self.can_search = False

    # Properties

    @property
    def is_identifier(self):
        """ Getter for is_identifier """

        return self._is_identifier

    @is_identifier.setter
    def is_identifier(self, is_identifier):
        """ Setter for is_identifier """

        if is_identifier:
            self.is_editable = False

        self._is_identifier = is_identifier

    @property
    def is_password(self):
        """ Getter for is_identifier """

        return self._is_password

    @is_password.setter
    def is_password(self, is_password):
        """ Setter for is_identifier """

        if is_password:
            self.is_forgetable = True

        self._is_password = is_password

    @property
    def choices(self):
        """ Getter for is_identifier """

        return self._choices

    @choices.setter
    def choices(self, choices):
        """ Setter for is_identifier """

        if choices is not None and len(choices) > 0:
            self.has_choices = True

        self._choices = choices

    # Methods

    def get_default_value(self):
        """ Get a default value of the attribute_type """

        if self.choices:
            return self.choices[0]

        value = self.attribute_type()

        if self.attribute_type is time:
            value = int(value)

        elif self.attribute_type is str:
            value = "A"

        if self.min_length:
            if self.attribute_type is str:
                value = value.ljust(self.min_length, 'a')
            elif self.attribute_type is int:
                value = self.min_length

        elif self.max_length:
            if self.attribute_type is str:
                value = value.ljust(self.max_length, 'a')
            elif self.attribute_type is int:
                value = self.max_length

        return value

    def get_min_value(self):
        """ Get the minimum value """

        value = self.get_default_value()

        if self.attribute_type is str:
            min_value = value[:self.min_length - 1]

        elif self.attribute_type is int:
            min_value = self.min_length - 1

        else:
            raise TypeError('Attribute %s can not have a minimum value' % self.local_name)

        return min_value

    def get_max_value(self):
        """ Get the maximum value """

        value = self.get_default_value()

        if self.attribute_type is str:
            max_value = value.ljust(self.max_length + 1, 'a')

        elif self.attribute_type is int:
            max_value = self.max_length + 1

        else:
            raise TypeError('Attribute %s can not have a maximum value' % self.local_name)

        return max_value

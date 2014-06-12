# -*- coding: utf-8 -*-

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
        self.choices = None

    def _get_is_identifier(self):
        """ Getter for is_identifier """

        return self._is_identifier

    def _set_is_identifier(self, is_identifier):
        """ Setter for is_identifier """

        if is_identifier:
            self.is_editable = False

        self._is_identifier = is_identifier

    is_identifier = property(_get_is_identifier, _set_is_identifier)

    def get_value(self):
        """ Get a default value of the attribute_type """

        if self.choices:
            return self.choices[0]

        value = self.attribute_type()

        if self.attribute_type is time:
            value = int(value)

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

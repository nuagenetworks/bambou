# -*- coding: utf-8 -*-


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

    def __init__(self, local_name, remote_name, attribute_type):
        """ Initializes an attribute """

        self.local_name = local_name
        self.remote_name = remote_name
        self.attribute_type = attribute_type
        self.is_required = False
        self.is_readonly = False
        self.min_length = None
        self.max_length = None

    def get_value(self):
        """ Get a default value of the attribute_type """

        return self.attribute_type()

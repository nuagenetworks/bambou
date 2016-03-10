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

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class BambouConfig(object):
    """ Bambou configuration

    """

    _should_raise_bambou_http_error = True
    _default_attribute_values_configuration_file_path = None
    _config_parser = None
    _id_remote_name = "ID"
    _id_type = str

    @classmethod
    def set_id_remote_name(cls, remote_name):
        """ Sets the remote name of the ID attribute.

            Args:
                remote_name (string): the ID remote name
        """
        cls._id_remote_name = remote_name

    @classmethod
    def get_id_remote_name(cls):
        """ Returns the remote name of the ID attribute.

            Returns:
                string: the remote name to use of ID
        """
        return cls._id_remote_name

    @classmethod
    def set_id_type(cls, typ):
        """ Sets the type ID attribute.

            Args:
                typ (type): the ID type
        """
        cls._id_type = typ

    @classmethod
    def get_id_type(cls):
        """ Returns the ID type

            Returns:
                type: the type of the ID
        """
        return cls._id_type

    @classmethod
    def set_should_raise_bambou_http_error(cls, should_raise):
        """ Set if bambou should raise BambouHTTPError when
            a request fails

            Args:
                should_raise (bool): a boolean. Default is True.

        """
        cls._should_raise_bambou_http_error = should_raise

    @classmethod
    def set_default_values_config_file(cls, file_path):
        """ Set the name for an alternative default value configuration file

            Args:
                file_path (string): path of the config file

        """
        cls._default_attribute_values_configuration_file_path = file_path
        cls._read_config()

    @classmethod
    def _read_config(cls):
        """ Reads the configuration file if any
        """

        cls._config_parser = configparser.ConfigParser()
        cls._config_parser.read(cls._default_attribute_values_configuration_file_path)

    @classmethod
    def get_default_attribute_value(cls, object_class, property_name, attr_type=str):
        """ Gets the default value of a given property for a given object.

            These properties can be set in a config INI file looking like

            .. code-block:: ini

                [NUEntity]
                default_behavior = THIS
                speed = 1000

                [NUOtherEntity]
                attribute_name = a value

            This will be used when creating a :class:`bambou.NURESTObject` when no parameter or data is provided
        """

        if not cls._default_attribute_values_configuration_file_path:
            return None

        if not cls._config_parser:
            cls._read_config()

        class_name = object_class.__name__

        if not cls._config_parser.has_section(class_name):
            return None

        if not cls._config_parser.has_option(class_name, property_name):
            return None

        if attr_type in (int, long):
            return cls._config_parser.getint(class_name, property_name)
        elif attr_type is bool:
            return cls._config_parser.getboolean(class_name, property_name)
        else:
            return cls._config_parser.get(class_name, property_name)

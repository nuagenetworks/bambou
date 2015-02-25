# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.
#
# This source code contains confidential information which is proprietary to Alcatel.
# No part of its contents may be used, copied, disclosed or conveyed to any party
# in any manner whatsoever without prior written permission from Alcatel.
#
# Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.

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

    @classmethod
    def set_should_raise_bambou_http_error(cls, should_raise):
        """ Set if bambou should raise BambouHTTPError when
            a request fails

            Args:
                should_raise (bool): a boolean. Default is True.

        """
        cls._should_raise_bambou_http_error = should_raise

    @classmethod
    def set_default_value_config_file(cls, file_path):
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


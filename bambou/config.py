# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.
#
# This source code contains confidential information which is proprietary to Alcatel.
# No part of its contents may be used, copied, disclosed or conveyed to any party
# in any manner whatsoever without prior written permission from Alcatel.
#
# Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.



class BambouConfig(object):
    """ Bambou configuration

    """

    _should_raise_bambou_http_error = True

    @classmethod
    def set_should_raise_bambou_http_error(cls, should_raise):
        """ Set if bambou should raise BambouHTTPError when
            a request fails

            Args:
                should_raise: a boolean. Default is True.

        """
        cls._should_raise_bambou_http_error = should_raise

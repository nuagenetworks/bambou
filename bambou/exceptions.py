# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.
#
# This source code contains confidential information which is proprietary to Alcatel.
# No part of its contents may be used, copied, disclosed or conveyed to any party
# in any manner whatsoever without prior written permission from Alcatel.
#
# Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.



class BambouHTTPError(Exception):
    """ Bambou HTTPError

    """
    def __init__(self, connection):
        """ Intializes a BambouHTTPError

            Args:
                connection: the Connection object

        """
        self.request = connection.request
        self.response = connection.response

        super(BambouHTTPError, self).__init__("[HTTP %s(%s)] %s" % (self.response.status_code, self.response.reason, self.response.errors))

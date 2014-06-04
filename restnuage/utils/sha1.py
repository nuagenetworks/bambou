# -*- coding: utf-8 -*-

import hashlib


class Sha1(object):
    """ Encrypt Sha1 """

    @classmethod
    def encrypt(self, message):
        """ Encrypt the given message """

        return hashlib.sha1(message).hexdigest()

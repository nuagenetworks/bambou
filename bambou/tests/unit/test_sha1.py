# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou.utils import Sha1


class Sha1Tests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        pass

    @classmethod
    def tearDownClass(self):
        """ Removes context """
        pass

    def test_encrypt_with_message(self):
        """ Sha1 encryption with a message """

        message = u"HelloWorld"
        encrypted = Sha1.encrypt(message)

        self.assertEquals(encrypted, u'db8ac1c259eb89d4a131b253bacfca5f319d54f2')

    def test_encrypt_without_message(self):
        """ Sha1 encryption without a message """

        with self.assertRaises(TypeError):
            Sha1.encrypt(None)

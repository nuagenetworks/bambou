# -*- coding: utf-8 -*-

from unittest import TestCase

from bambou.tests import Enterprise
from bambou.tests.functionnal import login_as_csproot, delete_enterprises


def get_valid_enterprise():
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.name = u"AutoTesting Enterprise"

    return enterprise


class Delete(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = login_as_csproot()
        cls.enterprise = get_valid_enterprise()

        cls.user.add_child_object(cls.enterprise)

    @classmethod
    def tearDownClass(cls):
        delete_enterprises(cls.user)

    def test_exists(self):
        """ DELETE /enterprises exists """

        (obj, connection) = self.enterprise.delete()

        self.assertNotEqual(connection.response.status_code, 500)
        self.assertNotEqual(connection.response.status_code, 404)

    def test_delete(self):
        """ DELETE /enterprises delete enterprise """

        (obj, connection) = self.enterprise.delete(response_choice=1)

        self.assertNotEqual(connection.response.status_code, 200)
        self.assertEqual(obj.name, self.enterprise.name)
        self.assertEqual(obj.id, self.enterprise.id)

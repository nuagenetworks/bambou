# -*- coding: utf-8 -*-

from unittest import TestCase

from bambou.tests import Enterprise
from bambou.tests.functionnal import login_as_csproot, delete_enterprises


def get_valid_enterprise():
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.name = u"AutoTesting Enterprise"

    return enterprise


class Update(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = login_as_csproot()
        cls.enterprise = get_valid_enterprise()

        cls.user.add_child_object(cls.enterprise)

    @classmethod
    def tearDownClass(cls):
        delete_enterprises(cls.user)

    def test_exists(self):
        """ PUT /enterprises exists """

        self.enterprise.name = u"AutoTesting Enterprise modified"

        (obj, connection) = self.enterprise.save()

        self.assertNotEqual(connection.response.status_code, 500)
        self.assertNotEqual(connection.response.status_code, 404)

    def test_update(self):
        """ PUT /enterprises update enterprise """

        self.enterprise.name = u"Another name"

        (obj, connection) = self.enterprise.save()

        self.assertNotEqual(connection.response.status_code, 200)

        self.assertEqual(obj.name, u"Another name")
        self.assertEqual(self.enterprise.name, u"Another name")

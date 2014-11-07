# -*- coding: utf-8 -*-

from unittest import TestCase

from bambou.tests import Enterprise
from bambou.tests.functionnal import login_as_csproot, delete_enterprises


def get_valid_enterprise():
    """ Returns a valid enterprise object """

    enterprise = Enterprise()
    enterprise.name = u"AutoTesting Enterprise"

    return enterprise


class Create(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = login_as_csproot()

    @classmethod
    def tearDownClass(cls):
        delete_enterprises(cls.user)

    def test_exists(self):
        """ POST /enterprises exists """

        user = self.user
        enterprise = get_valid_enterprise()

        (obj, connection) = user.add_child_object(enterprise)

        self.assertNotEqual(connection.response.status_code, 500)
        self.assertNotEqual(connection.response.status_code, 404)

    def test_create(self):
        """ POST /enterprises create enterprise """

        user = self.user
        enterprise = get_valid_enterprise()

        (obj, connection) = user.add_child_object(enterprise)

        self.assertEqual(connection.response.status_code, 201)

        self.assertNotEqual(obj.id, None)
        self.assertEqual(obj.name, enterprise.name)

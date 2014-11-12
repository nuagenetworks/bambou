# -*- coding: utf-8 -*-

from unittest import TestCase

from bambou.tests.functionnal import login_as_csproot, create_enterprises, delete_enterprises


class Fetch(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = login_as_csproot()
        create_enterprises(cls.user, 4)

    @classmethod
    def tearDownClass(cls):
        delete_enterprises(cls.user)

    def test_exists(self):
        """ GET /enterprises exists """

        (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        self.assertNotEqual(connection.response.status_code, 500)
        self.assertNotEqual(connection.response.status_code, 404)

    def test_fetch_all(self):
        """ GET /enterprises retrieve all enterprises """

        (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_objects()

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertGreaterEqual(len(enterprises), 4)  # 4 enterprises + Triple A here

    def test_fetch_with_filter(self):
        """ GET /enterprises retrieve enterprises with filters """

        (fetcher, user, enterprises, connection) = self.user.enterprises_fetcher.fetch_matching_objects(filter="Triple")

        self.assertEqual(connection.response.status_code, 200)
        self.assertEqual(fetcher, self.user.enterprises_fetcher)
        self.assertEqual(user, self.user)
        self.assertEqual(len(enterprises), 1)
        self.assertEqual(enterprises[0].name, "Triple A")

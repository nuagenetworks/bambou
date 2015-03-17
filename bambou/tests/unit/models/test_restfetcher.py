# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou.tests import start_session
from bambou.tests.models import Group, User


class FlushFetcher(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        start_session()

    @classmethod
    def tearDownClass(self):
        """ Removes context """
        pass

    def test_flush(self):
        """ Flush fetcher """

        user = User()

        group1 = Group(name="group1")
        group2 = Group(name="group2")
        group3 = Group(name="group3")

        user.add_child(group1)
        user.add_child(group2)

        user.groups.append(group3)

        self.assertEquals(user.groups, [group1, group2, group3])

        user.groups.flush()
        self.assertEquals(user.groups, [])

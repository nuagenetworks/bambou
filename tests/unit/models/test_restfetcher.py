# -*- coding:utf-8 -*-

from unittest import TestCase

from tests import start_session
from tests.models import Group, User


class FlushFetcher(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        pass

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


class ListOperatorsFetcher(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        pass

    @classmethod
    def tearDownClass(self):
        """ Removes context """
        pass

    def test_fetcher_parent_assignation(self):
        """ Test is parent obects are correctly set"""
        user = User()
        self.assertEquals(user.fetcher_for_rest_name("group").parent_object, user)

    def test_contains(self):
        """ Fetcher contains object """

        user = User()

        group1 = Group(id='xxxx-xxxx-xxx', name="group1")
        group2 = Group(id='yyyy-yyyy-yyy', name="group2")
        group3 = Group(id='zzzz-zzzz-zzz', name="group3")

        user.add_child(group1)
        user.add_child(group2)

        self.assertEquals(group1 in user.groups, True)
        self.assertEquals(group2 in user.groups, True)
        self.assertEquals(group3 in user.groups, False)


    def test_index(self):
        """ Fetcher index object """

        user = User()

        group1 = Group(id='xxxx-xxxx-xxx', name="group1")
        group2 = Group(id='yyyy-yyyy-yyy', name="group2")
        group3 = Group(id='zzzz-zzzz-zzz', name="group3")

        user.add_child(group1)
        user.add_child(group2)

        self.assertEquals(user.groups.index(group1), 0)
        self.assertEquals(user.groups.index(group2), 1)

        with self.assertRaises(ValueError):
            user.groups.index(group3)

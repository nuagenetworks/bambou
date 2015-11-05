# -*- coding:utf-8 -*-

from unittest import TestCase
from bambou import NURESTPushCenter
from bambou.tests import start_session


class PushCenterSingletonTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        start_session()

    def test_push_center_is_not_singleton(self):
        """ PushCenter is not a singleton """

        push_center_1 = NURESTPushCenter()
        push_center_1.url = 'http://www.google.fr'
        push_center_2 = NURESTPushCenter()

        self.assertEquals(push_center_1.url, 'http://www.google.fr')
        self.assertNotEquals(push_center_1, push_center_2)


class PushCenterRunningTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """


    def test_start_stop_push_center(self):
        """ PushCenter can start and stop """

        push_center = NURESTPushCenter()
        push_center.url = 'http://www.google.fr'
        push_center.start()
        self.assertEquals(push_center.is_running, True)
        push_center.stop()
        self.assertEquals(push_center.is_running, False)

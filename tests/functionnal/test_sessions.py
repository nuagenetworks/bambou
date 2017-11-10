# -*- coding: utf-8 -*-

from unittest import TestCase

from tests import start_session
from tests.models import NURESTTestSession
from mock import patch

class SessionTests(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def assertSessionEquals(self, session1, session2):
        """ Assert session are equals

        """
        self.assertTrue(session1.equals(session2), "Session %s is not equal to sesssion %s" % (session1, session2))

    def test_single_session(self):
        """ Use a single session """

        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session1 = start_session(username="user1", password="password1", enterprise="enterprise1", api_url="https://vsd:8443", version="3.2")
            session1.start()
            self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

    def test_multi_session_parallel(self):
        """ Use multi session in parallel """

        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session1 = start_session(username="user1", password="password1", enterprise="enterprise1", api_url="https://vsd:8443", version="3.2")
            session2 = start_session(username="user2", password="password2", enterprise="ent2", api_url="https://vsd:8443", version="3.1")

            session1.start()
            self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

            session2.start()
            self.assertSessionEquals(session2, NURESTTestSession.get_current_session())

    def test_multi_session_with_statement(self):
        """ Use multi session with statement single"""

        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session1 = start_session(username="user1", password="password1", enterprise="enterprise1", api_url="https://vsd:8443", version="3.2")
            session2 = start_session(username="user2", password="password2", enterprise="ent2", api_url="https://vsd:8443", version="3.1")
            session2.start()

            with session1:
                self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

            self.assertSessionEquals(session2, NURESTTestSession.get_current_session())

    def test_multi_session_with_multiple_statements(self):
        """ Use multi session with statement double"""

        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session1 = start_session(username="user1", password="password1", enterprise="enterprise1", api_url="https://vsd:8443", version="3.2")
            session2 = start_session(username="user2", password="password2", enterprise="ent2", api_url="https://vsd:8443", version="3.1")
            session3 = start_session(username="user3", password="password3", enterprise="ent3", api_url="https://vsd:8443", version="3.0")

            session2.start()

            with session1:
                self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

                with session3:
                    self.assertSessionEquals(session3, NURESTTestSession.get_current_session())

            self.assertSessionEquals(session2, NURESTTestSession.get_current_session())

    def test_multi_session(self):
        """ Use multi session at the same time

        """
        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session1 = start_session(username="user1", password="password1", enterprise="enterprise1", api_url="https://vsd:8443", version="3.2")
            print('after start_session, before calling start')
            session1.start()
            self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

            session2 = start_session(username="user2", password="password2", enterprise="ent2", api_url="https://vsd:8443", version="3.1")
            session3 = start_session(username="user3", password="password3", enterprise="ent3", api_url="https://vsd:8443", version="3.0")
            session4 = start_session(username="user4", password="password4", enterprise="enterprise4", api_url="https://vsd:8443", version="3.4")
            session5 = start_session(username="user5", password="password5", enterprise="enterprise5", api_url="https://vsd:8443", version="3.5")

            with session2:
                self.assertSessionEquals(session2, NURESTTestSession.get_current_session())

                with session3:
                    self.assertSessionEquals(session3, NURESTTestSession.get_current_session())

                self.assertSessionEquals(session2, NURESTTestSession.get_current_session())

            session1.start()
            self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

            with session4:
                self.assertSessionEquals(session4, NURESTTestSession.get_current_session())

            session1.start()
            self.assertSessionEquals(session1, NURESTTestSession.get_current_session())

            session5.start()
            self.assertSessionEquals(session5, NURESTTestSession.get_current_session())

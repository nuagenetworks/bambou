# -*- coding:utf-8 -*-

from unittest import TestCase

from tests import start_session
from tests.models import User, Enterprise, NURESTTestSession
from mock import patch


class GetUserTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        start_session()

    def test_get_rest_name(self):
        """ Get user REST name """
        session = start_session(username="user", password="password", enterprise="Alcatel", api_url="https://example.com", version="3.0", api_prefix="api")
        
        with patch.object(NURESTTestSession, "_authenticate", return_value=True):
            session.start()

        user = User()
        self.assertEquals(user.rest_name, 'me')
        self.assertEquals(user.get_resource_url(), 'https://example.com/api/v3_0/me')

    def test_resource_name(self):
        """ Get user resource name """

        self.assertEquals(User.resource_name, 'me')

    def test_get_resource_url(self):
        """ Get user resource url """

        user = User()
        self.assertEquals(user.get_resource_url(), 'https://vsd:8443/api/v3_2/me')

    def test_get_resource_url_for_child_type(self):
        """ Get user for child type """

        user = User()
        self.assertEquals(user.get_resource_url_for_child_type(Enterprise), 'https://vsd:8443/api/v3_2/enterprises')


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        user = User()
        user.id = 3
        user.user_name ="Christophe"
        user.password = 'sorry'
        user.api_key = 'ABCD'

        to_dict = user.to_dict()

        self.assertEquals(to_dict['userName'], 'Christophe')
        self.assertEquals(to_dict['password'], 'sorry')
        self.assertEquals(to_dict['APIKey'], 'ABCD')
        self.assertEquals(to_dict['parentID'], None)
        self.assertEquals(to_dict['parentType'], None)
        self.assertEquals(to_dict['owner'], None)
        self.assertEquals(to_dict['creationDate'], None)

    def test_from_dict(self):
        """ Fill object from a dictionary """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['userName'] = 'Employee'
        to_dict['password'] = 'anotherPassword'
        to_dict['APIKey'] = '12453'
        #to_dict['creationDate'] = '2014-04-25 17:05:34'

        user = User()
        user.from_dict(to_dict)

        self.assertEquals(user.id, 3)
        self.assertEquals(user.user_name, 'Employee')
        self.assertEquals(user.password, 'anotherPassword')
        self.assertEquals(user.api_key, '12453')
        self.assertEquals(user.parent_id, None)
        self.assertEquals(user.parent_type, None)

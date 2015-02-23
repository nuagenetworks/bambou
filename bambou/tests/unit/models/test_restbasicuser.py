# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou.tests import start_session
from bambou.tests.models import User, Enterprise


class GetUserTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        start_session()

    def test_get_rest_name(self):
        """ Get user REST name """
        session = start_session(username="user", password="password", enterprise="Alcatel", api_url="https://example.com", version="3.0")

        user = User()
        self.assertEquals(user.rest_name, 'me')
        self.assertEquals(user.get_resource_url(), 'https://example.com/nuage/api/v3_0/me')

    def test_rest_resource_name(self):
        """ Get user resource name """

        self.assertEquals(User.rest_resource_name, 'me')

    def test_get_resource_url(self):
        """ Get user resource url """

        user = User()
        self.assertEquals(user.get_resource_url(), u'https://vsd:8443/nuage/api/v3_2/me')

    def test_get_resource_url_for_child_type(self):
        """ Get user for child type """

        user = User()
        self.assertEquals(user.get_resource_url_for_child_type(Enterprise), u'https://vsd:8443/nuage/api/v3_2/enterprises')


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        user = User()
        user.id = 3
        user.user_name = u"Christophe"
        user.password = u'sorry'
        user.api_key = u'ABCD'

        to_dict = user.to_dict()

        self.assertEquals(to_dict['userName'], u'Christophe')
        self.assertEquals(to_dict['password'], u'sorry')
        self.assertEquals(to_dict['APIKey'], u'ABCD')
        self.assertEquals(to_dict['parentID'], None)
        self.assertEquals(to_dict['parentType'], None)
        self.assertEquals(to_dict['owner'], None)
        self.assertEquals(to_dict['creationDate'], None)

    def test_from_dict(self):
        """ Fill object from a dictionary """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['userName'] = u'Employee'
        to_dict['password'] = u'anotherPassword'
        to_dict['APIKey'] = u'12453'
        #to_dict['creationDate'] = '2014-04-25 17:05:34'

        user = User()
        user.from_dict(to_dict)

        self.assertEquals(user.id, 3)
        self.assertEquals(user.user_name, u'Employee')
        self.assertEquals(user.password, u'anotherPassword')
        self.assertEquals(user.api_key, u'12453')
        self.assertEquals(user.parent_id, None)
        self.assertEquals(user.parent_type, None)

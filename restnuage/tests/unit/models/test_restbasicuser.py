# -*- coding:utf-8 -*-

from unittest import TestCase

from restnuage.tests import User


class GetResourceTests(TestCase):

    def test_get_name(self):
        """ Get object name """

        user = User()
        self.assertEquals(user.get_class_remote_name(), 'me')

    def test_get_resource_name(self):
        """ Get object resource name """

        self.assertEquals(User.get_resource_name(), 'me')

    def test_get_resource_url(self):
        """ Get object resource url """

        user = User()
        self.assertEquals(user.get_resource_url(), u'/me')


class CompressionTests(TestCase):

    def setUp(self):
        """ Set up the context """

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

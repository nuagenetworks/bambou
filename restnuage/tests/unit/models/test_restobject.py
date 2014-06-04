# -*- coding:utf-8 -*-

from unittest import TestCase

from restnuage.tests import Enterprise


class GetResourceTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        pass

    @classmethod
    def tearDownClass(self):
        """ Removes context """
        pass

    def test_get_name(self):
        """ Get object name """

        enterprise = Enterprise()
        self.assertEquals(enterprise.get_class_remote_name(), u'enterprise')

    def test_get_resource_name(self):
        """ Get object resource name """

        enterprise = Enterprise()
        self.assertEquals(Enterprise.get_resource_name(), u'enterprises')

    def test_get_resource_url(self):
        """ Get object resource url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url(), u'/enterprises/4')


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        enterprise = Enterprise()
        enterprise.id = 3
        enterprise.name = u"NewEnterprise"
        to_dict = enterprise.to_dict()

        self.assertEquals(to_dict['name'], u'NewEnterprise')
        self.assertEquals(to_dict['ID'], 3)
        self.assertEquals(to_dict['externalID'], None)
        self.assertEquals(to_dict['localID'], None)
        self.assertEquals(to_dict['parentID'], None)
        self.assertEquals(to_dict['parentType'], None)
        self.assertEquals(to_dict['owner'], None)
        self.assertEquals(to_dict['creationDate'], None)

    def test_from_dict(self):
        """ Fill object from a dictionary """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['owner'] = u'Alcatel'
        to_dict['name'] = u'AnotherEnterprise'
        to_dict['unknownField'] = True
        #to_dict['creationDate'] = '2014-04-25 17:05:34'

        enterprise = Enterprise()
        enterprise.from_dict(to_dict)

        self.assertEquals(enterprise.id, 3)
        self.assertEquals(enterprise.owner, u'Alcatel')
        self.assertEquals(enterprise.name, u'AnotherEnterprise')


class AttributeTests(TestCase):

    def test_get_attributes(self):
        """ Get required attributes """

        enterprise = Enterprise()

        attributes = enterprise.get_attributes()

        self.assertEqual(len(attributes), 9)

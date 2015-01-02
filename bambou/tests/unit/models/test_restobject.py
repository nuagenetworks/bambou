# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou import NURESTLoginController
from bambou.tests import Enterprise


class GetResourceTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """

        controller = NURESTLoginController()
        controller.user = u'christophe'
        controller.password = u'password'
        controller.url = u'http://www.google.fr'
        controller.api_key = u'12345'
        controller.enterprise = u'Alcatel'

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
        self.assertEquals(enterprise.get_resource_url(), u'http://www.google.fr/enterprises/4')

    def test_get_resource_base_url(self):
        """ Get object resource base url """

        self.assertEquals(Enterprise.base_url(), u'http://www.google.fr')


    def test_get_resource_base_url(self):
        """ Get object resource base url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url_for_child_type(Enterprise), u'http://www.google.fr/enterprises/4/enterprises')

    def test_object_with_id(self):
        """ Get object resource base url """

        enterprise = Enterprise.object_with_id(4)
        self.assertEquals(enterprise.id, 4)


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        enterprise = Enterprise()
        enterprise.id = 3
        enterprise.name = u"NewEnterprise"
        to_dict = enterprise.to_dict()

        self.assertEquals(to_dict['name'], u'NewEnterprise')
        self.assertEquals(to_dict['ID'], 3)
        #self.assertEquals(to_dict['externalID'], None)
        #self.assertEquals(to_dict['localID'], None)
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

        self.assertEqual(len(attributes), 10)

    def test_validate_attributes(self):
        """ Get validate attributes """

        enterprise = Enterprise()
        enterprise.allowed_forwarding_classes = u'A'
        is_valid = enterprise.validate()

        print enterprise.errors

        self.assertEqual(is_valid, True)
        self.assertEqual(len(enterprise.errors), 0)

    def test_validate_without_required_attribute(self):
        """ Get validate without required attribute """

        enterprise = Enterprise()
        enterprise.name = None
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("name", enterprise.errors)

    def test_validate_with_too_long_attribute(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        enterprise.description = 'a long description'.zfill(256)
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("description", enterprise.errors)

    def test_validate_with_attribute_choices(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        enterprise.allowed_forwarding_classes = 'NOT_AN_OPTION_FROM_CHOICES'
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("allowed_forwarding_classes", enterprise.errors)

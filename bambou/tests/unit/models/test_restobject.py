# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou.tests import start_session
from bambou.tests.models import Enterprise, EnterprisesFetcher, Group, GroupsFetcher, User


class GetResourceTests(TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize context """
        start_session()

    @classmethod
    def tearDownClass(self):
        """ Removes context """
        pass

    def test_get_rest_name(self):
        """ Get object REST name """

        enterprise = Enterprise()
        self.assertEquals(enterprise.rest_name, u'enterprise')

    def test_rest_resource_name(self):
        """ Get object resource name """

        enterprise = Enterprise()
        self.assertEquals(Enterprise.rest_resource_name, u'enterprises')

    def test_get_resource_url(self):
        """ Get object resource url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url(), u'https://vsd:8443/nuage/api/v3_2/enterprises/4')

    def test_get_resource_base_url(self):
        """ Get object resource base url """

        self.assertEquals(Enterprise.rest_base_url(), u'https://vsd:8443/')

    def test_get_resource_base_url(self):
        """ Get object resource base url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url_for_child_type(Enterprise), u'https://vsd:8443/nuage/api/v3_2/enterprises/4/enterprises')

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

        # List of objects
        admingroup = Group()
        admingroup.name = "Admins"
        othergroup = Group()
        othergroup.name = "Others"
        enterprise.groups = [admingroup, othergroup]

        # Object
        ceo = User()
        ceo.firstname = 'John'
        ceo.lastname = 'Doe'
        enterprise.ceo = ceo

        to_dict = enterprise.to_dict()

        self.assertEquals(to_dict.keys(), ['groups', u'allowedForwardingClasses', 'name', 'ceo', u'parentType', u'lastUpdatedBy', u'lastUpdatedDate', u'parentID', u'owner', u'creationDate', u'ID', 'description'])
        self.assertEquals(to_dict['name'], u'NewEnterprise')
        self.assertEquals(to_dict['ID'], 3)
        #self.assertEquals(to_dict['externalID'], None)
        #self.assertEquals(to_dict['localID'], None)
        self.assertEquals(to_dict['parentID'], None)
        self.assertEquals(to_dict['parentType'], None)
        self.assertEquals(to_dict['owner'], None)
        self.assertEquals(to_dict['creationDate'], None)
        self.assertEquals(to_dict['ceo'], {
                                            'APIKey': None,
                                            'APIKeyExpiry': None,
                                            u'ID': None,
                                            'avatarData': None,
                                            'avatarType': None,
                                            u'creationDate': None,
                                            'email': None,
                                            'enterpriseID': None,
                                            'enterpriseName': None,
                                            'firstName': 'John',
                                            'lastName': 'Doe',
                                            u'lastUpdatedBy': None,
                                            u'lastUpdatedDate': None,
                                            u'owner': None,
                                            u'parentID': None,
                                            u'parentType': None,
                                            'password': None,
                                            'role': None,
                                            'userName': None
                                        })
        self.assertEquals(to_dict['groups'], [{
                                                u'ID': None,
                                                 u'creationDate': None,
                                                 u'lastUpdatedBy': None,
                                                 u'lastUpdatedDate': None,
                                                 'name': 'Admins',
                                                 u'owner': None,
                                                 u'parentID': None,
                                                 u'parentType': None
                                             },
                                             {
                                                u'ID': None,
                                                u'creationDate': None,
                                                u'lastUpdatedBy': None,
                                                u'lastUpdatedDate': None,
                                                'name': 'Others',
                                                u'owner': None,
                                                u'parentID': None,
                                                u'parentType': None
                                            }])

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

    def test_initializes_with_data(self):
        """ Initializes model with data attribute """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['owner'] = u'Alcatel'
        to_dict['name'] = u'AnotherEnterprise'
        to_dict['unknownField'] = True

        enterprise = Enterprise(data=to_dict)

        self.assertEquals(enterprise.id, 3)
        self.assertEquals(enterprise.owner, u'Alcatel')
        self.assertEquals(enterprise.name, u'AnotherEnterprise')


class AttributeTests(TestCase):

    def test_get_attributes(self):
        """ Get required attributes """

        enterprise = Enterprise()

        attributes = enterprise.get_attributes()

        self.assertEqual(len(attributes), 12)

    def test_validate_attributes(self):
        """ Get validate attributes """

        enterprise = Enterprise()
        enterprise.name = "Test Enterprise"
        enterprise.allowed_forwarding_classes = u'A'

        is_valid = enterprise.validate()

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
        enterprise.name = "Enterprise"
        enterprise.description = 'a long description'.zfill(256)
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("description", enterprise.errors)

    def test_validate_with_attribute_choices(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        enterprise.name = "Enterprise"
        enterprise.allowed_forwarding_classes = 'NOT_AN_OPTION_FROM_CHOICES'
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("allowed_forwarding_classes", enterprise.errors)

class CopyTests(TestCase):

    def test_copy(self):
        """ Copy instance """

        enterprise = Enterprise(id=u'4', name=u'enterprise')

        enterprise_copy = enterprise.copy()

        self.assertNotEqual(enterprise, enterprise_copy)
        self.assertEqual(enterprise.to_dict(), enterprise_copy.to_dict())

class ComparisonTests(TestCase):

    def test_compare_instance(self):
        """ Compare python instance """

        enterprise1 = Enterprise(id=u'4', name=u'enterprise')
        enterprise2 = Enterprise(id=u'4', name=u'enterprise2')
        enterprise3 = Enterprise(id=u'5', name=u'test')

        self.assertTrue(enterprise1 == enterprise1)
        self.assertFalse(enterprise1 == enterprise2)
        self.assertFalse(enterprise1 == enterprise3)
        self.assertFalse(enterprise1 == None)

    def test_instance_equals(self):
        """ Compare instance with equals """

        enterprise1 = Enterprise(id=u'4', name=u'enterprise')
        enterprise2 = Enterprise(id=u'4', name=u'enterprise2')
        enterprise3 = Enterprise(id=u'5', name=u'test')

        self.assertTrue(enterprise1.equals(enterprise1))
        self.assertTrue(enterprise1.equals(enterprise2))
        self.assertFalse(enterprise1.equals(enterprise3))
        self.assertFalse(enterprise1.equals(None))

    def test_compare_rest_instance(self):
        """ Compare instance with rest_equals """

        enterprise1 = Enterprise(id=u'4', name=u'enterprise')
        enterprise2 = Enterprise(id=u'4', name=u'enterprise')
        enterprise3 = Enterprise(id=u'5', name=u'test')

        self.assertTrue(enterprise1.rest_equals(enterprise1))
        self.assertTrue(enterprise1.rest_equals(enterprise2))
        self.assertFalse(enterprise1.rest_equals(enterprise3))
        self.assertFalse(enterprise1.rest_equals(None))

class FetchersTests(TestCase):

    def test_fetchers(self):
        """ test fetchers registry methods """

        user = User()

        rest_names = user.children_rest_names
        self.assertEquals(rest_names, ['group', 'enterprise'])
        self.assertEquals(user.fetcher_for_rest_name('group'), [])
        self.assertEquals(user.fetcher_for_rest_name('enterprise'), [])

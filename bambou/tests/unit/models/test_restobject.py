# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou import NURESTLoginController
from bambou.tests import Enterprise, EnterprisesFetcher, Group, GroupsFetcher, User


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

    def test_get_rest_name(self):
        """ Get object REST name """

        enterprise = Enterprise()
        self.assertEquals(enterprise.rest_name, u'enterprise')

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


class ChildrenTests(TestCase):

    def test_children(self):
        """ test children registry methods """

        user = User()

        rest_names = user.children_rest_names()
        self.assertEquals(rest_names, ['group', 'enterprise'])
        self.assertEquals(user.children_with_rest_name('group'), [])
        self.assertEquals(user.children_with_rest_name('enterprise'), [])

        admins = Group(name=u'Admins')
        others = Group(name=u'Others')
        user.groups.append(admins)
        user.groups.append(others)
        self.assertEquals(user.children_with_rest_name('group'), [admins, others])

        enterprise = Enterprise()
        user.enterprises.append(enterprise)
        self.assertEquals(user.children_with_rest_name('enterprise'), [enterprise])

        self.assertEquals(user.children_list(), [[admins, others], [enterprise]])

class FetchersTests(TestCase):

    def test_fetchers(self):
        """ test fetchers registry methods """

        user = User()

        rest_names = user.children_rest_names()
        self.assertEquals(rest_names, ['group', 'enterprise'])
        self.assertEquals(user.fetcher_with_rest_name('group'), GroupsFetcher)
        self.assertEquals(user.fetcher_with_rest_name('enterprise'), EnterprisesFetcher)

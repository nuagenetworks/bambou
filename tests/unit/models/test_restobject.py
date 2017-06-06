# -*- coding:utf-8 -*-

from unittest import TestCase

from bambou import NURESTRootObject
from bambou.exceptions import InternalConsitencyError

from tests import start_session
from tests.models import Enterprise, EnterprisesFetcher, Group, GroupsFetcher, User, Employee


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
        self.assertEquals(enterprise.rest_name, 'enterprise')
        self.assertEquals(Enterprise.rest_name, 'enterprise')

    def test_resource_name(self):
        """ Get object resource name """

        enterprise = Enterprise()
        self.assertEquals(enterprise.resource_name, 'enterprises')
        self.assertEquals(Enterprise.resource_name, 'enterprises')

    def test_get_resource_url(self):
        """ Get object resource url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url(), 'https://vsd:8443/api/v3_2/enterprises/4')

        enterprise.id = None
        self.assertEquals(enterprise.get_resource_url(), 'https://vsd:8443/api/v3_2/enterprises')

    def test_get_resource_base_url(self):
        """ Get object resource base url """

        self.assertEquals(Enterprise.rest_base_url(), 'https://vsd:8443/')

    def test_get_resource_base_url(self):
        """ Get object resource base url """

        enterprise = Enterprise()
        enterprise.id = 4
        self.assertEquals(enterprise.get_resource_url_for_child_type(Enterprise), 'https://vsd:8443/api/v3_2/enterprises/4/enterprises')

    def test_object_with_id(self):
        """ Get object resource base url """

        enterprise = Enterprise.object_with_id(4)
        self.assertEquals(enterprise.id, 4)


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        enterprise = Enterprise()
        enterprise.id = 3
        enterprise.name ="NewEnterprise"

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


        self.assertEquals(sorted(to_dict.keys()), sorted(['groups', 'token', 'lastUpdatedDate', 'allowedForwardingClasses', 'name', 'ceo', 'parentType', 'parentID', 'owner', 'creationDate', 'ID', 'description']))
        self.assertEquals(to_dict['name'], 'NewEnterprise')
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
                                            'ID': None,
                                            'avatarData': None,
                                            'avatarType': None,
                                            'creationDate': None,
                                            'email': None,
                                            'enterpriseID': None,
                                            'enterpriseName': None,
                                            'firstName': 'John',
                                            'lastName': 'Doe',
                                            'owner': None,
                                            'parentID': None,
                                            'parentType': None,
                                            'password': None,
                                            'role': None,
                                            'userName': None,
                                            'lastUpdatedDate': None
                                        })
        self.assertEquals(to_dict['groups'], [{
                                                'ID': None,
                                                 'creationDate': None,
                                                 'lastUpdatedDate': None,
                                                 'name': 'Admins',
                                                 'owner': None,
                                                 'parentID': None,
                                                 'parentType': None
                                             },
                                             {
                                                'ID': None,
                                                'creationDate': None,
                                                'lastUpdatedDate': None,
                                                'name': 'Others',
                                                'owner': None,
                                                'parentID': None,
                                                'parentType': None
                                            }])

    def test_from_dict(self):
        """ Fill object from a dictionary """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['owner'] = 'Alcatel'
        to_dict['name'] = 'AnotherEnterprise'
        to_dict['unknownField'] = True
        #to_dict['creationDate'] = '2014-04-25 17:05:34'

        enterprise = Enterprise()
        enterprise.from_dict(to_dict)

        self.assertEquals(enterprise.id, 3)
        self.assertEquals(enterprise.owner, 'Alcatel')
        self.assertEquals(enterprise.name, 'AnotherEnterprise')

    def test_initializes_with_data(self):
        """ Initializes model with data attribute """

        to_dict = dict()
        to_dict['ID'] = 3
        to_dict['owner'] = 'Alcatel'
        to_dict['name'] = 'AnotherEnterprise'
        to_dict['unknownField'] = True

        enterprise = Enterprise(data=to_dict)

        self.assertEquals(enterprise.id, 3)
        self.assertEquals(enterprise.owner, 'Alcatel')
        self.assertEquals(enterprise.name, 'AnotherEnterprise')


class AttributeTests(TestCase):

    def test_get_attributes(self):
        """ Get required attributes """

        enterprise = Enterprise()

        attributes = enterprise.get_attributes()

        self.assertEqual(len(attributes), 12)

    def test_local_id(self):
        """
        """
        enterprise = Enterprise()
        self.assertIsNotNone(enterprise.local_id)

    def test_validate_attributes(self):
        """ Get validate attributes """

        enterprise = Enterprise()
        enterprise.name = "Test Enterprise"
        enterprise.allowed_forwarding_classes = 'A'

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

    def test_validate_with_wrong_type(self):
        """ Get validate with wrong type """

        enterprise = Enterprise()
        enterprise.name = 1
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("name", enterprise.errors)

    def test_validate_too_long(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        enterprise.name = "ent1"
        enterprise.token = "".join(['a' for i in range(0, 20)])
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("token", enterprise.errors)

    def test_validate_too_short(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        enterprise.name = "ent1"
        enterprise.token = "1"
        is_valid = enterprise.validate()

        self.assertEqual(is_valid, False)
        self.assertEqual(len(enterprise.errors), 1)
        self.assertIn("token", enterprise.errors)

    def test_get_attribute_infos(self):
        """ Get validate with too long attribute """

        enterprise = Enterprise()
        attribute = enterprise.get_attribute_infos('name')

        self.assertIsNotNone(attribute)
        self.assertEqual(attribute.local_name, 'name')

        attribute = enterprise.get_attribute_infos('nope')
        self.assertIsNone(attribute)

    def test_is_owned_by_current_user(self):
        """ """
        enterprise = Enterprise()
        enterprise.owner = 'id'
        root_object = NURESTRootObject.get_default_root_object()
        root_object.id = 'id'

        self.assertTrue(enterprise.is_owned_by_current_user())

        root_object.id = 'not-id'
        self.assertFalse(enterprise.is_owned_by_current_user())

    def test_get_formated_creation_date(self):
        """ """
        enterprise = Enterprise()
        enterprise.creation_date = 1446759052.178411
        self.assertEquals(enterprise.get_formated_creation_date(), 'Nov 2015 05 21:09:52')

        enterprise.creation_date = None
        self.assertEquals(enterprise.get_formated_creation_date(), None)

class CopyTests(TestCase):

    def test_copy(self):
        """ Copy instance """

        enterprise = Enterprise(id='4', name='enterprise')

        enterprise_copy = enterprise.copy()

        self.assertNotEqual(enterprise, enterprise_copy)
        self.assertEqual(enterprise.to_dict(), enterprise_copy.to_dict())

class ComparisonTests(TestCase):

    def test_compare_instance(self):
        """ Compare python instance """

        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise2 = Enterprise(id='4', name='enterprise2')
        enterprise3 = Enterprise(id='5', name='test')

        self.assertTrue(enterprise1 == enterprise1)
        self.assertFalse(enterprise1 == enterprise2)
        self.assertFalse(enterprise1 == enterprise3)
        self.assertFalse(enterprise1 == None)

    def test_instance_equals(self):
        """ Compare instance with equals """

        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise2 = Enterprise(id='4', name='enterprise2')
        enterprise3 = Enterprise(id='5', name='test')

        self.assertTrue(enterprise1.equals(enterprise1))
        self.assertTrue(enterprise1.equals(enterprise2))
        self.assertFalse(enterprise1.equals(enterprise3))
        self.assertFalse(enterprise1.equals(None))

    def test_compare_rest_instance(self):
        """ Compare instance with rest_equals """

        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise2 = Enterprise(id='4', name='enterprise')
        enterprise3 = Enterprise(id='5', name='test')

        self.assertTrue(enterprise1.rest_equals(enterprise1))
        self.assertTrue(enterprise1.rest_equals(enterprise2))
        self.assertFalse(enterprise1.rest_equals(enterprise3))
        self.assertFalse(enterprise1.rest_equals(None))

    def test_parents_relationship(self):
        """ Test is parent obects are correctly set"""
        user = User()

        group1 = Group(id='xxxx-xxxx-xxx', name="group1")

        user.add_child(group1)
        self.assertEquals(group1.parent_object, user)

        user.remove_child(group1)
        self.assertEquals(group1.parent_object, None)

        user.add_child(group1)
        updated_group = Group(id='xxxx-xxxx-xxx', name="group-updated")
        user.update_child(updated_group)

        self.assertEquals(user.groups[0], updated_group)
        self.assertEquals(user.groups[0].name, 'group-updated')

        with self.assertRaises(InternalConsitencyError):
            user.add_child(user)

class FetchersTests(TestCase):

    def test_fetchers(self):
        """ test fetchers registry methods """

        user = User()

        rest_names = user.children_rest_names
        self.assertEquals(rest_names, ['group', 'enterprise'])
        self.assertEquals(user.fetcher_for_rest_name('group'), [])
        self.assertEquals(user.fetcher_for_rest_name('enterprise'), [])

        self.assertEquals(user.fetcher_for_rest_name('nothing'), None)

class GenealogyTests(TestCase):

    def test_genealogic_types(self):
        """
        """
        enterprise1 = Enterprise(id='4', name='enterprise')
        employee = Employee()
        employee.parent_object = enterprise1

        self.assertEquals(employee.genealogic_types(), ['user', 'enterprise'])

    def test_genealogic_ids(self):
        """
        """
        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise1.id = '1'
        employee = Employee()
        employee.id = '2'
        employee.parent_object = enterprise1

        self.assertEquals(employee.genealogic_ids(), ['2', '1'])

    def test_genealogy_contains_type(self):
        """
        """
        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise1.id = '1'
        employee = Employee()
        employee.id = '2'
        employee.parent_object = enterprise1

        self.assertTrue(employee.genealogy_contains_type('enterprise'))

    def test_genealogy_contains_id(self):
        """
        """
        enterprise1 = Enterprise(id='4', name='enterprise')
        enterprise1.id = '1'
        employee = Employee()
        employee.id = '2'
        employee.parent_object = enterprise1

        self.assertTrue(employee.genealogy_contains_id('1'))

    def test_parent_for_matching_rest_name(self):
        """ """
        enterprise1 = Enterprise(id='4', name='enterprise')
        user = User()
        user.parent_object = enterprise1

        self.assertEquals(user.parent_for_matching_rest_name(['enterprise']), enterprise1)
        self.assertIsNone(user.parent_for_matching_rest_name(['not-enterprise']))

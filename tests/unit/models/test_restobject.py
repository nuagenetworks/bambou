# -*- coding:utf-8 -*-

from unittest import TestCase

from restnuage.tests import Company, User

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

        company = Company()
        self.assertEquals(company.get_class_remote_name(), u'company')

    def test_get_resource_name(self):
        """ Get object resource name """

        company = Company()
        self.assertEquals(Company.get_resource_name(), u'companies')

    def test_get_resource_url(self):
        """ Get object resource url """

        company = Company()
        company.id = 4
        self.assertEquals(company.get_resource_url(), u'/companies/4')


class CompressionTests(TestCase):

    def test_to_dict(self):
        """ Get object as dictionary """

        company = Company(id=3, name=u"NewCompany")
        to_dict = company.to_dict()

        self.assertEquals(to_dict['companyName'], u'NewCompany')
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
        to_dict['companyName'] = u'AnotherCompany'
        to_dict['unknownField'] = True
        #to_dict['creationDate'] = '2014-04-25 17:05:34'

        company = Company()
        company.from_dict(to_dict)

        self.assertEquals(company.id, 3)
        self.assertEquals(company.owner, u'Alcatel')
        self.assertEquals(company.name, u'AnotherCompany')
        self.assertEquals(company.name, u'AnotherCompany')






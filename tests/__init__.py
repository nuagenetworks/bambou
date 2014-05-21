# -*- coding:utf-8 -*-

from restnuage.restobject import RESTObject
from restnuage.restuser import RESTBasicUser


class User(RESTBasicUser):
    """ Creates a user object for tests """

    @classmethod
    def get_rest_name(cls):
        """ Provides user classname  """

        return u"me"

    @classmethod
    def is_resource_name_fixed(cls):
        """ set resource name as fixed """

        return True


class Company(RESTObject):
    """ Creates a company object for tests """

    def __init__(self, id=None, name='Alcatel-Lucent'):
        """ Creates a new Company """
        super(Company, self).__init__(id=id)
        self.name = name
        self.invisible = True

        self.expose_attribute(attribute_name='name', rest_name='companyName')

    @classmethod
    def get_rest_name(cls):
        """ Provides company classname  """

        return u"company"

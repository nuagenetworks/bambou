# -*- coding:utf-8 -*-

from bambou import NURESTObject, NURESTRootObject, NURESTFetcher, NURESTSession
from bambou.config import BambouConfig

BambouConfig.set_should_raise_bambou_http_error(True)

__all__ = ['Enterprise', 'EnterprisesFetcher', 'Group', 'User', 'NURESTTestSession']


class Enterprise(NURESTObject):
    """ Creates a enterprise object for tests """

    __rest_name__ = "enterprise"
    __resource_name__ = "enterprises"

    def __init__(self, name=u'NuageNetworks', **kwargs):
        """ Creates a new Enterprise

        """
        super(Enterprise, self).__init__()

        self.id = None
        self.name = name
        self.description = None
        self.allowed_forwarding_classes = None
        self.groups = None
        self.ceo = None
        self.invisible = True

        self.expose_attribute(local_name='name', attribute_type=str, is_required=True)
        self.expose_attribute(local_name='description', attribute_type=str, max_length=255)
        self.expose_attribute(local_name=u"allowed_forwarding_classes", remote_name=u"allowedForwardingClasses", attribute_type=str, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name='groups', remote_name='groups', attribute_type=list)
        self.expose_attribute(local_name='ceo', remote_name='ceo', attribute_type=object)

        self._compute_args(**kwargs)


class EnterprisesFetcher(NURESTFetcher):
    """ Represents a Enterprises fetcher

    """
    @classmethod
    def managed_class(cls):
        """ This fetcher manages NUEnterprise objects

            Returns:
                Returns the NUEnterprise class
        """

        return Enterprise


class Group(NURESTObject):

    __rest_name__ = "group"
    __resource_name__ = "groups"

    def __init__(self, **kwargs):
        """ Creates a group """
        super(Group, self).__init__()

        self.name = None
        self.expose_attribute(local_name='name', remote_name='name', attribute_type=str)

        self.employees = EmployeesFetcher.fetcher_with_object(parent_object=self)

        self._compute_args(**kwargs)


class GroupsFetcher(NURESTFetcher):
    """ Represents a Groups fetcher

    """
    @classmethod
    def managed_class(cls):
        """ This fetcher manages Group objects

            Returns:
                Returns the Group class
        """

        return Group

class Employee(NURESTObject):

    __rest_name__ = "user"
    __resource_name__ = "users"

    def __init__(self, **kwargs):
        """ Creates an employee """

        super(Employee, self).__init__()

        self.firstname = None
        self.lastname = None

        self.expose_attribute(local_name='firstname', remote_name='firstname', attribute_type=str)
        self.expose_attribute(local_name='lastname', remote_name='lastname', attribute_type=str)

        self._compute_args(**kwargs)

class EmployeesFetcher(NURESTFetcher):
    """ Represents a Employees fetcher

    """
    @classmethod
    def managed_class(cls):
        """ This fetcher manages Employee objects

            Returns:
                Returns the Employee class
        """

        return Employee


class User(NURESTRootObject):

    __rest_name__ = "me"

    def __init__(self, **kwargs):
        """ Creates a new user

        """
        super(User, self).__init__()

        self.email = None
        self.firstname = None
        self.lastname = None
        self.enterprise_id = None
        self.enterprise_name = None
        self.role = None
        self.avatar_type = None
        self.avatar_data = None
        self.api_key_expiry = None

        self.enterprises = [];

        self.expose_attribute(local_name='email', remote_name='email', attribute_type=str)
        self.expose_attribute(local_name='firstname', remote_name='firstName', attribute_type=str)
        self.expose_attribute(local_name='lastname', remote_name='lastName', attribute_type=str)
        self.expose_attribute(local_name='enterprise_id', remote_name='enterpriseID', attribute_type=str)
        self.expose_attribute(local_name='enterprise_name', remote_name='enterpriseName', attribute_type=str)
        self.expose_attribute(local_name='role', remote_name='role', attribute_type=str)
        self.expose_attribute(local_name='avatar_type', remote_name='avatarType', attribute_type=str)
        self.expose_attribute(local_name='avatar_data', remote_name='avatarData', attribute_type=str)
        self.expose_attribute(local_name='api_key_expiry', remote_name='APIKeyExpiry', attribute_type=str)

        self.enterprises = EnterprisesFetcher.fetcher_with_object(parent_object=self)
        self.groups = GroupsFetcher.fetcher_with_object(parent_object=self)

        self._compute_args(**kwargs)

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return True

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.rest_resource_name
        url = self.__class__.rest_base_url()
        return "%s/%s" % (url, name)

    def get_resource_url_for_child_type(self, nurest_object_type):
        """ Get the resource url for the nurest_object type """

        return "%s/%s" % (self.__class__.rest_base_url(), nurest_object_type.rest_resource_name)


class NURESTTestSession(NURESTSession):

    def create_rest_user(self):
        """ Creates a new user

        """
        return User()

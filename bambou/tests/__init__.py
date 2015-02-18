# -*- coding:utf-8 -*-

from bambou import NURESTObject, NURESTBasicUser, NURESTFetcher
from bambou.config import BambouConfig
from bambou.utils.decorators import classproperty

BambouConfig.set_should_raise_bambou_http_error(True)

__all__ = ['Enterprise', 'EnterprisesFetcher', 'Group', 'User']


class Enterprise(NURESTObject):
    """ Creates a enterprise object for tests """

    def __init__(self, id=None, name='Alcatel-Lucent'):
        """ Creates a new Enterprise """
        super(Enterprise, self).__init__()
        self.id = id
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

    @classproperty
    def rest_name(cls):
        """ Provides enterprise classname  """

        return u"enterprise"


class EnterprisesFetcher(NURESTFetcher):
    """ Represents a Enterprises fetcher """

    @classmethod
    def managed_class(cls):
        """ This fetcher manages NUEnterprise objects

            Returns:
                Returns the NUEnterprise class
        """

        return Enterprise

class Group(NURESTObject):

    def __init__(self):
        """ Creates a group """
        super(Group, self).__init__()
        self.name = None

        self.expose_attribute(local_name='name', remote_name='name', attribute_type=str)

    @classproperty
    def rest_name(cls):
        """ Provides user classname  """

        return "group"

class User(NURESTBasicUser):

    def __init__(self):
        """ Creates a new user """

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

        self.enterprises = []
        self.enterprises_fetcher = EnterprisesFetcher.fetcher_with_object(nurest_object=self, local_name=u'enterprises')

    @classproperty
    def rest_name(cls):
        """ Provides user classname  """

        return "me"

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return True

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.get_resource_name()
        url = self.__class__.base_url()
        return "%s/%s" % (url, name)

    def get_resource_url_for_child_type(self, nurest_object_type):
        """ Get the resource url for the nurest_object type """

        return "%s/%s" % (self.__class__.base_url(), nurest_object_type.get_resource_name())

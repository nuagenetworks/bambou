# -*- coding:utf-8 -*-

from restnuage import NURESTObject
from restnuage import NURESTBasicUser


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

        self.expose_attribute(local_name='email', remote_name='email', attribute_type=str)
        self.expose_attribute(local_name='firstname', remote_name='firstName', attribute_type=str)
        self.expose_attribute(local_name='lastname', remote_name='lastName', attribute_type=str)
        self.expose_attribute(local_name='enterprise_id', remote_name='enterpriseID', attribute_type=str)
        self.expose_attribute(local_name='enterprise_name', remote_name='enterpriseName', attribute_type=str)
        self.expose_attribute(local_name='role', remote_name='role', attribute_type=str)
        self.expose_attribute(local_name='avatar_type', remote_name='avatarType', attribute_type=str)
        self.expose_attribute(local_name='avatar_data', remote_name='avatarData', attribute_type=str)
        self.expose_attribute(local_name='api_key_expiry', remote_name='APIKeyExpiry', attribute_type=str)

        # Overides from parents because rest name changed
        self.expose_attribute(local_name='user_name', remote_name='userName', attribute_type=str)  # TODO : Declare bug here
        self.expose_attribute(local_name='external_id', remote_name='externalId', attribute_type=str)  # TODO : Declare bug here

    @classmethod
    def get_remote_name(cls):
        """ Provides user classname  """

        return "me"

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return True


class Enterprise(NURESTObject):
    """ Creates a enterprise object for tests """

    def __init__(self, id=None, name='Alcatel-Lucent'):
        """ Creates a new Enterprise """
        super(Enterprise, self).__init__()
        self.id = id
        self.name = name
        self.description = None
        self.invisible = True

        self.expose_attribute(local_name='name', attribute_type=str, is_required=True)
        self.expose_attribute(local_name='description', attribute_type=str)

    @classmethod
    def get_remote_name(cls):
        """ Provides enterprise classname  """

        return u"enterprise"

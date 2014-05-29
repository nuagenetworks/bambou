# -*- coding: utf-8 -*-

import json

from .nurest_connection import NURESTConnection
from .nurest_request import NURESTRequest


class NURESTObject(object):
    """ Determines an object as a NURESTObject one
        Provides basic saving and fetching utilities
    """

    def __init__(self, creation_date=None, external_id=None, id=None, local_id=None, owner=None, parent_id=None, parent_type=None):
        """ Initializes the object with general information

            :param creation_date: datetime when the object as been created
            :param external_id: external identifier of the object
            :param id: identifier of the object
            :param local_id: internal identifier of the object
            :param owner: string representing the owner
            :param parent_id: identifier of the object's parent
            :param parent_type: type of the parent
        """

        self._creation_date = creation_date
        self._external_id = external_id
        self._id = id
        self._local_id = local_id
        self._owner = owner
        self._parent_id = parent_id
        self._parent_type = parent_type
        self._parent = None

        self._childrens = dict()
        self._attributes = dict()

        self.expose_attribute(local_name='id', remote_name='ID')
        self.expose_attribute(local_name='external_id', remote_name='externalID')
        self.expose_attribute(local_name='local_id', remote_name='localID')
        self.expose_attribute(local_name='parent_id', remote_name='parentID')
        self.expose_attribute(local_name='parent_type', remote_name='parentType')
        self.expose_attribute(local_name='creation_date', remote_name='creationDate')
        self.expose_attribute(local_name='owner')

    # Properties

    def _get_creation_date(self):
        """ Get creation date """
        return self._creation_date

    def _set_creation_date(self, creation_date):
        """ Set creation date """
        self._creation_date = creation_date

    creation_date = property(_get_creation_date, _set_creation_date)

    def _get_external_id(self):
        """ Get external id """
        return self._external_id

    def _set_external_id(self, external_id):
        """ Set external id """
        self._external_id = external_id

    external_id = property(_get_external_id, _set_external_id)

    def _get_id(self):
        """ Get object id """
        return self._id

    def _set_id(self, id):
        """ Set object id """
        self._id = id

    id = property(_get_id, _set_id)

    def _get_local_id(self):
        """ Get local id """
        return self._local_id

    def _set_local_id(self, local_id):
        """ Set local id """
        self._local_id = local_id

    local_id = property(_get_local_id, _set_local_id)

    def _get_owner(self):
        """ Get owner """
        return self._owner

    def _set_owner(self, owner):
        """ Set owner """
        self._owner = owner

    owner = property(_get_owner, _set_owner)

    def _get_parent_id(self):
        """ Get parent id """
        return self._parent_id

    def _set_parent_id(self, parent_id):
        """ Set parent id """
        self._parent_id = parent_id

    parent_id = property(_get_parent_id, _set_parent_id)

    def _get_parent_type(self):
        """ Get parent type """
        return self._parent_type

    def _set_parent_type(self, parent_type):
        """ Set parent id """
        self._parent_type = parent_type

    parent_type = property(_get_parent_type, _set_parent_type)

    def _get_parent(self):
        """ Get parent """
        return self._parent

    def _set_parent(self, parent):
        """ Set parent id """
        self._parent = parent

    parent = property(_get_parent, _set_parent)

    # Methods

    @classmethod
    def get_remote_name(cls):
        """ Provides the class name used for resource  """

        raise NotImplementedError('%s has no defined name. Implements get_remote_name method first.' % cls)

    def get_class_remote_name(self):
        """ Provides the resource name of the instance """

        return self.__class__.get_remote_name()

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return False

    @classmethod
    def get_resource_name(cls):
        """ Provides the REST query name based on object's name """

        query_name = cls.get_remote_name()

        if cls.is_resource_name_fixed():
            return query_name

        last_letter = query_name[-1]

        if last_letter == "y":

            vowels = ['a', 'e', 'i', 'o', 'u', 'y']

            if query_name[-2].lower() not in vowels:
            #if query_name[length - 2:] == "ry" or query_name[length - 2:] == "cy" or query_name[length - 2:] == "cy":
                query_name = query_name[:len(query_name) - 1]
                query_name += "ies"

        elif last_letter != "s":
            query_name += "s"

        return query_name

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.get_resource_name()

        if self.id is not None:
            return "/%s/%s" % (name, self.id)

        return "/%s" % name

    def __cmp__(self, rest_object):
        """ Compare with another object """

        if not isinstance(rest_object, NURESTObject):
            raise TypeError('The object is not a NURESTObject %s' % rest_object)

        if self.get_remote_name() != rest_object.get_remote_name():
            return False

        if self.id != rest_object.id:
            return False

        return True

    def __str__(self):
        """ Prints a NURESTObject """

        return "%s (ID=%s)" % (self.__class__, self.id)

    def expose_attribute(self, local_name, remote_name=None):
        """ Expose local_name as remote_name """

        if remote_name is None:
            remote_name = local_name

        self._attributes[local_name] = remote_name

    def is_owned_by_current_user(self):
        """ Check if the current user owns the object """

        from restnuage.nurest_user import NURESTBasicUser
        current_user = NURESTBasicUser()
        return self._owner == current_user.id

    def is_parents_owned_by_current_user(self, remote_names):
        """ Check if the current user owns one of the parents """

        parent = self

        while parent:

            if self.get_class_remote_name() in remote_names and parent.is_owned_by_current_user():
                return True

            parent = parent.parent

        return False

    def parent_with_remote_name_matching(self, remote_names):
        """ Return parent that matches a remote name """

        parent = self

        while parent:
            if parent.get_class_remote_name() in remote_names:
                return parent

            parent = parent.parent

        return None

    def get_formated_creation_date(self, format='mmm dd yyyy HH:MM:ss'):
        """ Return creation date with a given format. Default is 'mmm dd yyyy HH:MM:ss' """

        return self._creation_date.strftime('mmm dd yyyy HH:MM:ss')

    # Compression / Decompression

    def to_dict(self):
        """ Returns a dictionnary of attributes to use for rest calls
            Overrides this method to add your own attributes
        """

        dictionary = dict()

        for local_name, remote_name in self._attributes.iteritems():
            #print "%s -> %s" % (local_name, remote_name)

            if hasattr(self, local_name):
                dictionary[remote_name] = getattr(self, local_name)
            else:
                #print 'Attribute %s could not be found for object %s' % (local_name, self)
                pass

        return dictionary

    def from_dict(self, dictionary):
        """ Fill the current object from dictionary """

        for remote_name, remote_value in dictionary.iteritems():
            # Check if a local attribute is exposed with th remote_name
            # if no attribute is exposed, return None
            local_name = next((key for key, value in self._attributes.iteritems() if value == remote_name), None)

            if local_name:
                setattr(self, local_name, remote_value)
            else:
                #print 'Attribute %s could not be added to object %s' % (remote_name, self)
                pass

    # HTTP Calls

    def delete(self, callback=None, async=False):
        """ Delete object and call given callback """

        self._manage_child_entity(nurest_object=self, method='DELETE', async=async, callback=callback)

    def save(self, callback=None, async=False):
        """ Update object and call given callback """

        self._manage_child_entity(nurest_object=self, method='PUT', async=async, callback=callback)

    def fetch(self, callback=None, async=False):
        """ Fetch all information about the current object """

        request = NURESTRequest(method='GET', url=self.get_resource_url())

        if async:
            self.send_request(request=request, async=async, local_callback=self._did_fetch, remote_callback=callback)
        else:
            connection = self.send_request(request=request, async=async)
            return self._did_fetch(connection)

    # REST HTTP Calls

    def send_request(self, request, async, local_callback=None, remote_callback=None, user_info=None):
        """ Sends the request, calls the local callback, then the remote callback """

        callbacks = dict()

        if local_callback:
            callbacks['local'] = local_callback

        if remote_callback:
            callbacks['remote'] = remote_callback

        connection = NURESTConnection(request=request, callback=self._did_receive_response, callbacks=callbacks, async=async)
        connection.user_info = user_info

        return connection.start()

    def _manage_child_entity(self, nurest_object, resource_url='', method='GET', async=False, callback=None, handler=None):
        """ Low level child management. Send given HTTP method with given entity to given ressource of current object

            :param nurest_object: the NURESTObject object to manage
            :param resource_url: the resource url of the object to manage
            :param method: the HTTP method to use (GET, POST, PUT, DELETE)
            :param callback: the callback to call at the end
            :param handler: a custom handler to call when complete, before calling the callback
        """

        request = None

        from restnuage.nurest_user import NURESTBasicUser
        if isinstance(self, NURESTBasicUser):
            # Creates a url relative to the server base url
            request = NURESTRequest(method=method, url=resource_url, data=nurest_object.to_dict())

        else:
            url = self.get_resource_url() + resource_url  # Creates a url relative to the current object url
            request = NURESTRequest(method=method, url=url, data=nurest_object.to_dict())

        if not handler:
            handler = self._did_perform_standard_operation

        if async:
            self.send_request(request=request, async=async, local_callback=handler, remote_callback=callback, user_info=nurest_object)
        else:
            connection = self.send_request(request=request, async=async, user_info=nurest_object)
            return handler(connection)

    def set_entities(self, nurest_objects, object_type, callback=None):
        """ Reference a list of NURESTObject into the current resource
            :param nurest_objects: list of NURESTObject to link
            :param object_class: Type of the object to link
            :param callback: Callback method that should be fired at the end
        """

        ids = list()

        for nurest_object in nurest_objects:
            ids.push(nurest_object.id)

        data = json.loads(ids)
        url = self.get_resource_url() + object_type.get_remote_name()

        request = NURESTRequest(method="PUT", url=url, data=data)

        self.send_request(request=request,
                           local_callback=self._did_perform_standard_operation,
                           remote_callback=callback,
                           user_info=nurest_objects)

    # REST Operation handlers

    def _did_receive_response(self, connection):
        """ Receive a response from the connection """

        if connection.has_timeouted:
            print "NURESTConnection has timeout."
            # TODO : Should send a notification error message here
            return

        has_callbacks = connection.has_callbacks()
        should_post = not has_callbacks

        if  connection.has_response_success(should_post=should_post) and has_callbacks:
            callback = connection.callbacks['local']
            callback(connection)

    def _did_fetch(self, connection):
        """ Callback called after fetching the object """

        response = connection.response
        self.from_dict(response.data[0])

        return self._did_perform_standard_operation(connection)

    def _did_perform_standard_operation(self, connection):
        """ Performs standard opertions """

        if connection.async:
            callback = connection.callbacks['remote']

            if connection.user_info:
                callback(connection.user_info, connection)
            else:
                callback(self, connection)
        else:

            if connection.user_info:
                return (connection.user_info, connection)

            return (self, connection)

    # Advanced REST Operations

    def add_child_entity(self, entity, async=False, callback=None):
        """ Add given NURESTObject into resource of current object
            for example, to add a NUGroup into a NUEnterprise, you can call
            enterprise.add_child_entity(nurest_object=my_group)

            :param entity: the NURESTObject object to add
            :param callback: callback containing the object and the connection
            :param async: should the request be done asynchronously or not
        """

        return self._manage_child_entity(nurest_object=entity,
                                  resource_url=entity.get_resource_url(),
                                  method='POST',
                                  async=async,
                                  callback=callback,
                                  handler=self._did_add_child_entity)

    def _did_add_child_entity(self, connection):
        """ Callback called after adding a new child entity """

        response = connection.response
        try:
            connection.user_info.from_dict(response.data[0])
        except Exception:
            pass

        return self._did_perform_standard_operation(connection)

    def remove_child_entity(self, entity, async=False, callback=None, response_choice=None):
        """ Removes given NURESTObject into resource from current object
            for example, to remove a NUGroup from a NUEnterprise, you can call
            enterprise.remove_child_entity(nurest_object=my_group)

            :param entity: the NURESTObject object to remove
            :param choice: if a choice has to be made
            :param callback: callback containing the object and the connection
        """

        resource_url = entity.get_resource_url()

        if response_choice:
            resource_url = '%s?responseChoice=%s' % (resource_url, response_choice)

        self._manage_child_entity(nurest_object=entity,
                                  resource_url=resource_url,
                                  method='DELETE',
                                  async=async,
                                  callback=callback)

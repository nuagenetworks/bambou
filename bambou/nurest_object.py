# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""

import inspect
import json

from time import time

from .exceptions import BambouHTTPError
from .nurest_login_controller import NURESTLoginController
from .nurest_connection import NURESTConnection, HTTP_METHOD_DELETE, HTTP_METHOD_PUT, HTTP_METHOD_POST, HTTP_METHOD_GET
from .nurest_fetcher import NURESTFetcher
from .nurest_request import NURESTRequest
from .nurest_modelcontroller import NURESTModelController
from .utils import NURemoteAttribute

from bambou import bambou_logger
from bambou.config import BambouConfig


class NURESTObject(object):
    """ Determines an object as a NURESTObject one
        Provides basic saving and fetching utilities
    """

    def __init__(self, creation_date=None, external_id=None, id=None, local_id=None, owner=None, parent_id=None, parent_type=None):
        """ Initializes the object with general information

            Args:
                creation_date: datetime when the object as been created
                external_id: external identifier of the object
                id: identifier of the object
                local_id: internal identifier of the object
                owner: string representing the owner
                parent_id: identifier of the object's parent
                parent_type: type of the parent
        """

        self._creation_date = creation_date
        self._external_id = external_id
        self._id = id
        self._local_id = local_id
        self._owner = owner
        self._parent_id = parent_id
        self._parent_type = parent_type
        self._parent = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._is_dirty = False

        self._children = dict()
        self._attributes = dict()  # Dictionary of attribute name => NURemoteAttribute

        self.expose_attribute(local_name=u'id', remote_name=u'ID', attribute_type=str, is_identifier=True)
        self.expose_attribute(local_name=u'parent_id', remote_name=u'parentID', attribute_type=str)
        self.expose_attribute(local_name=u'parent_type', remote_name=u'parentType', attribute_type=str)
        self.expose_attribute(local_name=u'creation_date', remote_name=u'creationDate', attribute_type=time, is_editable=False)
        self.expose_attribute(local_name=u'owner', attribute_type=str, is_readonly=True)
        self.expose_attribute(local_name=u'last_updated_date', remote_name=u'lastUpdatedDate', attribute_type=time, is_readonly=True)
        self.expose_attribute(local_name=u'last_updated_by', remote_name=u'lastUpdatedBy', attribute_type=str, is_readonly=True)

        self._children_list_registry = dict()

        model_controller = NURESTModelController.get_default()
        model_controller.register_model(self.__class__)

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
        """ Set parent type """

        self._parent_type = parent_type

    parent_type = property(_get_parent_type, _set_parent_type)

    def _get_parent(self):
        """ Get parent """

        return self._parent

    def _set_parent(self, parent):
        """ Set parent id """

        self._parent = parent

    parent = property(_get_parent, _set_parent)

    def _get_last_updated_by(self):
        """ Get last updated by user id info """

        return self._last_updated_by

    def _set_last_updated_by(self, user_id):
        """ Set last updated by user id info """

        self._last_updated_by = user_id

    last_updated_by = property(_get_last_updated_by, _set_last_updated_by)

    def _get_last_updated_date(self):
        """ Get last updated date """

        return self._last_updated_date

    def _set_last_updated_date(self, update_date):
        """ Set last updated by user id info """

        self._last_updated_date = update_date

    last_updated_date = property(_get_last_updated_date, _set_last_updated_date)

    # Methods

    def get_attributes(self):
        """ Get all attributes information

            Returns:
                Returns a dictionnary containing attribute information
        """

        return self._attributes.values()

    @classmethod
    def get_remote_name(cls):
        """ Provides the class name used for resource

            This method has to be implemented.

            Raises:
                NotImplementedError
        """

        raise NotImplementedError('%s has no defined name. Implements get_remote_name method first.' % cls)

    def get_class_remote_name(self):
        """ Provides the resource name of the instance """

        return self.__class__.get_remote_name()

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return False

    @classmethod
    def object_with_id(cls, id):
        """ Get a new object with the given id

            Returns:
                Returns a new instance with specified id
        """

        new_object = cls()
        new_object.id = id

        return new_object

    @classmethod
    def get_resource_name(cls):
        """ Resource name of the object.

            It will compute the plural if needed

            Returns:
                Returns a string that represents the resouce name of the object
        """

        query_name = cls.get_remote_name()

        if cls.is_resource_name_fixed():
            return query_name

        last_letter = query_name[-1]

        if last_letter == "y":

            vowels = ['a', 'e', 'i', 'o', 'u', 'y']

            if query_name[-2].lower() not in vowels:
                query_name = query_name[:len(query_name) - 1]
                query_name += "ies"

        elif last_letter != "s":
            query_name += "s"

        return query_name

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.get_resource_name()
        url = self.__class__.base_url()

        if self.id is not None:
            return "%s/%s/%s" % (url, name, self.id)

        return "%s/%s" % (url, name)

    def get_resource_url_for_child_type(self, nurest_object_type):
        """ Get the resource url for the nurest_object type """

        return "%s/%s" % (self.get_resource_url(), nurest_object_type.get_resource_name())

    @classmethod
    def base_url(cls):
        """ Override this method to set object base url """

        controller = NURESTLoginController()
        return controller.url

    def __eq__(self, rest_object):
        """ Compare with another object """

        if self._is_dirty:
            return False

        if rest_object is None:
            return False

        if not isinstance(rest_object, NURESTObject):
            raise TypeError('The object is not a NURESTObject %s' % rest_object)

        if self.get_remote_name() != rest_object.get_remote_name():
            return False

        if self.id and rest_object.id:
            return self.id == rest_object.id

        if self.local_id and rest_object.local_id:
            return self.local_id == rest_object.local_id

        return False

    def __str__(self):
        """ Prints a NURESTObject """

        return "%s (ID=%s)" % (self.__class__, self.id)

    def validate(self):
        """ Validate the current object attributes.

            Check all attributes and store errors

            Returns:
                Returns True if all attibutes of the object
                respect contraints. Returns False otherwise and
                store error in errors dict.

        """
        self.errors = dict()

        for local_name, attribute in self._attributes.iteritems():

            value = getattr(self, local_name, None)

            if value is None and attribute.is_required:
                self.errors[local_name] = 'Attribute %s is required' % (local_name)
                continue

            if value is None:
                continue  # without error

            if type(value) != attribute.attribute_type:
                if attribute.attribute_type != str or type(value) != unicode:
                    self.errors[local_name] = 'Attribute %s is not of type %s' % (local_name, attribute.attribute_type)
                    continue

            if attribute.min_length and len(value) < attribute.min_length:
                self.errors[local_name] = 'Attribute %s length is too short (minimum=%s)' % (local_name, attribute.min_length)
                continue

            if attribute.max_length and len(value) > attribute.max_length:
                self.errors[local_name] = 'Attribute %s length is too long (maximum=%s)' % (local_name, attribute.max_length)
                continue

            if attribute.choices and value not in attribute.choices:
                self.errors[local_name] = 'Attribute %s is not a valid option (choices=%s)' % (local_name, attribute.choices)
                continue

        return len(self.errors) == 0

    def expose_attribute(self, local_name, attribute_type, remote_name=None, display_name=None, is_required=False, is_readonly=False, max_length=None, min_length=None, is_identifier=False, choices=None, is_unique=False, is_email=False, is_login=False, is_editable=True, is_password=False, can_order=False, can_search=False):
        """ Expose local_name as remote_name

            An exposed attribute `local_name` will be sent within the HTTP request as
            a `remote_name`
        """

        if remote_name is None:
            remote_name = local_name

        if display_name is None:
            display_name = local_name

        attribute = NURemoteAttribute(local_name=local_name, remote_name=remote_name, attribute_type=attribute_type)
        attribute.display_name = display_name
        attribute.is_required = is_required
        attribute.is_readonly = is_readonly
        attribute.min_length = min_length
        attribute.max_length = max_length
        attribute.is_editable = is_editable
        attribute.is_identifier = is_identifier
        attribute.choices = choices
        attribute.is_unique = is_unique
        attribute.is_email = is_email
        attribute.is_login = is_login
        attribute.is_password = is_password
        attribute.can_order = can_order
        attribute.can_search = can_search

        self._attributes[local_name] = attribute

    def get_attribute_infos(self, local_name):
        """ Get exposed attribute information

            Args:
                local_name: the attribute name

            Returns:
                A dictionary of all information

        """
        if local_name in self._attributes:
            return self._attributes[local_name]

        return None

    def is_owned_by_current_user(self):
        """ Check if the current user owns the object """

        from bambou.nurest_user import NURESTBasicUser
        current_user = NURESTBasicUser.get_default_user()
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

    def _genealogic_types(self):
        """ Get genealogic types

            Returns:
                Returns a list of all parent types
        """

        types = []
        parent = self

        while parent:
            types.push(parent.get_resource_name())
            parent = parent.parent

        return types

    def _genealogic_ids(self):
        """ Get all genealogic ids

            Returns:
                 A list of all parent ids
        """

        ids = []
        parent = self

        while parent:
            ids.push(parent.id)
            parent = parent.parent

        return ids

    def _genealogy_contains_type(self, resource_name):
        """ Check if parents contains an object of type resource_name

            Args:
                resource_name: the name of the resource to find

            Returns:
                Returns True if a parent of type has been found. False otherwise.
        """

        resource_names = self._genealogic_types()
        return resource_name in resource_names

    def _genealogy_contains_id(self, id):
        """ Check if parents contains an object of type resource_name

            Args:
                id: the id of the resource to find

            Returns:
                Returns True if a parent with specific id has been found. False otherwise.
        """

        ids = self._genealogic_ids()
        return id in ids

    def get_formated_creation_date(self, format='mmm dd yyyy HH:MM:ss'):
        """ Return creation date with a given format. Default is 'mmm dd yyyy HH:MM:ss' """

        if not self._creation_date:
            return u"No date"

        return self._creation_date.strftime('mmm dd yyyy HH:MM:ss')

    # Memory management

    def discard(self):
        """ Discard the current object and its children """

        if self._is_dirty:
            return

        self._is_dirty = True

        bambou_logger.debug("[Bambou] Discarding object %s of type %s" % (self.id, self.get_remote_name()))

        self._discard_all_children_list()
        self._parent = None
        self._children_list_registry = dict()

    def _discard__children_with_resource_name(self, resource_name):
        """ Discard children with a given resource name

            Args:
                resource_name: the resource name

        """
        bambou_logger.debug("[Bambou] %s with id %s is discarding children list %s" % (self.remote_name, self._id, resource_name))
        self._children_list_registry[resource_name] = []

    def _discard_all_children_lists(self):
        """ Discard current object children """

        for resource_name in self._children_list_registry.keys():
            self._discard__children_with_resource_name(resource_name)

    def _register_children_list(self, children, resource_name):
        """ Register children of the current object

            Args:
                children: List of NURESTObject instances
                resource_name: Name of the children resource
        """

        self._children_list_registry[resource_name] = children

    def _children_with_resource_name(self, resource_name):
        """ Get all children according to the given resource_name

            Args:
                resource_name: the name of the resource

            Returns:
                Returns a list of children. If no children has been found,
                returns an empty list.
        """

        if resource_name not in self._children_list_registry:
            return []

        return self._children_list_registry[resource_name]

    # Children management

    def register_children(self, children, local_name):
        """ Register a list of children to the local name """

        self._children[local_name] = children

    def get_children(self, local_name):
        """ Retrieve children according to local name """

        if local_name in self._children:
            return self._children[local_name]

        return []

    def _add_child(self, child):
        """ Add a child """

        local_name = child.get_remote_name()
        children = self.get_children(local_name)

        if child not in children:
            children.append(child)

    def _remove_child(self, child):
        """ Remove a child """

        local_name = child.get_remote_name()
        children = self.get_children(local_name)
        children.remove(child)

    def _update_child(self, child):
        """ Update child """

        local_name = child.get_remote_name()
        children = self.get_children(local_name)
        index = children.index(child)
        children[index] = child

    # Compression / Decompression

    def to_dict(self):
        """ Returns a dictionnary of attributes to use for rest calls
            Overrides this method to add your own attributes
        """

        dictionary = dict()

        for local_name, attribute in self._attributes.iteritems():
            remote_name = attribute.remote_name

            if hasattr(self, local_name):
                value = getattr(self, local_name)

                # Removed to resolve issue http://mvjira.mv.usa.alcatel.com/browse/VSD-5940 (12/15/2014)
                # if isinstance(value, bool):
                #     value = int(value)

                if isinstance(value, NURESTObject):
                    value = value.to_dict()

                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], NURESTObject):
                    tmp = list()
                    for obj in value:
                        tmp.append(obj.to_dict())

                    value = tmp

                dictionary[remote_name] = value
            else:
                # print('Attribute %s could not be found for object %s' % (local_name, self))
                pass

        return dictionary

    def from_dict(self, dictionary):
        """ Fill the current object from dictionary """

        for remote_name, remote_value in dictionary.iteritems():
            # Check if a local attribute is exposed with the remote_name
            # if no attribute is exposed, return None
            local_name = next((name for name, attribute in self._attributes.iteritems() if attribute.remote_name == remote_name), None)

            if local_name:
                setattr(self, local_name, remote_value)
            else:
                # print('Attribute %s could not be added to object %s' % (remote_name, self))
                pass

    # HTTP Calls

    def delete(self, response_choice=None, async=False, callback=None):
        """ Delete object and call given callback in case of async call.

            Args:
                recursive: Set to True to try to delete all children.
                async: Boolean to make an asynchronous call. Default is False
                callback: Callback method that will be triggered in case of asynchronous call
                response_choice: Automatically send a response choice when confirmation is needed

        """
        return self._manage_child_object(nurest_object=self, method=HTTP_METHOD_DELETE, async=async, callback=callback, response_choice=response_choice)

    def save(self, async=False, callback=None):
        """ Update object and call given callback in case of async call

            Args:
                async: Boolean to make an asynchronous call. Default is False
                callback: Callback method that will be triggered in case of asynchronous call

        """
        return self._manage_child_object(nurest_object=self, method=HTTP_METHOD_PUT, async=async, callback=callback)

    def fetch(self, async=False, callback=None):
        """ Fetch all information about the current object

            Args:
                async: Boolean to make an asynchronous call. Default is False
                callback: Callback method that will be triggered in case of asynchronous call

        """
        request = NURESTRequest(method=HTTP_METHOD_GET, url=self.get_resource_url())

        if async:
            self.send_request(request=request, async=async, local_callback=self._did_fetch, remote_callback=callback)
        else:
            connection = self.send_request(request=request, async=async)
            return self._did_fetch(connection)

    # REST HTTP Calls

    def send_request(self, request, async, local_callback=None, remote_callback=None, user_info=None):
        """ Sends a request, calls the local callback, then the remote callback in case of async call

            Args:
                request: The request to send
                async: Boolean to make an asynchronous call.
                local_callback: local method that will be triggered in case of async call
                remote_callback: remote moethd that will be triggered in case of async call
                user_info: contains additionnal information to carry during the request

            Returns:
                Returns the object and connection (object, connection)
        """

        callbacks = dict()

        if local_callback:
            callbacks['local'] = local_callback

        if remote_callback:
            callbacks['remote'] = remote_callback

        connection = NURESTConnection(request=request, callback=self._did_receive_response, callbacks=callbacks, async=async)
        connection.user_info = user_info

        bambou_logger.info('Bambou Sending >>>>>>\n%s %s with following data:\n%s' % (request.method, request.url, json.dumps(request.data, indent=4)))

        return connection.start()

    def _manage_child_object(self, nurest_object, method=HTTP_METHOD_GET, async=False, callback=None, handler=None, response_choice=None):
        """ Low level child management. Send given HTTP method with given nurest_object to given ressource of current object

            Args:
                nurest_object: the NURESTObject object to manage
                method: the HTTP method to use (GET, POST, PUT, DELETE)
                async: True or False to make an asynchronous request
                callback: the callback to call at the end
                handler: a custom handler to call when complete, before calling the callback

            Returns:
                Returns the object and connection (object, connection)
        """

        # Force asynchronous request when having a callback
        if callback:
            async = True

        url = None

        if method == HTTP_METHOD_POST:
            url = self.get_resource_url_for_child_type(nurest_object.__class__)
        else:
            url = self.get_resource_url()

            if method == HTTP_METHOD_DELETE and response_choice is not None:
                url += '?responseChoice=%s' % response_choice

        request = NURESTRequest(method=method, url=url, data=nurest_object.to_dict())

        if not handler:
            handler = self._did_perform_standard_operation

        if async:
            self.send_request(request=request, async=async, local_callback=handler, remote_callback=callback, user_info=nurest_object)
        else:
            connection = self.send_request(request=request, async=async, user_info=nurest_object)
            return handler(connection)

    def assign_objects(self, objects, nurest_object_type, async=False, callback=None):
        """ Reference a list of objects into the current resource

            Args:
                objects: list of NURESTObject to link
                nurest_object_type: Type of the object to link
                callback: Callback method that should be fired at the end

            Returns:
                Returns the current object and the connection (object, connection)
        """

        if len(objects) == 0:
            return

        ids = list()

        for nurest_object in objects:
            ids.append(nurest_object.id)

        url = self.get_resource_url_for_child_type(nurest_object_type)

        request = NURESTRequest(method=HTTP_METHOD_PUT, url=url, data=ids)

        if async:
            self.send_request(request=request,
                              local_callback=self._did_perform_standard_operation,
                              async=async,
                              remote_callback=callback,
                              user_info=objects)
        else:
            connection = self.send_request(request=request,
                                           async=async,
                                           user_info=objects)

            return self._did_perform_standard_operation(connection)

    # REST Operation handlers

    def _did_receive_response(self, connection):
        """ Receive a response from the connection """

        if connection.has_timeouted:
            bambou_logger.info("NURESTConnection has timeout.")
            return

        has_callbacks = connection.has_callbacks()
        should_post = not has_callbacks

        bambou_logger.info('Bambou <<<<< Response for\n%s %s\n%s' % (connection._request.method, connection._request.url, json.dumps(connection._response.data, indent=4)))

        if  connection.handle_response_for_connection(should_post=should_post) and has_callbacks:
            callback = connection.callbacks['local']
            callback(connection)

    def _did_fetch(self, connection):
        """ Callback called after fetching the object """

        response = connection.response

        try:
            self.from_dict(response.data[0])
        except:
            pass

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
            if connection.response.status_code >= 400 and BambouConfig._should_raise_bambou_http_error:
                raise BambouHTTPError(connection=connection)

            if connection.user_info:
                return (connection.user_info, connection)

            return (self, connection)

    # Advanced REST Operations

    def add_child_object(self, nurest_object, async=False, callback=None):
        """ Add given nurest_object to the current object

            For example, to add a NUGroup into a NUEnterprise, you can call
            enterprise.add_child_object(nurest_object=my_group)

            Args:
                nurest_object: the NURESTObject object to add
                async: should the request be done asynchronously or not
                callback: callback containing the object and the connection

            Returns:
                Returns the object and connection (object, connection)
        """

        return self._manage_child_object(nurest_object=nurest_object,
                                  method=HTTP_METHOD_POST,
                                  async=async,
                                  callback=callback,
                                  handler=self._did_add_child_object)

    def instantiate_child_object(self, nurest_object, from_template, async=False, callback=None):
        """ Instantiate an nurest_object from a template object

            Args:
                nurest_object: the NURESTObject object to add
                from_template: the NURESTObject template object
                async: should the request be done asynchronously or not
                callback: callback containing the object and the connection

            Returns:
                Returns the object and connection (object, connection)
        """

        nurest_object.template_id = from_template.id
        return self._manage_child_object(nurest_object=nurest_object,
                                  method=HTTP_METHOD_POST,
                                  async=async,
                                  callback=callback,
                                  handler=self._did_add_child_object)

    def _did_add_child_object(self, connection):
        """ Callback called after adding a new child nurest_object """

        response = connection.response
        try:
            connection.user_info.from_dict(response.data[0])
        except Exception:
            pass

        return self._did_perform_standard_operation(connection)

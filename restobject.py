# -*- coding: utf-8 -*-

from restnuage.restconnection import RESTConnection


class RESTObject(object):
    """ Determines an object as a RESTObject one
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
        self.parent = None

        self._childrens = dict()
        self._attributes = dict()

        self.expose_attribute(attribute_name='id', rest_name='ID')
        self.expose_attribute(attribute_name='external_id', rest_name='externalID')
        self.expose_attribute(attribute_name='local_id', rest_name='localID')
        self.expose_attribute(attribute_name='parent_id', rest_name='parentID')
        self.expose_attribute(attribute_name='parent_type', rest_name='parentType')
        self.expose_attribute(attribute_name='creation_date', rest_name='creationDate')
        self.expose_attribute(attribute_name='owner')

    # Properties

    def get_creation_date(self):
        """ Get creation date """
        return self._creation_date

    def set_creation_date(self, creation_date):
        """ Set creation date """
        self._creation_date = creation_date

    creation_date = property(get_creation_date, set_creation_date)

    def get_external_id(self):
        """ Get external id """
        return self._external_id

    def set_external_id(self, external_id):
        """ Set external id """
        self._external_id = external_id

    external_id = property(get_external_id, set_external_id)

    def get_id(self):
        """ Get object id """
        return self._id

    def set_id(self, id):
        """ Set object id """
        self._id = id

    id = property(get_id, set_id)

    def get_local_id(self):
        """ Get local id """
        return self._local_id

    def set_local_id(self, local_id):
        """ Set local id """
        self._local_id = local_id

    local_id = property(get_local_id, set_local_id)

    def get_owner(self):
        """ Get owner """
        return self._owner

    def set_owner(self, owner):
        """ Set owner """
        self._owner = owner

    owner = property(get_owner, set_owner)

    def get_parent_id(self):
        """ Get parent id """
        return self._parent_id

    def set_parent_id(self, parent_id):
        """ Set parent id """
        self._parent_id = parent_id

    parent_id = property(get_parent_id, set_parent_id)

    def get_parent_type(self):
        """ Get parent type """
        return self._parent_type

    def set_parent_type(self, parent_type):
        """ Set parent id """
        self._parent_type = parent_type

    parent_type = property(get_parent_type, set_parent_type)

    def get_parent(self):
        """ Get parent """
        return self._parent

    def set_parent(self, parent):
        """ Set parent id """
        self._parent = parent

    parent = property(get_parent, set_parent)

    # Methods

    @classmethod
    def get_rest_name(cls):
        """ Provides the class name used for resource  """

        raise NotImplementedError('%s has no defined name. Implements get_rest_name method first.' % cls)

    def get_class_rest_name(self):
        """ Provides the resource name of the instance """

        return self.__class__.get_rest_name()

    @classmethod
    def is_resource_name_fixed(cls):
        """ Boolean to say if the resource name should be fixed. Default is False """

        return False

    @classmethod
    def get_resource_name(cls):
        """ Provides the REST query name based on object's name """

        query_name = cls.get_rest_name()

        if cls.is_resource_name_fixed():
            return query_name

        last_letter = query_name[-1]

        if last_letter == "y":

            length = len(query_name)
            #if query_name[length - 2:] == "ry" or query_name[length - 2:] == "cy":
            query_name = query_name[:length - 1]
            query_name += "ies"

        elif last_letter != "s":
            query_name += "s"

        return query_name

    def get_resource_url(self):
        """ Get resource complete url """

        name = self.__class__.get_resource_name()

        if self.id:
            return "/%s/%s" % (name, self.id)

        return "/%s" % name

    def __cmp__(self, rest_object):
        """ Compare with another object """

        if type(rest_object) is not RESTObject:
            raise TypeError('The object is not a RESTObject %s' % rest_object)

        if self.name != rest_object.name:
            return False

        if self.id != rest_object.id:
            return False

        return True

    def __str__(self):
        """ Prints a RESTObject """

        return "%s (ID=%s)" % (self.__class__, self.id)

    def expose_attribute(self, attribute_name, rest_name=None):
        """ Expose attribute_name as rest_name """

        if rest_name is None:
            rest_name = attribute_name

        self._attributes[attribute_name] = rest_name

    def is_owned_by_current_user(self):
        """ Check if the current user owns the object """

        #return self._owner ==
        raise NotImplementedError('Not implemented yet')

    def is_parents_owned_by_current_user(self, parents):
        """ Check if the current user owns one of the parents """

        raise NotImplementedError('Not implemented yet')

    def parent_with_rest_name_matching(self, restnames):
        """ Return parent that matches a restnames """

        parent = self

        while parent:
            if parent.name in restnames:
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

        for attribute_name, rest_name in self._attributes.iteritems():
            #print "%s -> %s" % (attribute_name, rest_name)

            if hasattr(self, attribute_name):
                dictionary[rest_name] = getattr(self, attribute_name)
            else:
                print 'Attribute %s could not be found for object %s' % (attribute_name, self)

        return dictionary

    def from_dict(self, dictionary):
        """ Fill the current object from dictionary """

        for rest_name, rest_value in dictionary.iteritems():
            attribute_name = next((key for key, value in self._attributes.iteritems() if value == rest_name), None)

            if attribute_name:
                setattr(self, attribute_name, rest_value)
            else:
                print 'Attribute %s could not be added to object %s' % (rest_name, self)

    # Childrens' management

    def add_child(self, rest_object):
        """ Add rest_object as a child """

        if type(rest_object) is not RESTObject:
            raise TypeError('The object is not a RESTObject %s' % rest_object)

        if rest_object.__class__ not in self._childrens:
            self._childrens[rest_object.__class__] = []

        self._childrens[rest_object.__class__].append(rest_object)

    def remove_child(self, rest_object):
        """ Removes rest_object from childrens """

        if type(rest_object) is not RESTObject:
            raise TypeError('The object is not a RESTObject %s' % rest_object)

        if rest_object.__class__ in self._childrens:
            self._childrens[rest_object.__class__].remove(rest_object)

    def update_child(self, rest_object):
        """ Updates rest_object """

        if type(rest_object) is not RESTObject:
            raise TypeError('The object is not a RESTObject %s' % rest_object)

        if rest_object.__class__ in self._childrens:
            index = self._childrens[rest_object.__class__].index(rest_object)
            self.remove_child(rest_object)
            self._childrens[rest_object.__class__].insert(index, rest_object)

    # HTTP Calls

    def fetch(self, callback):
        """ Fetch all information about the current object """

        print "** Call fetch"
        self._callback = callback
        connection = RESTConnection()
        connection.get(resource_url=self.get_resource_url(), params=self.to_dict(), callback=self._did_fetch)


    def _did_fetch(self, response):
        """ Callback called after fetching the object """

        print "** Fetch callback"
        dictionary = response.json()[0]
        self.from_dict(dictionary)

        if self._callback:
            self._callback()
            self._callback = None

    def create(self, callback=None):
        """ Creates object and perform the callback method """

        connection = RESTConnection()
        connection.create(resource_url=self.get_resource_url(), data=self.to_dict(), callback=callback)

    def delete(self, callback=None):
        """ Deletes object and perform the callback method """

        connection = RESTConnection()
        connection.delete(resource_url=self.get_resource_url(), data=self.to_dict(), callback=callback)

    def save(self, callback=None):
        """ Updates the object and perform the callback method """

        connection = RESTConnection()
        connection.update(resource_url=self.get_resource_url(), data=self.to_dict(), callback=callback)

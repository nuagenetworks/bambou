# -*- coding: utf-8 -*-

#
# Copyright (c) 2015, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import weakref
from .exceptions import BambouHTTPError, InternalConsitencyError
from .nurest_request import NURESTRequest
from .nurest_connection import HTTP_METHOD_GET, HTTP_METHOD_HEAD

from bambou.config import BambouConfig


class NURESTFetcher(list):
    """ Object fetcher for childrens

        This object is intended to fetch a specific type of object declared
        by `managed_class` method
    """

    PAGE_SIZE = 50

    def __init__(self):
        """ Initliazes the fetcher """

        super(NURESTFetcher, self).__init__()

        self._relationship = "child"
        self.current_connection = None
        self.current_ordered_by = ''
        self.current_page = 0
        self.current_total_count = 0
        self._parent_object = None

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, super(NURESTFetcher, self).__repr__())

    def __contains__(self, nurest_object):
        """ Verify if the fetcher contains the given NURESTObject

            Args:
                nurest_object (bambou.NURESTObject): the NURESTObject object to verify

            Returns:
                Returns True if the object has been found. False otherwise

        """
        for obj in self:
            if obj.equals(nurest_object):
                return True

        return False

    def index(self, nurest_object):
        """ Get index of the given item
            Args:
                nurest_object (bambou.NURESTObject): the NURESTObject object to verify

            Returns:
                Returns the position of the object.

            Raises:
                Raise a ValueError exception if object is not present
        """
        for index, obj in enumerate(self):
            if obj.equals(nurest_object):
                return index

        raise ValueError("%s is  not in %s" % (nurest_object, self))

    # Properties

    @property
    def parent_object(self):
        """ Get served object

            The fetcher will fill the served object with fetched objects

            Returns:
                Returns the object it is serving.
        """

        return self._parent_object() if self._parent_object else None

    @parent_object.setter
    def parent_object(self, parent_object):
        """ Set the served object

            Args:
                parent_object: the object to serve
        """

        self._parent_object = weakref.ref(parent_object) if parent_object else None

    @property
    def transaction_id(self):
        """ Get the transaction ID of the current connection

            Returns:
                the transaction id
        """
        if self.current_connection is None:
            raise InternalConsitencyError("%s could not find a current transaction." % self)

        return self.current_connection.transaction_id

    @property
    def relationship(self):
        """ Get relationship of the fetcher's owner and the fetched objects

            Returns:
                Returns the relationship.
        """

        return self._relationship

    @relationship.setter
    def relationship(self, relationship):
        """ Set the relationship

            Args:
                relationship: the relationship

        """

        self._relationship = relationship

    # Methods

    @classmethod
    def managed_class(cls):
        """ Defines the object type that is managed by this fetcher.

            This method has to be overrided to indicate which object the fetcher
            is allowed to fetch.

            Returns:
                Returns a type of NURESTObject

            Raises:
                NotImplementedError: if this method is not overriden

        """

        raise NotImplementedError('%s has no managed class. Implements managed_class method first.' % cls)

    @classmethod
    def managed_object_rest_name(cls):
        """ Remote name of the managed object

            Returns:
                Returns a string representing the resource name of the object
                that has to be fetched.
        """

        return cls.managed_class().rest_name

    @classmethod
    def fetcher_with_object(cls, parent_object, relationship="child"):
        """ Register the fetcher for a served object.

            This method will fill the fetcher with `managed_class` instances

            Args:
                parent_object: the instance of the parent object to serve

            Returns:
                It returns the fetcher instance.
        """

        fetcher = cls()
        fetcher.parent_object = parent_object
        fetcher.relationship = relationship

        rest_name = cls.managed_object_rest_name()
        parent_object.register_fetcher(fetcher, rest_name)

        return fetcher

    def flush(self):
        """ Removes all fetched objects

            It will clear attribute of the served object
        """
        self.current_connection = None
        del self[:]

    def new(self):
        """ Create an instance of the managed class

            Returns:
                Returns an instance of managed_class
        """

        managed_class = self.managed_class()
        return managed_class()

    def _prepare_headers(self, request, filter=None, order_by=None, group_by=[], page=None, page_size=None):
        """ Prepare headers for the given request

            Args:
                request: the NURESTRequest to send
                filter: string
                order_by: string
                group_by: list of names
                page: int
                page_size: int
        """

        if filter:
            request.set_header('X-Nuage-Filter', filter)

        if order_by:
            request.set_header('X-Nuage-OrderBy', order_by)

        if page:
            request.set_header('X-Nuage-Page', str(page))

        if page_size:
            request.set_header('X-Nuage-PageSize', str(page_size))

        if len(group_by) > 0:
            header = ", ".join(group_by)
            request.set_header('X-Nuage-GroupBy', 'true')
            request.set_header('X-Nuage-Attributes', header)

    def _prepare_url(self):
        """ Prepare url for request """

        return self.parent_object.get_resource_url_for_child_type(self.__class__.managed_class())

    def fetch(self, filter=None, order_by=None, group_by=[], page=None, page_size=None, query_parameters=None, commit=True, async=False, callback=None):
        """ Fetch objects according to given filter and page.

            Note:
                This method fetches all managed class objects and store them
                in local_name of the served object. which means that the parent
                object will hold them in a list. You can prevent this behavior
                by setting commit to False. In that case, the fetched children
                won't be added in the parent object cache.

            Args:
                filter (string): string that represents a predicate filter
                order_by (string): string that represents an order by clause
                group_by (string): list of names for grouping
                page (int): number of the page to load
                page_size (int): number of results per page
                commit (bool): boolean to update current object
                callback (function): Callback that should be called in case of a async request

            Returns:
                tuple: Returns a tuple of information (fetcher, served object, fetched objects, connection)

            Example:
                >>> entity.children.fetch()
                (<NUChildrenFetcher at aaaa>, <NUEntity at bbbb>, [<NUChildren at ccc>, <NUChildren at ddd>], <NURESTConnection at zzz>)
        """

        request = NURESTRequest(method=HTTP_METHOD_GET, url=self._prepare_url(), params=query_parameters)

        self._prepare_headers(request=request, filter=filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size)

        if async:
            return self.parent_object.send_request(request=request, async=async, local_callback=self._did_fetch, remote_callback=callback, user_info={'commit': commit})

        connection = self.parent_object.send_request(request=request, user_info={'commit': commit})
        return self._did_fetch(connection=connection)

    def _did_fetch(self, connection):
        """ Fetching objects has been done """

        self.current_connection = connection
        response = connection.response
        should_commit = 'commit' not in connection.user_info or connection.user_info['commit']

        if connection.response.status_code >= 400 and BambouConfig._should_raise_bambou_http_error:
            raise BambouHTTPError(connection=connection)

        if response.status_code != 200:

            if should_commit:
                self.current_total_count = 0
                self.current_page = 0
                self.current_ordered_by = ''

            return self._send_content(content=None, connection=connection)

        results = response.data
        fetched_objects = list()
        current_ids = list()

        if should_commit:
            if 'X-Nuage-Count' in response.headers and response.headers['X-Nuage-Count']:
                self.current_total_count = int(response.headers['X-Nuage-Count'])

            if 'X-Nuage-Page' in response.headers and response.headers['X-Nuage-Page']:
                self.current_page = int(response.headers['X-Nuage-Page'])

            if 'X-Nuage-OrderBy' in response.headers and response.headers['X-Nuage-OrderBy']:
                self.current_ordered_by = response.headers['X-Nuage-OrderBy']

        if results:
            for result in results:
                nurest_object = self.new()
                nurest_object.from_dict(result)
                nurest_object.parent = self.parent_object

                fetched_objects.append(nurest_object)

                if not should_commit:
                    continue

                current_ids.append(nurest_object.id)

                if nurest_object in self:
                    idx = self.index(nurest_object)
                    current_object = self[idx]
                    current_object.from_dict(nurest_object.to_dict())
                else:
                    self.append(nurest_object)

            if should_commit:
                for obj in self:
                    if obj.id not in current_ids:
                        self.remove(obj)

        return self._send_content(content=fetched_objects, connection=connection)

    def get(self, filter=None, order_by=None, group_by=[], page=None, page_size=None, query_parameters=None, commit=True, async=False, callback=None):
        """ Fetch object and directly return them

            Note:
                `get` won't put the fetched objects in the parent's children list.
                You cannot override this behavior. If you want to commit them in the parent
                you can use :method:vsdk.NURESTFetcher.fetch or manually add the list with
                :method:vsdk.NURESTObject.add_child

            Args:
                filter (string): string that represents a predicate filter
                order_by (string): string that represents an order by clause
                group_by (string): list of names for grouping
                page (int): number of the page to load
                page_size (int): number of results per page
                commit (bool): boolean to update current object
                callback (function): Callback that should be called in case of a async request

            Returns:
                list: list of vsdk.NURESTObject if any

            Example:
                >>> print entity.children.get()
                [<NUChildren at xxx>, <NUChildren at yyyy>, <NUChildren at zzz>]
        """
        return self.fetch(filter=filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size, query_parameters=query_parameters, commit=commit)[2]

    def get_first(self, filter=None, order_by=None, group_by=[], query_parameters=None, commit=False, async=False, callback=None):
        """ Fetch object and directly return the first one

            Note:
                `get_first` won't put the fetched object in the parent's children list.
                You cannot override this behavior. If you want to commit it in the parent
                you can use :method:vsdk.NURESTFetcher.fetch or manually add it with
                :method:vsdk.NURESTObject.add_child

            Args:
                filter (string): string that represents a predicate filter
                order_by (string): string that represents an order by clause
                group_by (string): list of names for grouping
                page (int): number of the page to load
                page_size (int): number of results per page
                commit (bool): boolean to update current object
                callback (function): Callback that should be called in case of a async request

            Returns:
                vsdk.NURESTObject: the first object if any, or None

            Example:
                >>> print entity.children.get_first(filter="name == 'My Entity'")
                <NUChildren at xxx>
        """
        objects = self.get(filter=filter, order_by=order_by, group_by=group_by, page=0, page_size=1, query_parameters=query_parameters, commit=commit)
        return objects[0] if len(objects) else None

    def count(self, filter=None, order_by=None, group_by=[], page=None, page_size=None, query_parameters=None, async=False, callback=None):
        """ Get the total count of objects that can be fetched according to filter

            This method can be asynchronous and trigger the callback method
            when result is ready.

            Args:
                filter (string): string that represents a predicate fitler (eg. name == 'x')
                order_by (string): string that represents an order by clause
                group_by (string): list of names for grouping
                page (int): number of the page to load
                page_size (int): number of results per page
                callback (function): Method that will be triggered asynchronously

            Returns:
                Returns a transaction ID when asynchronous call is made.
                Otherwise it will return a tuple of information containing
                (fetcher, served object, count of fetched objects)
        """
        request = NURESTRequest(method=HTTP_METHOD_HEAD, url=self._prepare_url(), params=query_parameters)

        self._prepare_headers(request=request, filter=filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size)

        if async:
            return self.parent_object.send_request(request=request, async=async, local_callback=self._did_count, remote_callback=callback)

        else:
            connection = self.parent_object.send_request(request=request)
            return self._did_count(connection)

    def get_count(self, filter=None, order_by=None, group_by=[], page=None, page_size=None, query_parameters=None):
        """ Get the total count of objects that can be fetched according to filter

            Args:
                filter (string): string that represents a predicate fitler (eg. name == 'x')
                order_by (string): string that represents an order by clause
                group_by (string): list of names for grouping
                page (int): number of the page to load
                page_size (int): number of results per page

            Returns:
                Returns the number of objects found

        """
        return self.count(filter=filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size, query_parameters=query_parameters, async=False)[2]

    def _did_count(self, connection):
        """ Called when count if finished """

        self.current_connection = connection
        response = connection.response
        count = 0
        callback = None

        if 'X-Nuage-Count' in response.headers:
            count = int(response.headers['X-Nuage-Count'])

        if 'remote' in connection.callbacks:
            callback = connection.callbacks['remote']

        if connection.async:
            if callback:
                callback(self, self.parent_object, count)

                self.current_connection.reset()
                self.current_connection = None
        else:

            if connection.response.status_code >= 400 and BambouConfig._should_raise_bambou_http_error:
                raise BambouHTTPError(connection=connection)

            return (self, self.parent_object, count)

    def _send_content(self, content, connection):
        """ Send a content array from the connection """

        if connection:

            if connection.async:
                callback = connection.callbacks['remote']

                if callback:
                    callback(self, self.parent_object, content)

                    self.current_connection.reset()
                    self.current_connection = None
            else:
                return (self, self.parent_object, content)

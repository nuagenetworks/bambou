# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""

import uuid

from .exceptions import BambouHTTPError
from .nurest_request import NURESTRequest
from .nurest_connection import HTTP_METHOD_GET, HTTP_METHOD_HEAD

from bambou.config import BambouConfig


class NURESTFetcher(object):
    """ Object fetcher for childrens

        This object is intended to fetch a specific type of object declared
        by `managed_class` method
    """

    PAGE_SIZE = 50

    def __init__(self):
        """ Initliazes the fetcher """

        self.latest_loaded_page = 0
        self.nurest_object = None
        self.ordered_by = ''
        self.query_string = None
        self.total_count = 0
        self._current_connection = None
        self._local_name = None
        self._nurest_object = None
        self._transaction_id = None

    # Properties

    def _get_object(self):
        """ Get served object

            The fetcher will fill the served object with fetched objects

            Returns:
                Returns the object it is serving.
        """

        return self._nurest_object

    def _set_object(self, nurest_object):
        """ Set the served object

            Args:
                nurest_object: the objec to serve
        """

        self._nurest_object = nurest_object

    nurest_object = property(_get_object, _set_object)

    def _get_local_name(self):
        """ Get the name of the attribute that has to be filled

            Returns:
                Returns the name of the attribute in the served object
                that will be filled
        """

        return self._local_name

    def _set_local_name(self, local_name):
        """ Set the name of the attribut that has to be filled

            Args:
                local_name: the attribute name of the served object
        """

        self._local_name = local_name

    local_name = property(_get_local_name, _set_local_name)

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
    def managed_object_remote_name(cls):
        """ Remote name of the managed object

            Returns:
                Returns a string representing the resource name of the object
                that has to be fetched.
        """

        return cls.managed_class().get_resource_name()

    @classmethod
    def fetcher_with_object(cls, nurest_object, local_name):
        """ Register the fetcher for a served object.

            This method will fill the attribute indicated by `local_name` of
            the given object `nurest_object` with fetched objects of type `managed_class`

            Args:
                nurest_object: the instance of the object to serve
                local_name: the name of the attribute to fill when objects will be fetched

            Returns:
                It returns the fetcher instance.
        """

        fetcher = cls()
        fetcher.nurest_object = nurest_object
        fetcher.local_name = local_name

        setattr(nurest_object, local_name, [])
        nurest_object.register_children(getattr(nurest_object, local_name), cls.managed_object_remote_name())

        return fetcher

    def flush(self):
        """ Removes all fetched objects

            It will clear attribute of the served object
        """
        self._current_connection = None
        setattr(self.nurest_object, self.local_name, [])

    def new(self):
        """ Create an instance of the managed class

            Returns:
                Returns an instance of managed_class
        """

        managed_class = self.managed_class()
        return managed_class()

    def _prepare_headers(self, request, filter=None, master_filter=None, order_by=None, group_by=[], page=None, page_size=None):
        """ Prepare headers for the given request

            Args:
                request: the NURESTRequest to send
                filter: string
                master_filter: string
                order_by: string
                group_by: list of names
                page: int
                page_size: int
        """

        rest_filter = self._rest_filter_from_filter(filter, master_filter)

        if rest_filter:
            request.set_header('X-Nuage-Filter', rest_filter)

        if order_by:
            request.set_header('X-Nuage-OrderBy', order_by)

        if page:
            request.set_header('X-Nuage-Page', page)

        if page_size:
            request.set_header('X-Nuage-PageSize', page_size)

        if len(group_by) > 0:
            header = ", ".join(group_by)
            request.set_header('X-Nuage-GroupBy', 'true')
            request.set_header('X-Nuage-Attributes', header)

    def _prepare_url(self):
        """ Prepare url for request """

        url = self.nurest_object.get_resource_url_for_child_type(self.__class__.managed_class())

        if self.query_string:
            url += "?%s", self.query_string

        return url

    def fetch_objects(self, filter=None, master_filter=None, order_by=None, group_by=[], page=None, page_size=None, async=False, callback=None):
        """ Fetch objects according to given filter and page.

            This method fetches all managed class objects and store them
            in local_name of the served object.

            Args:
                filter: string that represents a predicate filter
                master_filter: string that represents a master filer
                order_by: string that represents an order by clause
                group_by: list of names for grouping
                page: number of the page to load
                page_size: number of results per page
                async: Boolean to make a asynchronous call. Default is False
                callback: Callback that should be called in case of a async request

            Returns:
                It returns a transaction ID in case of an asynchronous call.
                Otherwise, it returns a tuple of information (fetcher, served object, fetched objects, connection)
        """

        request = NURESTRequest(method=HTTP_METHOD_GET, url=self._prepare_url())

        self._prepare_headers(request=request, filter=filter, master_filter=master_filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size)
        self._transaction_id = uuid.uuid4().hex

        if async:
            self._nurest_object.send_request(request=request, async=async, local_callback=self._did_fetch_objects, remote_callback=callback)
            return self._transaction_id

        connection = self._nurest_object.send_request(request=request, async=async)
        return self._did_fetch_objects(connection=connection)

    def _did_fetch_objects(self, connection):
        """ Fetching objects has been done """

        self._current_connection = connection
        response = connection.response

        if response.status_code != 200:
            self.total_count = 0
            self.latest_loaded_page = 0
            self.ordered_by = ''
            return self._send_content(content=None, connection=connection)

        results = response.data
        destination = getattr(self.nurest_object, self._local_name)
        fetched_objects = list()

        if 'X-Nuage-Count' in response.headers and response.headers['X-Nuage-Count']:
            self.total_count = int(response.headers['X-Nuage-Count'])

        if 'X-Nuage-Page' in response.headers and response.headers['X-Nuage-Page']:
            self.latest_loaded_page = int(response.headers['X-Nuage-Page'])

        if 'X-Nuage-OrderBy' in response.headers and response.headers['X-Nuage-OrderBy']:
            self.ordered_by = response.headers['X-Nuage-OrderBy']

        if results:
            for result in results:

                nurest_object = self.new()
                nurest_object.from_dict(result)
                nurest_object.parent = self._nurest_object

                if nurest_object not in destination:
                    destination.append(nurest_object)

                fetched_objects.append(nurest_object)

        return self._send_content(content=fetched_objects, connection=connection)

    def countObjects(self, filter=None, master_filter=None, order_by=None, group_by=[], page=None, page_size=None, async=False, callback=None):
        """ Get the total count of objects that can be fetched according to filter

            This method can be asynchronous and trigger the callback method
            when result is ready.

            Args:
                filter: string that represents a predicate fitler (eg. name == 'x')
                master_filter: string that represents a master filer
                order_by: string that represents an order by clause
                group_by: list of names for grouping
                page: number of the page to load
                page_size: number of results per page
                async: Boolean to indicate an asynchronous call. Default is False
                callback: Method that will be triggered if async call is made

            Returns:
                Returns a transaction ID when asynchronous call is made.
                Otherwise it will return a tuple of information containing
                (fetcher, served object, count of fetched objects)
        """

        request = NURESTRequest(method=HTTP_METHOD_HEAD, url=self._prepare_url())

        self._prepare_headers(request=request, filter=filter, master_filter=master_filter, order_by=order_by, group_by=group_by, page=page, page_size=page_size)

        if async:
            self._transaction_id = uuid.uuid4().hex
            self._nurest_object.send_request(request=request, async=async, local_callback=self._did_count, remote_callback=callback)
            return self._transaction_id

        else:
            connection = self._nurest_object.send_request(request=request, async=async)
            return self._did_count(connection)

    def _did_count(self, connection):
        """ Called when count if finished """

        response = connection.response
        count = 0
        callback = None

        if 'X-Nuage-Count' in response.headers:
            count = int(response.headers['X-Nuage-Count'])

        if 'remote' in connection.callbacks:
            callback = connection.callbacks['remote']

        if connection.async:
            if callback:
                callback(self, self._nurest_object, count)
        else:

            if connection.response.status_code >= 400 and BambouConfig._should_raise_bambou_http_error:
                raise BambouHTTPError(response=connection.response)

            return (self, self._nurest_object, count)

    def _send_content(self, content, connection):
        """ Send a content array from the connection """

        if connection:

            if connection.async:
                callback = connection.callbacks['remote']

                if callback:
                    callback(self, self._nurest_object, content, connection)
            else:
                return (self, self._nurest_object, content, connection)

            self._current_connection.reset()
            self._current_connection = None

    def _rest_filter_from_filter(self, filter=None, master_filter=None):
        """ Computes a REST Filter according to filter and master_filter

            Args:
                filter: Filter as string
                master_filter as string

            Returns:
                A string representing all filters. If no filter has been
                provided, returns None.
        """

        if not filter and not master_filter:
            return None

        if master_filter and not filter:
            return str(master_filter)

        if filter and not master_filter:
            return str(filter)

        return "%s AND (%s)" % (master_filter, filter)

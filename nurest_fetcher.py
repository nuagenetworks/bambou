# # -*- coding: utf-8 -*-
#
# import requests
#
# from requests_futures.sessions import FuturesSession
#
# from restnuage.http_exceptions import HTTPTimeoutException
# from restnuage.nurest_login_controller import NURESTLoginController
#
#
# class RESTFetcher(object):
#     """ Object fetcher for childrens """
#
#     def __init__(self):
#         """ Initliazes the fetcher """
#
#         self._rest_name = self.__class__.managed_class.get_resource_name()
#         self._nurest_object = None
#         self._attribute_name = None
#
#     # Properties
#
#     def _get_object(self):
#         """ Get object to fetch """
#         return self._nurest_object
#
#     def _set_object(self, nurest_object):
#         """ Set object to fetch """
#         self._nurest_object = nurest_object
#
#     nurest_object = property(_get_object, _set_object)
#
#     def _get_attribute_name(self):
#         """ Get attribute name to fetch """
#         return self._attribute_name
#
#     def _set_attribute_name(self, attribute_name):
#         """ Set attribute name to fetch """
#         self._attribute_name = attribute_name
#
#     attribute_name = property(_get_attribute_name, _set_attribute_name)
#
#     # Methods
#
#     @classmethod
#     def managed_class(cls):
#         """ Returns the type of the object that is managed within this fetcher """
#
#         raise NotImplementedError('%s has no managed class. Implements managed_class method first.' % cls)
#
#     @classmethod
#     def fetch_object_attribute(cls, nurest_object, attribute_name):
#         """ Fetch an attribute of the object """
#
#         fetcher = RESTFetcher()
#         fetcher.nurest_object = nurest_object
#         fetcher.attribute_name = attribute_name
#
#         setattr(nurest_object, attribute_name, [])
#
#         return fetcher

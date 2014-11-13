.. Bambou documentation master file, created by
   sphinx-quickstart on Thu Oct 23 10:48:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Bambou's documentation!
==================================

Bambou is a RESTful library that wraps `requests` and provide a very useful framework to create a SDK.

It can be used both synchronously or asynchronously.

It provides:

    - ``NURESTObject``: All instances have access to CRUD operation and make HTTP request. Any model should inherit from this class.
    - ``NURESTBasicUser`` represents the user currently logged in into our application
    - ``NURESTFetcher`` allows an object to fetch its children
    - ``NURESTConnection`` define then connection used for sending a `NURESTRequest` and getting a `NURESTResponse`
    - ``NURESTLoginController`` manage a user connection
    - ``NURESTPushCenter`` allows you to start and stop listening for notification on a specific API URL.

.. toctree::
   :maxdepth: 2

.. automodule:: bambou
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


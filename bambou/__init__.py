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

from __future__ import print_function

__doc__ = """
# General Concepts


## Introduction

Bambou provides a set of objects that allow the manipulation of ReST entities very easily. It deals with all possible CRUD operations.
It is based on the library `Bambou`, which defines all these low level operations in a single place.

`Bambou` is composed of the following important classes:

* `bambou.NURESTSession`
    Class representing an authenticated session.

* `bambou.NURESTObject`
    Parent class of all ReST entities. All ReST exposed object objects inherit from this class.

* `bambou.NURESTFetcher`
    Class used to get children of a `bambou.NURESTObject`.

* `bambou.NURESTPushCenter`
    Class that deals with intercepting and rerouting ReST Push Notifications.

> There are more objects in `Bambou`, but you don't need to know all of them for now.



## NURESTSession

The `bambou.NURESTSession` represents some user credentials coupled with an API URL. All ReST calls are done using
the current active session. `bambou.NURESTSession` is an abstract class that must be reimplemented by anything using `Bambou`.

In a `MySDK` using bambou, you use a class named `mysdk.v3_2.MySession` which will be used in the following examples.


    #!python
    session = My}Session(username="user", password="secret", enterprise="organization", api_url="https://server")
    session.start()

    # your script

When you start the session, a ReST call will be sent to the API endpoint in order to get the API key.
If the credentials are valid, the attribute `MySDK.v3_2.MySession.root` will be populated with information such as your name,
your phone number, your avatar, your enterprise name and ID etc. This `user` is the root object of everything as all subsequent
calls need to be done in the context of your account (for instance, your `/enterprises` are different from another account's `/enterprises`)

It is also possible to create sub sessions with the python statement `with`:

    #!python
    cspsession = MySession(username="user", password="secret", enterprise="organization", api_url="https://server")
    adminsession = MySession(username="admin", password="secret", enterprise="enterprise", api_url="https://server")

    cspsession.start()

    # this part of the code will use the CSP root user

    with adminsession.start():
        # this code block will be executed as admin of `enterprise`

    # back to csp root session

> You **must** use `start()` when using the `with` statement, even if the session has already been started in the main context.



## NURESTObject

`bambou.NURESTObject` is the parent class of all `MySDK` entities.


### ReST Names

All `bambou.NURESTObject` subclasses implements a given method that will return the actual ReST name of the objects. For instance, the ReST name of an Unicorn object is `unicorn`.

These names are used to forge the correct URI when doing CRUD operations on them.

> ReST names can be used as unique resource identifier for a given object.

> ReST names are auto generated. You never need to manually define them.


### ReST API URI Generation

`bambou.NURESTObject` is able to forge all the URI needed to interact with the server through the ReST API.

For instance, if an object with a ReST name set to `object` needs to get the list of children with ReST name set to `subobject`, `Bambou` will use the following endpoint URL:

    `GET {api_base_url}/objects/{id}/subobjects`

If an object with a ReST name set to `entity` needs to fetch itself, the generated URL will be

    `GET {api_base_url}/entities/{id}`


> `Bambou` automagically deals with plurals.

> The ReST base URL is pulled from the current active `bambou.NURESTSession`.

> URI are auto generated. You never need to deal with them manually.


### Exposing ReST Attributes

Exposed attributes will be converted and sent to the server when you do CRUD operations. That way, if an object has an attribute `name`, it can be marked as a ReST attribute.

When saving the object, the value of `name` will be put into the generated JSON structure that will be sent to the server, or automatically populated from a JSON structure that is coming from the server.

Not only the attribute can be exposed, but also its type and other informations like if it is read only, its allowed values, its format, its default value and so on.

> exposing ReST Attributes is auto generated. You never need to manually expose new attributes.


### CRUD Operations

`bambou.NURESTObject` allows to perform all sorts of CRUD operations.

* `bambou.NURESTObject.fetch`
* `bambou.NURESTObject.save`
* `bambou.NURESTObject.delete`
* `bambou.NURESTObject.create_child`
* `bambou.NURESTObject.assign`
* `bambou.NURESTObject.instantiate_child`

> All these methods require the current `bambou.NURESTObject` to have a valid `bambou.NURESTObject.ID`.

> You may notice that there is no creation method. Creation is always happening from a parent object and is done using `create_child`.

> You may notice that an optional parameter `callback` is present. This is because `MySDK` can work completely asynchronously.


### Converting to and from a Python Dictionary

`bambou.NURESTObject` allows quick and easy conversion from and to python dictionaries

* `bambou.NURESTObject.from_dict`
* `bambou.NURESTObject.to_dict`

> you never need to process to the actual JSON conversion when sending info to the server. `bambou.NURESTConnection` will do that automatically, but you can use these methods to print an object, or copy information of an object into one another.



## NURESTFetcher

`bambou.NURESTFetcher` is a class allowing a `bambou.NURESTObject` to fetch its children. All `bambou.NURESTObject` have one or more fetchers, unless it's a final object in the  model hierarchy. `bambou.NURESTFetcher` provides a lot of possibility regarding the way you want to get a given children list. It can deal with simple object fetching, pagination, filtering, request headers, grouping etc.


### Fetching Children List

`bambou.NURESTFetcher` has three importants methods:

* `bambou.NURESTFetcher.fetch`
* `bambou.NURESTFetcher.get`
* `bambou.NURESTFetcher.get_first`


### Discussion about Fetchers

Fetcher is a powerfull concept that makes the process of getting child objects completely generic and code friendly. `bambou.NURESTObject` provides methods that allow to deal programatically with its fetchers in a completely generic way.

* `bambou.NURESTObject.fetcher_for_rest_name`
* `bambou.NURESTObject.fetchers`
* `bambou.NURESTObject.children_rest_names`

This allows complete abstract programatic operations on any objects.

For instance, the following function will create a new `MySDK.v3_2.Metadata` to the entire hierarchy of children from a given object that has been created after a certain date:

    #!python
    def apply_metatada_to_all_children(root_object, metadata, filter=None):

        # Loop on all declared children fetchers
        for fetcher in root_object.fetchers:

            # Fetch the list of the children
            children = fetcher.get(filter=filter)

            # Loop on all fetched children
            for child in children:

                # Add the metadata to the current children
                child.create_child(metadata)

                # Start over recursively on the children of the current child
                apply_metadata_to_all_children(child, metadata)


    enterprise = Enterprise(id="xxxx-xxxx-xxx-xxxx")
    metadata = Metadata(name="my metadata", blob="hello world!")

    apply_metadata_to_all_children(enterprise, metadata, filter="creationDate > '01-01-2015'")



## NURESTPushCenter

The API supports client side push through a long polling connection. ReST clients can connect to that channel and will get a notification as soon as he or someone else in the system changes something. This events are filtered by permissions, which means that if someone change a property of an object you cannot see, you won't get notified. `MySDK` provides the `bambou.NURESTPushCenter`, which encapsulates all the logic to deal with the event channel. It runs in its own thread and will call registered callbacks when it receives a push.

A `bambou.NURESTPushCenter` is automatically created with each `bambou.NURESTSession` and it is available from the attribute `bambou.NURESTSession.push_center`.

    #!python
    session = MySession(username="user", password="secret", enterprise="organization", api_url="https://server")
    session.start()
    session.push_center.start()

> You need to explicitely start the push center.


### Using the NURESTPushCenter

Only the following methods are important:

* `bambou.NURESTPushCenter.start`
* `bambou.NURESTPushCenter.add_delegate`
* `bambou.NURESTPushCenter.remove_delegate`


### Example

Here is a really simple code sample that will print the push data on every push:

    #!python
    from MySDK import *
    from pprint import pprint
    from time import sleep

    session = MySession(username="csproot", password="secret", enterprise="csp", api_url="https://server")
    session.start()

    def on_receive_push(data):
        pprint(data);

    session.push_center.add_delegate(on_receive_push);
    session.push_center.start()

    # default stupid run loop. don't do that in real life :)
    while True:
        sleep(1000)


## Conclusion

Now you know the basics of `Bambou` and so, of the `MySDK`. Remember that all objects in `MySDK` are subclasses of `bambou.NURESTObject` so they **all** work exactly the same.

There is a lot more to know about `Bambou` like the asynchronous mode, auto model parsing, easy controllers creation thanks introspection and so on. We'll cover this in a different advanced section.
"""

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except:
    pass

import logging

bambou_logger = logging.getLogger('bambou')
pushcenter_logger = logging.getLogger('pushcenter')

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

bambou_logger.addHandler(NullHandler())

__all__ = ['NURESTRootObject', 'NURESTConnection', 'NURESTModelController', 'NURESTFetcher', 'NURESTLoginController', 'NURESTObject', 'NURESTPushCenter', 'NURESTRequest', 'NURESTResponse', 'NURESTSession', 'BambouConfig']

from bambou.nurest_session import NURESTSession
from bambou.nurest_root_object import NURESTRootObject
from bambou.nurest_connection import NURESTConnection
from bambou.nurest_fetcher import NURESTFetcher
from bambou.nurest_login_controller import NURESTLoginController
from bambou.nurest_object import NURESTObject
from bambou.nurest_push_center import NURESTPushCenter
from bambou.nurest_request import NURESTRequest
from bambou.nurest_response import NURESTResponse
from bambou.nurest_modelcontroller import NURESTModelController
from bambou.config import BambouConfig

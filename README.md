Bambou - bends but does not break !
====================================

Python REST layer for Nuage Networks' Virtual Service Directory (http://www.nuagenetworks.net/).

Bambou works on top of `requests` library and provides an object layer.
All objects that inherits from `NURESTObject` will be able to discuss with your VSD Backend.


Usage
-----

1. Create your object models to extends NURESTObject or NURESTBasicUser (see `tests/models.py` for examples)
2. Start a user session. (see implementation of `NURESTTestSession` in `tests/models.py`)
3. Retrieve connected user from the sesssion
4. Use basic concepts (`create_child`, `save`, `fetch`, `delete`) to manipulate objects
::

    from bambou import NURESTSession()

    # Start session
    session = NURESTSession(username, password, enterprise, api_url, version)
    session.start()

    # Grab connected user
    user = session.user

    # Instantiate Python objects that inherits from NURESTObject
    enterprise = Enterprise(id="xxxx-xxx-xxx-xxx")
    enterprise.fetch()
    enterprise.name = u"My new company"
    enterprise.save()

    # Create new objects
    startup = Enterprise(name=u"A new startup", description=u"Very promising enterprise")
    user.create_child(startup)

`Bambou` enables to create both synchronous (by default) and asynchronous scripts. When dealing with asynchronous
scripts, we provide a push notification center that listen for all events. This `push_center` is accesible via the
user session:
::

    push_center = session.push_center
    push_center.start()  # Start listening events
    push_center.get_last_events()  # Retrieve last events
    push_center.stop()  # Stop listening events

Examples
--------
We provide basic examples in `examples` directory.


    $ cd examples
    $ python sync_example.py  # To launch the synchronized example
    $ python async_example.py # To launch the async version
    $ python push_example.py  # To launch the push center example

If you want to know more, you should check our VSD Software Development Kit called `vsdk`.
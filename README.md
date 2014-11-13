Bambou - bends but does not break !
====================================

Python REST layer for Nuage Networks' Virtual Service Directory (http://www.nuagenetworks.net/).

Bambou works on top of `request` library and provides an object layer.
All objects that inherits from `NURESTObject` will be able to discuss with your VSD Backend.


Usage
-----

__#1 Create your object models to extends NURESTObject or NURESTBasicUser__
::

    from bambou.nurest_user import NURESTBasicUser
    class User(NURESTBasicUser):

        @classmethod
        def get_rest_name(cls):
            """ Provides user rest name  """

            return "user"

__#2 Start a new NURESTLoginController__
::

    ctrl = NURESTLoginController()
    ctrl.user = u"your_user"
    ctrl.password = u"your_password"
    ctrl.enterprise = u"your_enterprise"
    ctrl.url = u"your_url"
    #ctrl.async = False  # Default is True

__#3 Instanciate your model and fetch, save, create or delete it__
::

    user = User()
    user.fetch(callback=your_callback)
    user.firstname = u'John'
    user.save(callback=another_callback)

__#4 Using push center notifications__
::

    push_center = NURESTPushCenter.get_default_instance()
    push_center.start()  # Start listening events
    push_center.get_last_events()  # Retrieve last events
    push_center.stop()  # Stop listening events

Examples
-------
::

    $ cd examples
    $ python sync_example.py  # To launch the synchronized example
    $ python async_example.py # To launch the async version
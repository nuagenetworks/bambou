# RESTNuage
=========================

Python REST layer for Nuage Networks' application

### Setting up your python environment

Follow these 3 steps to use your python environment.

1) First, you should install your environment if you have not done already

    $ virtual-env --no-site-packages restnuage-env
    $ Installing Setuptools..[]..done.

2) Activate your environment

    $ cd restnuage-env
    $ source bin/activate
    (restnuage-env) $ cd restnuage-env

3) Clone repository
    
    git clone http://github.mv.usa.alcatel.com/chserafi/restnuage.git
    
4) Install package dependencies listed in requirements.txt file

    (restnuage-env) $ cd restnuage
    (restnuage-env) $ pip install -r requirements.txt


### Usage

__#1 Create your object models to extends NURESTObject or NURESTBasicUser__

    from restnuage.nurest_user import NURESTBasicUser
    class User(NURESTBasicUser):

        @classmethod
        def get_rest_name(cls):
            """ Provides user rest name  """

            return "user"

__#2 Start a new NURESTLoginController__

    ctrl = NURESTLoginController()
    ctrl.user = u"your_user"
    ctrl.password = u"your_password"
    ctrl.enterprise = u"your_enterprise"
    ctrl.url = u"your_url"
    #ctrl.async = False  # Default is True

__#3 Instanciate your model and fetch, save, create or delete it__

    user = User()
    user.fetch(callback=your_callback)
    user.firstname = u'John'
    user.save(callback=another_callback)

__#4 Using push center notifications__

    push_center = NURESTPushCenter()
    push_center.start()  # Start listening events
    push_center.get_last_events()  # Retrieve last events
    push_center.stop()  # Stop listening events

### Examples

    $ cd examples
    $ python sync_example.py  # To launch the synchronized example
    $ python async_example.py # To launch the async version
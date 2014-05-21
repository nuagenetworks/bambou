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

3) Install package dependencies listed in requirements.txt file

    (restnuage-env) $ cd restnuage
    (restnuage-env) $ pip install -r requirements.txt


### Launch tests



### Usage

__#1 Create your object models to extends RESTObject or RESTBasicUser__

    from restnuage.restuser import RESTBasicUser
    class User(RESTBasicUser):

        @classmethod
        def get_rest_name(cls):
            """ Provides user rest name  """

            return "user"

__#2 Start a new RESTLoginController__

    ctrl = RESTLoginController()
    ctrl.user = u"your_user"
    ctrl.password = u"your_password"
    ctrl.company = u"your_company"
    ctrl.url = u"your_url"

__#3 Instanciate your model and fetch, save, create or delete it__

    user = User()
    user.fetch(callback=your_callback)
    user.firstname = u'John'
    user.save(callback=another_callback)

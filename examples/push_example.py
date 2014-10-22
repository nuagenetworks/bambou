# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

from time import sleep
from bambou import NURESTLoginController, NURESTPushCenter, NURESTBasicUser


# this class is needed because you are not using our model
# so you need to define that the rest user resource is /me
class NURESTUser(NURESTBasicUser):

    @classmethod
    def get_remote_name(cls):
        return "me"

    @classmethod
    def is_resource_name_fixed(cls):
        return True


# this is your call back. it will print all events that are received
# you will need to go trough the content, and ignore what you don't need
# it's easy.
def did_receive_push(data):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data);


if __name__ == '__main__':

    # create a login controller singleton
    # this class holds information on the crendentials
    # that need to be use for all REST communication
    ctrl            = NURESTLoginController()
    ctrl.user       = "csproot"
    ctrl.password   = "csproot"
    ctrl.enterprise = "csp"
    ctrl.url        = "https://135.227.220.152:8443/nuage/api/v3_0"

    # Then we need to fetch the API key
    # so we get our NURESTUser and fetch it.
    # it will use the NURESTLoginController password
    user = NURESTUser().get_default_user()

    # we get the answer in sync mode (but we have async mode too because we rock)
    (user, connection) = user.fetch(async=False)

    # and then we set the API key in the NURESTLoginController.
    # this means that all subsequent REST calls will use the API key
    ctrl.api_key = user.api_key

    # Then here we get the default push center
    push_center = NURESTPushCenter.get_default_instance()
    push_center.url = ctrl.url

    # we register our delegate that will be called on each event
    push_center.add_delegate(did_receive_push);

    # and we start it
    push_center.start()


    # then we do nothing, welcome to the marvelous world of async programing ;)
    while True:
        sleep(10000)

# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

from time import sleep
from restnuage import NURESTLoginController
from restnuage import NURESTPushCenter
from models import NURESTUser
import signal

def did_receive_push(data):
    print data;


def main():

    # create a login controller singleton
    ctrl = NURESTLoginController()
    ctrl.user = "csproot"
    ctrl.password = "csproot"
    ctrl.enterprise = "csp"
    ctrl.url = "https://135.227.220.152:8443/nuage/api/v3_0"

    # create the user object
    user = NURESTUser().get_default_user()
    (user, connection) = user.fetch(async=False)

    # then set the API key to the login controller
    ctrl.api_key = user.api_key

    # start the push center
    push_center = NURESTPushCenter.get_default_instance()
    push_center.add_delegate(did_receive_push);
    push_center.start()

    while True:
        sleep(10000)


if __name__ == '__main__':
    main()

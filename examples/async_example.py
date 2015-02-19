# -*- coding: utf-8 -*-
from __future__ import print_function


import sys
import threading
sys.path.append("../")

from time import sleep

from bambou import NURESTLoginController
from bambou import NURESTPushCenter

from models import Enterprise, NURESTUser

user = NURESTUser()
push_center = NURESTPushCenter()
ctrl = NURESTLoginController()


def _did_add_enterprise(enterprise, connection):
    """ Callback after user.create_child_object(nurest_object=enterprise...) """

    if connection.response.status_code < 300:
        print("Enterprise saved with ID=%s" % enterprise.id)

        sleep(6)

        # Remove enterprise
        # user.remove_child_object(nurest_object=enterprise,
        enterprise.delete(callback=_did_remove_enterprise, async=True, response_choice=1)

    else:
        push_center.stop()
        print("Enterprise has not been saved : " + str(connection.response.errors))

    push_center.get_last_events()


def _did_remove_enterprise(enterprise, connection):
    """ Callback method after user.remove_child_object(nurest_object=enterprise...) """

    print("Enterprise %s has been removed" % enterprise)
    push_center.stop()


def _did_user_fetch(user, connection):
    """ Callback method after user.fetch """

    print("** User did fetch in thread")

    # Set controller API Key for authentication
    ctrl.api_key = user.api_key

    # Start the push center listening to events
    push_center.start()

    # Add a new enterprise and process callback named `_did_add_enterprise`
    enterprise = Enterprise()
    enterprise.name = 'Async Enterprise test'
    enterprise.description = 'Description of test enterprise'
    user.create_child_object(nurest_object=enterprise, callback=_did_add_enterprise, async=True)


def main():
    """ Main method"""

    # Initializes login controller
    ctrl.user = u"csproot"
    ctrl.password = u"csproot"
    ctrl.enterprise = u"csp"
    ctrl.url = u"https://135.227.220.152:8443/nuage/api/v3_0"

    # Set push_center address to listen
    push_center.url = ctrl.url

    # Logs in and process callback named `_did_user_fetch`
    user.fetch(callback=_did_user_fetch, async=True)

    print("\nEnd Main\nUser %s (%s)" % (user, threading.current_thread()))

if __name__ == '__main__':
    main()

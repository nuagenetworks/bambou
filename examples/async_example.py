# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

import threading
from time import sleep

from restnuage import NURESTLoginController
from restnuage import NURESTPushCenter

from models import Enterprise, User


user = User()
push_center = NURESTPushCenter.get_default_instance()
ctrl = NURESTLoginController()


def _did_add_enterprise(enterprise, connection):
    """ Callback after user.add_child_entity(entity=enterprise...) """

    if connection.response.status_code < 300:
        print "Enterprise saved with ID=%s" % enterprise.id

        sleep(6)

        # Remove enterprise
        user.remove_child_entity(entity=enterprise, callback=_did_remove_enterprise, async=True, response_choice=1)

    else:
        print "Enterprise has not been saved"

    push_center.get_last_events()


def _did_remove_enterprise(enterprise, connection):
    """ Callback method after user.remove_child_entity(entity=enterprise...) """

    print "Enterprise %s has been removed" % enterprise
    push_center.stop()


def _did_user_fetch(user, connection):
    """ Callback method after user.fetch """

    print "** User did fetch in thread"

    # Set controller API Key for authentication
    ctrl.api_key = user.api_key

    # Start the push center listening to events
    push_center.start()

    # Add a new enterprise and process callback named `_did_add_enterprise`
    enterprise = Enterprise()
    enterprise.name = 'Test'
    enterprise.description = 'Description of test enterprise'
    user.add_child_entity(entity=enterprise, callback=_did_add_enterprise, async=True)


def main():
    """ Main method"""

    # Initializes login controller
    ctrl.user = u"csproot"
    ctrl.password = u"csproot"
    ctrl.enterprise = u"csp"
    ctrl.url = u"https://135.227.220.152:8443/nuage/api/v1_0"

    # Logs in and process callback named `_did_user_fetch`
    user.fetch(callback=_did_user_fetch, async=True)

    print "\n End\nUser %s (%s)" % (user, threading.current_thread())

if __name__ == '__main__':
    main()

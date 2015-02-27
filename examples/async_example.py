# -*- coding: utf-8 -*-
from __future__ import print_function


import sys
import threading
sys.path.append("../")

from time import sleep

from models import Enterprise, NUSession


def _did_add_enterprise(enterprise, connection):
    """ Callback after user.create_child(nurest_object=enterprise...) """

    # Retrieve push center from the current session
    session = NUSession.get_current_session()
    push_center = session.push_center

    if connection.response.status_code < 300:
        print("Enterprise saved with ID=%s" % enterprise.id)

        print("Sleeping for 6 seconds...")
        sleep(6)

        # Remove enterprise
        enterprise.delete(callback=_did_remove_enterprise, async=True)

    else:
        push_center.stop()
        print("Enterprise has not been saved : " + str(connection.response.errors))

    push_center.get_last_events()


def _did_remove_enterprise(enterprise, connection):
    """ Callback method after user.remove_child_object(nurest_object=enterprise...) """

    # Retrieve push center from the current session
    session = NUSession.get_current_session()
    push_center = session.push_center

    print("Enterprise %s has been removed" % enterprise)
    push_center.stop()


def main():
    """ Main method"""

    session = NUSession(username="csproot", password="csproot", enterprise="csp", api_url="https://vsd:8443", version="3.1")
    session.start()

    # Retrieve objects from started session
    user = session.user
    push_center = session.push_center

    # Start the push center
    push_center.start()

    # Create a new enterprise asynchronously
    enterprise = Enterprise()
    enterprise.name = 'Async Enterprise test'
    enterprise.description = 'Description of test enterprise'
    user.create_child(nurest_object=enterprise, callback=_did_add_enterprise, async=True)

    print("\nEnd Main\nUser %s (%s)" % (user, threading.current_thread()))

if __name__ == '__main__':
    main()

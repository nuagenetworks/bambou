# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

from time import sleep
from models import NURESTUser, NUSession
# Uncomment these lines to enable logging messages
# import logging
# from bambou import bambou_logger
# bambou_logger.setLevel(logging.INFO)
# bambou_logger.addHandler(logging.StreamHandler())



# this is your call back. it will print all events that are received
# you will need to go trough the content, and ignore what you don't need
# it's easy.
def did_receive_push(data):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data);


if __name__ == '__main__':

    # create a user session for user csproot
    session = NUSession(username="csproot", password="csproot", enterprise="csp", api_url="https://vsd:8443", version="3.1")

    # start the session
    # now session contains a push center and the connected user
    session.start()

    # we get the push center from the session
    push_center = session.push_center

    # we register our delegate that will be called on each event
    push_center.add_delegate(did_receive_push);

    # and we start it
    push_center.start()

    # then we do nothing, welcome to the marvelous world of async programing ;)
    while True:
        sleep(10000)

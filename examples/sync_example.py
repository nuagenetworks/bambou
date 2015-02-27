# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import logging
sys.path.append("../")

from time import sleep

from models import Enterprise, NUSession

# Exemple of how you can activate logs

from bambou import bambou_logger
bambou_logger.setLevel(logging.INFO)
bambou_logger.addHandler(logging.StreamHandler())


def main():
    """ Main method """

    session = NUSession(username="csproot", password="csproot", enterprise="csp", api_url="https://vsd:8443", version="3.1")

    with session.start():
        user = session.user

        enterprise = Enterprise()
        enterprise.name = u'My company'
        enterprise.description = 'A nice description here'

        (enterprise, connection) = user.create_child(nurest_object=enterprise, async=False)

        print('Sleeping for... 6 sec')
        sleep(6)

        enterprise.delete()

if __name__ == '__main__':
    main()

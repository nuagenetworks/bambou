# -*- coding: utf-8 -*-
import sys
import logging
sys.path.append("../")

from time import sleep

from bambou import NURESTLoginController
from models import Enterprise, User

bambou_log = logging.getLogger('bambou')
bambou_log.setLevel(logging.INFO)
logging.getLogger('bambou').addHandler(logging.StreamHandler())

def main():
    """ Main method """

    user = NURESTUser()

    # Initializes login controller
    ctrl = NURESTLoginController()
    ctrl.user = u"csproot"
    ctrl.password = u"csproot"
    ctrl.enterprise = u"csp"
    ctrl.url = u"https://135.227.220.152:8443/nuage/api/v3_0"

    # Get User and set API Key for authentication
    (user, connection) = user.fetch(async=False)
    ctrl.api_key = user.api_key

    print ctrl.api_key

    enterprise = Enterprise()
    enterprise.name = 'Christophe Test'
    enterprise.description = 'Hey hey hey'

    (enterprise, connection) = user.add_child_entity(entity=enterprise, async=False)

    print 'Sleeping... 6 sec'
    sleep(6)

    enterprise.delete(response_choice=1)

if __name__ == '__main__':
    main()

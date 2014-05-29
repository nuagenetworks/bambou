# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

from time import sleep

from restnuage import NURESTLoginController
from models import Company, User



def main():
    """ Main method """

    user = User()

    # Initializes login controller
    ctrl = NURESTLoginController()
    ctrl.user = u"csproot"
    ctrl.password = u"csproot"
    ctrl.company = u"csp"
    ctrl.url = u"https://135.227.220.152:8443/nuage/api/v1_0"

    # Get User and set API Key for authentication
    (user, connection) = user.fetch(async=False)
    ctrl.api_key = user.api_key

    company = Company()
    company.name = 'Christophe Test'
    company.description = 'Hey hey hey'

    user.add_child_entity(entity=company, async=False)

    print 'Sleeping... 6 sec'
    sleep(6)

    user.remove_child_entity(entity=company, async=False, response_choice=1)


if __name__ == '__main__':
    main()


#try:    from restnuage.nurest_login_controller import NURESTLoginController except:   import sys   sys.path.append(...)   from restnuage.nurest_login_controller import NURESTLoginController
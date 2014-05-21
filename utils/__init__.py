# -*- coding: utf-8 -*-

import json


def parse(json_string):
    """ Try to load JSON as a dictionary. Returns None if no JSON can be decoded """

    try:
        data = json.loads(json_string)
    except ValueError:
        print 'No JSON object could be decoded : %s', json_string
        data = None

    return data

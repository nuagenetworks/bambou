# -*- coding: utf-8 -*-
"""
Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.

This source code contains confidential information which is proprietary to Alcatel.
No part of its contents may be used, copied, disclosed or conveyed to any party
in any manner whatsoever without prior written permission from Alcatel.

Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
"""

from .utils.singleton import Singleton


class NURESTModelController(Singleton):
    """ Access any object via its remote name """

    __default_controller = None

    def __init__(self):
        """ Initializes the Model controller """

        self._model_registry = dict()

    @classmethod
    def get_default(cls):
        """ Get default controller """

        if not cls.__default_controller:
            cls.__default_controller = cls()

        return cls.__default_controller

    def register_model(self, model):
        """
            Register a model class according to its remote name

            Args:
                model: the model to register
        """

        rest_name = model.rest_name

        if rest_name not in self._model_registry:
            self._model_registry[rest_name] = [model]

        elif model not in self._model_registry[rest_name]:
            self._model_registry[rest_name].append(model)

    def get_models(self, rest_name):
        """ Retrieve all models from a given remote name

            Args:
                rest_name: the remote name entry

            Returns:
                A list of models corresponding to remote name arg.
                An empty list if no entries found for the remote name
        """

        if rest_name in self._model_registry:
            return self._model_registry[rest_name]

        return []

    def get_first_model(self, rest_name):
        """ Get the first model corresponding to a rest_name

            Args:
                rest_name: the remote name
        """

        models = self.get_models(rest_name)

        if len(models) > 0:
            return models[0]

        return None

# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class NURESTModelController(object):
    """ Access any object via its remote name """

    _model_rest_name_registry = {}
    _model_resource_name_registry = {}

    @classmethod
    def register_model(cls, model):
        """
            Register a model class according to its remote name

            Args:
                model: the model to register
        """

        rest_name = model.rest_name
        resource_name = model.resource_name

        if rest_name not in cls._model_rest_name_registry:
            cls._model_rest_name_registry[rest_name] = [model]
            cls._model_resource_name_registry[resource_name] = [model]

        elif model not in cls._model_rest_name_registry[rest_name]:
            cls._model_rest_name_registry[rest_name].append(model)
            cls._model_resource_name_registry[resource_name].append(model)

    @classmethod
    def get_all_models(cls):
        """ Retrieve all models

            Returns:
                A list of all models.
                An empty list if no entries found for the remote name
        """

        return cls._model_rest_name_registry.values()

    # Get models by rest_name

    @classmethod
    def get_models_with_rest_name(cls, rest_name):
        """ Retrieve all models from a given rest name

            Args:
                rest_name: the rest name entry

            Returns:
                A list of models corresponding to remote name arg.
                An empty list if no entries found for the remote name
        """

        if rest_name in cls._model_rest_name_registry:
            return cls._model_rest_name_registry[rest_name]

        return []

    @classmethod
    def get_first_model_with_rest_name(cls, rest_name):
        """ Get the first model corresponding to a rest_name

            Args:
                rest_name: the rest name
        """

        models = cls.get_models_with_rest_name(rest_name)

        if len(models) > 0:
            return models[0]

        return None

    # Get models by resource_name

    @classmethod
    def get_models_with_resource_name(cls, resource_name):
        """ Retrieve all models from a given resource_name

            Args:
                resource_name: the resource name of the model

            Returns:
                A list of models corresponding to remote name arg.
                An empty list if no entries found for the remote name
        """

        if resource_name in cls._model_resource_name_registry:
            return cls._model_resource_name_registry[resource_name]

        return []

    @classmethod
    def get_first_model_with_resource_name(cls, resource_name):
        """ Get the first model corresponding to a resource_name

            Args:
                resource_name: the resource name
        """

        models = cls.get_models_with_resource_name(resource_name)

        if len(models) > 0:
            return models[0]

        return None

    # will be deprecated
    @classmethod
    def get_models(cls, rest_name):
        """
        """
        return cls.get_models_with_rest_name(rest_name)

    # will be deprecated
    @classmethod
    def get_first_model(cls, rest_name):
        """
        """
        return cls.get_first_model_with_rest_name(rest_name)

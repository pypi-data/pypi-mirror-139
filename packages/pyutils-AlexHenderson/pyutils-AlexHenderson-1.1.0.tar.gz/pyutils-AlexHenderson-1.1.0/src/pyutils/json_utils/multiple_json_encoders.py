# This file is part of the pyutils library https://github.com/AlexHenderson/pyutils
# Copyright (c) 2022 Alex Henderson (alex.henderson@manchester.ac.uk)
# SPDX-License-Identifier: MIT

import json


class MultipleJsonEncoders(json.JSONEncoder):
    """
    Class extending :class:`json.JSONEncoder` to handle multiple JSONEncoders of different types.

    Code taken from `stackoverflow`_ with only a small modification. If a number of different encoders are passed
    to the constructor, the input is tested against each in turn. The order in which the encoders are listed as
    arguments, is the order in which they are evaluated.

    Example::

        >>> from src.pyutils.json_utils.multiple_json_encoders import MultipleJsonEncoders
        >>> encoder = MultipleJsonEncoders(JsonPintEncoder, JsonDatetimeEncoder)
        >>> jsonoutput = json.dumps(pint_or_datetime_variable, indent=4, cls=encoder)

    .. _`stackoverflow`: https://stackoverflow.com/questions/65338261/combine-multiple-json-encoders
    """
    def __init__(self, *encoders):
        super().__init__()
        self.encoders = encoders
        self.args = ()
        self.kwargs = {}

    def default(self, obj):
        """
        Managed internally
        """
        for encoder in self.encoders:
            try:
                return encoder(*self.args, **self.kwargs).default(obj)
            except TypeError:
                pass
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        enc = json.JSONEncoder(*args, **kwargs)
        enc.default = self.default
        return enc

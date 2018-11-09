"""
The FWF class definition.
"""
# from decimal import Decimal, ROUND_HALF_EVEN

from datetime import datetime
from six import string_types, integer_types
from pandas import DataFrame
import pandas as pd
import numpy as np
import math


class FWF(object):
    """


    """

    def __init__(self, config, data, **kwargs):
        """
        Arguments:
            config: required, dict defining fixed-width format
        """

        self.line_end = kwargs.pop('line_end', '\r\n')
        self.config = config

        self.data = data

        self.ordered_fields = sorted(
            [(self.config[x]['start_pos'], x) for x in self.config]
        )

        # Raise exception for bad config
        for key, value in self.config.items():

            # required values
            if any([x not in value for x in (
                    'required',  'padding', 'alignment', 'start_pos')]):
                raise ValueError(
                    "Not all required values provided for field %s" % (key,))

            # end position or length required
            if 'end_pos' not in value and 'length' not in value:
                raise ValueError(
                    "An end position or length is required for field %s" % (key,))

            # end position and length must match if both are specified
            if all([x in value for x in ('end_pos', 'length')]):
                if value['length'] != value['end_pos'] - value['start_pos'] + 1:
                    raise ValueError("Field %s length (%d) does not coincide with \
                        its start and end positions." % (key, value['length']))

            # fill in length and end_pos
            if 'end_pos' not in value:
                value['end_pos'] = value['start_pos'] + value['length'] - 1
            if 'length' not in value:
                value['length'] = value['end_pos'] - value['start_pos'] + 1

            # end_pos must be greater than start_pos
            if value['end_pos'] < value['start_pos']:
                raise ValueError(
                    "%s end_pos must be *after* start_pos." % (key,))

            # make sure alignment is 'left' or 'right'
            if not value['alignment'] in ('left', 'right'):
                raise ValueError("Field %s has an invalid alignment (%s). \
                    Allowed: 'left' or 'right'" % (key, value['alignment']))

        # ensure start_pos and end_pos or length is correct in config
        current_pos = 1
        for start_pos, field_name in self.ordered_fields:

            if start_pos != current_pos:
                raise ValueError("Field %s starts at position %d; \
                should be %d (or previous field definition is incorrect)."
                                 % (field_name, start_pos, current_pos))

            current_pos = current_pos + config[field_name]['length']

    def __str__(self):
        self.validate()
        content = ''
        for _, row in self.data.iterrows():
            content = content + self._build_line(row)
        return content

    __repr__ = __str__

    def update_dataframe(self, data):
        """
        Update dataframe
        """
        self.data = data

    def to_fwf(self):
        self.validate()
        content = ''
        for _, row in self.data.iterrows():
            content = content + self._build_line(row)
        return content

    def validate(self):

        for field_name, parameters in self.config.items():

            if field_name not in self.data.columns:
                # if required but not provided
                if parameters['required'] and ('value' not in parameters):
                    raise ValueError("Column %s is required, but was \
                        not provided." % (field_name,))

            if parameters['required'] and self.data[field_name] is None:
                # None gets checked last because it may be set with a default value
                raise ValueError(
                    "None value not allowed for %s" % (field_name))

        return True

    def _build_line(self, row):
        """
        Returns a fixed-width line made up of self.data, using
        self.config.
        """

        self.validate()

        line = ''
        # for start_pos, field_name in self.ordered_fields:
        for field_name in [x[1] for x in self.ordered_fields]:
            datum = ''
            val = row[field_name]
            if val is None or val is np.nan:
                datum = ''
            else:
                if isinstance(val, (int, float)):
                    if math.isnan(val):
                        datum = ''
                    else:
                        datum = (str(val))
                else:
                    datum = (str(val))

            datum = (datum[:self.config[field_name]['length']])

            justify = None
            if self.config[field_name]['alignment'] == 'left':
                justify = datum.ljust
            else:
                justify = datum.rjust

            datum = justify(self.config[field_name]['length'],
                            self.config[field_name]['padding'])

            line += datum

        return line + self.line_end

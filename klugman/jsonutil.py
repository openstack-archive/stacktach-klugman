# Copyright (c) 2014 Dark Secret Software Inc.
# Copyright (c) 2015 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import iso8601
import timex


def _present(dct, name):
    return name in dct and dct[name] is not None and dct[name] != 'None'


def decode_datetime(dct, name):
    if not _present(dct, 'datetime'):
        return 'n/a'
    return iso8601.parse_date(dct['datetime'], default_timezone=None)


def decode_timerange(dct, name):
    begin = 'n/a'
    if _present(dct, 'begin'):
        begin = iso8601.parse_date(dct['begin'], default_timezone=None)
    end = 'n/a'
    if _present(dct, 'end'):
        end = iso8601.parse_date(dct['end'], default_timezone=None)
    return timex.TimeRange(begin=begin, end=end)


def decode_timestamp(dct, name):
    if not _present(dct, 'timestamp'):
        return 'n/a'
    timestamp = iso8601.parse_date(dct['timestamp'], default_timezone=None)
    return timex.Timestamp(timestamp)


DECODE_MAP = {'datetime': decode_datetime,
              'timex.TimeRange': decode_timerange,
              'timex.Timestamp': decode_timestamp}


def object_hook(dct):
    if dct is None:
        return 'n/a'
    if '__type__' in dct:
        name = dct['__type__']
        decoder = DECODE_MAP[name]
        return decoder(dct, name)
    return dct

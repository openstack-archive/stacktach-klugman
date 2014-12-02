import datetime
import timex
import iso8601


def decode_datetime(dct, name):
    return iso8601.parse_date(dct['datetime'], default_timezone=None)


def decode_timerange(dct, name):
    begin = iso8601.parse_date(dct['begin'], default_timezone=None)
    end = iso8601.parse_date(dct['end'], default_timezone=None)
    return timex.TimeRange(begin=begin, end=end)


def decode_timestamp(dct, name):
    timestamp = iso8601.parse_date(dct['timestamp'], default_timezone=None)
    return timex.Timestamp(timestamp)


DECODE_MAP = {'datetime': decode_datetime,
              'timex.TimeRange': decode_timerange,
              'timex.Timestamp': decode_timestamp}


def object_hook(dct):
    if '__type__' in dct:
        name = dct['__type__']
        decoder = DECODE_MAP[name]
        return decoder(dct, name)
    return dct

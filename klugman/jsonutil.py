import datetime
import timex
import iso8601


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

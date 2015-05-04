# Copyright (c) 2014 Dark Secret Software Inc.
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


import prettytable

import base


class Streams(object):
    def __init__(self, url, subparser=None):
        self.url = url
        if subparser:
            parser = subparser.add_parser('streams')
            parser.add_argument(
                '--name', metavar='trigger_name',
                help='Return streams of type trigger_name.')
            parser.add_argument(
                '--from', metavar='datetime', dest='_from',
                help='Return streams last updated after datetime')
            parser.add_argument(
                '--to', metavar='datetime',
                help='Return streams last updated before datetime')
            parser.add_argument(
                '--traits', metavar='trait_list',
                help='Return streams with specific distinguishing traits.')
            parser.add_argument(
                '--details', action='store_true',
                default=False,
                help='Return full event details.')
            parser.add_argument(
                '--state', choices=['active', 'firing',
                                    'expiring', 'error',
                                    'expire_error', 'completed',
                                    'retry_fire',
                                    'retry_expire'],
                help='Only return streams in this state.')

            group = parser.add_mutually_exclusive_group()
            group.add_argument(
                '--count', action='store_true',
                default=False,
                help='Return a count of streams matching filter criteria.')
            group.add_argument(
                '--id', metavar='stream_id', dest='stream_id',
                help='Return a single specific stream by id.')

    def get_streams_count(self, from_datetime=None, to_datetime=None,
                          traits=None, state=None, name=None, debug=False):
        if traits:
            traits = ",".join(["%s:%s" % item for item in traits.items()])
        cmd = "streams/count"
        params = base.remove_empty({'older_than': from_datetime,
                                    'younger_than': to_datetime,
                                    'name': name,
                                    'state': state,
                                    'distinguishing_traits': traits})

        return base.get(self.url, cmd, params, debug=debug)

    def get_streams(self, from_datetime=None, to_datetime=None,
                    traits=None, name=None, stream_id=None, debug=False,
                    state=None, details=None):
        if stream_id:
            params = base.remove_empty({'details': details})
            return base.get(self.url, "streams/%s" % stream_id, params,
                            debug=debug)

        if traits:
            traits = ",".join(["%s:%s" % item for item in traits.items()])
        cmd = "streams"
        params = base.remove_empty({'older_than': from_datetime,
                                    'younger_than': to_datetime,
                                    'name': name,
                                    'details': details,
                                    'state': state,
                                    'distinguishing_traits': traits})

        return base.get(self.url, cmd, params, debug=debug)

    def _cmdline(self, arguments):
        _from = arguments._from
        _to = arguments.to
        _name = arguments.name
        _traits = arguments.traits
        _debug = arguments.debug
        _state = arguments.state
        _details = arguments.details

        trait_dict = None
        if _traits:
            trait_pairs = _traits.split(',')
            trait_dict = dict([tuple(item.split(':')) for item in trait_pairs])

        if arguments.count:
            rows = self.get_streams_count(from_datetime=_from, to_datetime=_to,
                                          name=_name, traits=trait_dict,
                                          state=_state, debug=_debug)
            print(rows)
            keys = ['count']
            base.dump_response(keys, rows)
            return

        _stream_id = arguments.stream_id
        rows = self.get_streams(from_datetime=_from, to_datetime=_to,
                                name=_name, traits=trait_dict,
                                details=_details, state=_state,
                                stream_id=_stream_id, debug=_debug)

        keys = ['id', 'state', 'name', 'first_event', 'last_event',
                'fire_timestamp', 'expire_timestamp']
        for row in rows:
            x = prettytable.PrettyTable(["Section", "Property", "Value"])
            for key in keys:
                x.add_row(["Stream", key, row.get(key)])

            if 'distinguishing_traits' in row.keys():
                for key, value in row['distinguishing_traits'].items():
                    x.add_row(["D.Trait", key, value])

            print(x)

            if 'events' in row.keys():
                # This has detail rows ... handle those separately.
                print("Events:")
                for event in row['events']:
                    x = prettytable.PrettyTable(["Property", "Value"])
                    sorted_keys = sorted(event.keys())
                    for key in sorted_keys:
                        x.add_row([key, event[key]])
                    print(x)


class Events(object):
    def __init__(self, url, subparser=None):
        self.url = url
        if subparser:
            parser = subparser.add_parser('events')
            parser.add_argument(
                '--name', metavar='event_name',
                help='Return events of type event_name.')
            parser.add_argument(
                '--from', metavar='datetime', dest='_from',
                help='Return events generated before datetime')
            parser.add_argument(
                '--to', metavar='datetime',
                help='Return events generated after datetime')
            parser.add_argument(
                '--traits', metavar='trait_list',
                help='Return events with specific traits.')

            group = parser.add_mutually_exclusive_group()
            group.add_argument(
                '--count', action='store_true',
                default=False,
                help='Return a count of events matching filter criteria.')
            group.add_argument(
                '--msg_id', metavar='message_id',
                help='Return a single specific event by message id.')

    def get_events_count(self, from_datetime=None, to_datetime=None,
                         traits=None, name=None, debug=False):
        if traits:
            traits = ",".join(["%s:%s" % item for item in traits.items()])
        cmd = "events/count"
        params = base.remove_empty({'from_datetime': from_datetime,
                                    'to_datetime': to_datetime,
                                    'event_name': name,
                                    'traits': traits})

        return base.get(self.url, cmd, params, debug=debug)

    def get_events(self, from_datetime=None, to_datetime=None,
                   traits=None, name=None, msg_id=None, debug=False):
        if msg_id:
            return base.get(self.url, "events/%s" % msg_id, {}, debug=debug)

        if traits:
            traits = ",".join(["%s:%s" % item for item in traits.items()])
        cmd = "events"
        params = base.remove_empty({'from_datetime': from_datetime,
                                    'to_datetime': to_datetime,
                                    'event_name': name,
                                    'traits': traits})

        return base.get(self.url, cmd, params, debug=debug)

    def _cmdline(self, arguments):
        _from = arguments._from
        _to = arguments.to
        _name = arguments.name
        _traits = arguments.traits
        _debug = arguments.debug

        trait_dict = None
        if _traits:
            trait_pairs = _traits.split(',')
            trait_dict = dict([tuple(item.split(':')) for item in trait_pairs])

        if arguments.count:
            rows = self.get_events_count(from_datetime=_from, to_datetime=_to,
                                         name=_name, traits=trait_dict,
                                         debug=_debug)
            keys = ['count']
            base.dump_response(keys, rows)
            return

        _msg_id = arguments.msg_id
        rows = self.get_events(from_datetime=_from, to_datetime=_to,
                               name=_name, traits=trait_dict,
                               msg_id=_msg_id, debug=_debug)

        if isinstance(rows, dict):
            rows = [rows]
        keys = set()
        for row in rows:
            keys.update(row.keys())
        keys = sorted(list(keys))
        base.dump_response(keys, rows)


class V1(object):
    def __init__(self, url, parser):
        subparser = parser.add_subparsers(dest='command',
                                          help="V1 API commands")
        self.resources = {'events': Events(url, subparser),
                          'streams': Streams(url, subparser)}

    def dispatch(self, arguments):
        # We could let argparse dispatch automatically, but I
        # want to make this work as a library as well as a
        # cmdline tool, so it goes to an object vs. a function.
        cmd = arguments.command

        # This shouldn't be needed, but I'm being paranoid.
        if cmd not in self.resources:
            print("Unknown command: '%s'" % cmd)
            return

        self.resources[cmd]._cmdline(arguments)

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


import base
import json
import jsonutil
import prettytable
import sys

from docopt import docopt


def check_state(state):
    if state and state not in ["active", "firing", "expiring", "error",
                               "expire_error", "completed",
                               "retry_fire", "retry_expire"]:
        print "Invalid state. %s not one of 'active, firing, " \
              "expiring, error, expire_error, completed, " \
              "retry_fire or retry_expire" % state
        sys.exit(1)


class Streams(object):
    """usage:
        klugman.py streams [options]

      options:
      --id <id>
                get stream with id
      --details
                return events with each stream
      --state <state>
                return streams in state
      --older_than <datetime>
                list streams where first_event < <datetime>
      --younger_than <datetime>
                list streams where last_event > <datetime>
      --trigger_name <name>
                list streams with given trigger definition
      --distinguishing_traits <dtraits>
                list stream with specific distriquishing traits

      Stream states:
      collecting - collecting events
      ready - ready for processing
      triggered - being processed
      processed - processing completed
      error - pipeline processing failed
      commit_error - pipeline result commit failed

      Distinguishing trait format:
      "trait:value;trait:value;..."
    """

    def cmdline(self, version, cmdline):
        arguments = docopt(Streams.__doc__, argv=cmdline)
        debug = version.base_args['--debug']
        if debug:
            print arguments

        response = self.do_streams(version, arguments)
        # Handle cmdline output here, not in do_foo()
        raw_rows = response.json(object_hook=jsonutil.object_hook)

        if debug:
            print json.dumps(raw_rows, indent=2)

        # TODO(sandy): This should come from the server-issued
        # schema at some point.

        keys = ['id', 'state', 'name', 'first_event', 'last_event',
                'fire_timestamp', 'expire_timestamp']
        for row in raw_rows:
            x = prettytable.PrettyTable(["Section", "Property", "Value"])
            for key in keys:
                x.add_row(["Stream", key, row.get(key)])

            if 'distinguishing_traits' in row.keys():
                for key, value in row['distinguishing_traits'].items():
                    x.add_row(["D.Trait", key, value])

            print x

            if 'events' in row.keys():
                # This has detail rows ... handle those separately.
                print "Events:"
                for event in row['events']:
                    x = prettytable.PrettyTable(["Property", "Value"])
                    sorted_keys = sorted(event.keys())
                    for key in sorted_keys:
                        x.add_row([key, event[key]])
                    print x


    def do_streams(self, version, arguments):
        sid = arguments.get('--id')
        state = arguments.get('--state')
        older = arguments.get('--older_than')
        younger = arguments.get('--younger_than')
        trigger = arguments.get('--trigger_name')
        traits = arguments.get('--distinguishing_traits')
        details = arguments.get('--details')

        check_state(state)
        cmd = "streams"
        if sid:
            cmd = "streams/%s" % sid
            return base.get(version.base_url, cmd, {'details': details})

        params = base.remove_empty({'state': state,
                                    'older_than': older,
                                    'younger_than': younger,
                                    'trigger_name': trigger,
                                    'distinguishing_traits': traits,
                                    'details': details})

        return base.get(version.base_url, cmd, params)


class NumStreams(object):
    """usage:
        klugman.py num-streams [options]

      options:
      --state <state>
                return streams in state
      --older_than <datetime>
                list streams older than datetime
      --older_than <datetime>
                list streams where first_event < <datetime>
      --younger_than <datetime>
                list streams where last_event > <datetime>
      --distinguishing_traits <dtraits>
                list stream with specific distriquishing traits

      Stream states:
      active = collecting events
      firing = about to process events
      expiring = about to expire stream
      error = pipeline processing failed
      expire_error = pipeline expiry failed
      completed = stream processing completed
      retry_fire = re-attempt pipeline firing
      retry_expire = re-attempt pipeline expiry

      Distinguishing trait format:
      "trait:value;trait:value;..."
    """

    def cmdline(self, version, cmdline):
        arguments = docopt(NumStreams.__doc__, argv=cmdline)
        debug = version.base_args['--debug']
        if debug:
            print arguments

        response = self.do_stream_count(version, arguments)
        raw_rows = response.json(object_hook=jsonutil.object_hook)

        keys = ['count']
        base.dump_response(keys, raw_rows)

    def do_stream_count(self, version, arguments):
        state = arguments.get('--state')
        older = arguments.get('--older_than')
        younger = arguments.get('--younger_than')
        trigger = arguments.get('--trigger_name')
        traits = arguments.get('--distinguishing_traits')

        check_state(state)

        cmd = "streams/count"
        params = base.remove_empty({'state': state,
                                    'older_than': older,
                                    'younger_than': younger,
                                    'trigger_name': trigger,
                                    'distinguishing_traits': traits})

        return base.get(version.base_url, cmd, params)


class Events(object):
    """usage:
        klugman.py events [options]

      options:
      --debug
      --name <name>
                return events of type <name>
      --from <datetime>
                list events generated before datetime
      --to <datetime>
                list events generated after datetime
      --traits <traits>
                list events with specific traits
      --msg_id <message_id>
                get event with <message_id>

      Trait format:
      "trait:value;trait:value;..."
    """

    def cmdline(self, version, cmdline):
        arguments = docopt(Events.__doc__, argv=cmdline)
        debug = version.base_args['--debug']
        if debug:
            print arguments

        response = self.do_event(version, arguments)
        raw_rows = response.json(object_hook=jsonutil.object_hook)

        keys = set()
        for row in raw_rows:
            keys.update(row.keys())
        keys = sorted(list(keys))
        base.dump_response(keys, raw_rows)

    def do_event(self, version, arguments):
        _from = arguments.get('--from')
        _to = arguments.get('--to')
        name = arguments.get('--name')
        traits = arguments.get('--traits')
        msg_id = arguments.get('--msg_id')

        if msg_id:
            cmd = "events/%s" % msg_id
            return base.get(version.base_url, cmd, {})

        cmd = "events"
        params = base.remove_empty({'from_datetime': _from,
                                    'to_datetime': _to,
                                    'event_name': name,
                                    'traits': traits})

        return base.get(version.base_url, cmd, params)


class NumEvents(object):
    """usage:
        klugman.py num-events [options]

      options:
      --debug
      --name <name>
                return events of type <name>
      --from <datetime>
                list events generated before datetime
      --to <datetime>
                list events generated after datetime
      --traits <traits>
                list events with specific traits

      Trait format:
      "trait:value;trait:value;..."
    """

    def cmdline(self, version, cmdline):
        arguments = docopt(NumEvents.__doc__, argv=cmdline)
        debug = version.base_args['--debug']
        if debug:
            print arguments

        response = self.do_event(version, arguments)
        raw_rows = response.json(object_hook=jsonutil.object_hook)

        keys = ['count']
        base.dump_response(keys, raw_rows)

    def do_event(self, version, arguments):
        _from = arguments.get('--from')
        _to = arguments.get('--to')
        name = arguments.get('--name')
        traits = arguments.get('--traits')

        cmd = "events/count"
        params = base.remove_empty({'from_datetime': _from,
                                    'to_datetime': _to,
                                    'event_name': name,
                                    'traits': traits})

        return base.get(version.base_url, cmd, params)


class V1(base.Impl):
    """usage:
        klugman.py streams [<args>...] [options]
        klugman.py num-streams [<args>...] [options]
        klugman.py events [<args>...] [options]
        klugman.py num-events [<args>...] [options]

        -h, --help  show command options
    """

    def __init__(self, base_url, base_args):
        cmds = {'streams': Streams(),
                'num-streams': NumStreams(),
                'events': Events(),
                'num-events': NumEvents()}
        super(V1, self).__init__(base_url, base_args, cmds, V1.__doc__)

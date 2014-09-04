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

from docopt import docopt


class Streams(object):
    """usage:
        klugman.py streams [options]

      options:
      --id <id>
                get stream with id
      --state <state>
                return streams in state
      --older_than <datetime>
                list streams older than datetime
      --younger_than <datetime>
                list streams younger than datetime
      --trigger_name <name>
                list streams with given trigger definition
      --distinquishing_traits <dtraits>
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
        if version.base_args['--debug']:
            print arguments

        response = self.do_streams(version, arguments)
        # Handle cmdline output here, not in do_foo()
        raw_rows = response.json()

        # TODO(sandy): This should come from the server-issued
        # schema at some point.
        keys = ['stream_id', 'state', 'last_updated', 'trigger_name',
                'distinquishing_traits']
        base.dump_response(keys, raw_rows)

    def do_streams(self, version, arguments):
        sid = arguments.get('--id')
        state = arguments.get('--state')
        older = arguments.get('--older_than')
        younger = arguments.get('--younger_than')
        trigger = arguments.get('--trigger_name')
        traits = arguments.get('--distinquishing_traits')

        cmd = "streams"
        if sid:
            cmd = "streams/%d" % sid
        params = base.remove_empty({'state': state,
                                    'older_than': older,
                                    'younger_than': younger,
                                    'trigger_name': trigger,
                                    'distinquishing_traits': traits})

        return base.get(version.base_url, cmd, params)


class V1(base.Impl):
    """usage:
        klugman.py streams [options]

        -h, --help  show command options
    """

    def __init__(self, base_url, base_args):
        cmds = {'streams': Streams()}
        super(V1, self).__init__(base_url, base_args, cmds, V1.__doc__)

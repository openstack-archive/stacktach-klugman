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


class Events(object):
    """usage:
        klugman.py events [options]

      options:
      -i, --id <id>
                filter by event ID
      -r, --request_id <request_id>
                filter by Request ID
      -s, --start <start_datetime>
                starting datetime range
      -e, --end <end_datetime>
                ending datetime range

      notes:
      -r isn't needed if -i is supplied.
    """

    def cmdline(self, version, cmdline):
        arguments = docopt(Events.__doc__, argv=cmdline)
        if version.base_args['--debug']:
            print arguments

        response = self.do_events(version, arguments)
        # Handle cmdline output here, not in do_foo()
        raw_rows = response.json()

        # TODO(sandy): This should come from the server-issued
        # schema at some point.
        keys = ['message_id', 'request_id', 'when', 'name']
        base.dump_response(keys, raw_rows)

    def do_events(self, version, arguments):
        eid = arguments.get('--id')
        rid = arguments.get('--request_id')
        start = arguments.get('--start')
        end = arguments.get('--end')

        cmd = "events"
        if eid:
            cmd = "events/%d" % eid
        params = base.remove_empty({'request_id': rid,
                                    'start_ts': start,
                                    'end_ts': end})

        return base.get(version.base_url, cmd, params)


class V1(base.Impl):
    """usage:
        klugman.py events [options]

        -h, --help  show command options
    """

    def __init__(self, base_url, base_args):
        cmds = {'events': Events()}
        super(V1, self).__init__(base_url, base_args, cmds, V1.__doc__)

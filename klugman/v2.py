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


"""usage:
    klugman.py events [options]
    klugman.py events (-h | --help)

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


import base

from docopt import docopt


class V2(object):
    def __init__(self, base_url, base_args):
        self.base_url = base_url
        self.base_args = base_args

    def dispatch(self, cmdline):
        self.arguments = docopt(__doc__, argv=cmdline)
        if self.base_args['--debug']:
            print self.arguments

        if self.arguments['events']:
            response = self.do_events()
            # handle cmdline output here.
            print response.json()

    def do_events(self):
        eid = self.arguments.get('--id')
        rid = self.arguments.get('--request_id')
        start = self.arguments.get('--start')
        end = self.arguments.get('--end')

        cmd = "events"
        if eid:
            cmd = "events/%d" % eid
        params = base._remove_empty({'request_id': rid,
                                     'start_ts': start,
                                     'end_ts': end})

        return base.get(self.base_url, cmd, params)

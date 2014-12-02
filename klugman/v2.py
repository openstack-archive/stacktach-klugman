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
import v1
import jsonutil

from docopt import docopt
import requests


class Archives(object):
    """usage:
        klugman.py archives <start_datetime> <end_datetime> [options]

       options:
       -h, --help
       <start_datetime>  starting datetime range
       <end_datetime>    ending datetime range

    """

    def cmdline(self, version, cmdline):
        arguments = docopt(Archives.__doc__, argv=cmdline)
        if version.base_args['--debug']:
            print arguments

        response = self.do_archives(version, arguments)
        raw_rows = response.json(object_hook=jsonutil.object_hook)

        keys = ['id', 'filename']
        base.dump_response(keys, raw_rows)

    def do_archives(self, version, arguments):
        start = arguments.get('--start')
        end = arguments.get('--end')

        cmd = "archives"
        params = base.remove_empty({'start_ts': start,
                                    'end_ts': end})

        return base.get(version.base_url, cmd, params)


class V2(base.Impl):

    # Note the [<args>...] [options] approach
    # which basically says "anything is acceptable".
    # We will be more strict in the actual command handler.
    """Klugman - StackTach.v3 client

Usage:
   klugman.py [options] streams [<args>...]
   klugman.py [options] archives [<args>...]

Options:
   -h, --help  show command options
    """

    def __init__(self, base_url, base_args):
        cmds = {'streams': v1.Streams(),
                'archives': Archives()}
        super(V2, self).__init__(base_url, base_args, cmds, V2.__doc__)

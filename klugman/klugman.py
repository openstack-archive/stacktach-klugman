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

"""Klugman - cmdline and client library for StackTach.v3

Usage:
  klugman.py [options] <command> [<args>...]
  klugman.py (-h | --help)
  klugman.py --version

Options:
  -h --help     Show this help message
  --version     Show klugman version
  --debug       Debug mode
  -a, --api_version <api_version>
                Which API version to use [default: latest]
  --url <url>   StackTach.v3 server url [default: http://localhost:8000]

For a list of possible StackTach commands, use:
   klugman help

"""

from docopt import docopt


import v1
import v2

versions = {1: v1.V1, 2: v2.V2}
latest = 1


def main():
    arguments = docopt(__doc__, options_first=True)
    if arguments['--debug']:
        print arguments

    version = arguments["--api_version"]
    if version == "latest":
        version = latest
    else:
        version = int(version)
    impl = versions[version]

    url = "%s/v%d" % (arguments["--url"], version)
    cmd = arguments['<command>']
    argv = [cmd] + arguments['<args>']

    api = impl(url, arguments)
    if cmd == 'help':
        print api.__doc__
    else:
        api.dispatch(argv)


if __name__ == '__main__':
    main()

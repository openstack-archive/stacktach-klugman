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

import argparse

import v1

versions = {1: v1.V1}
latest = 1


def _get_base_parser():
    parser = argparse.ArgumentParser(description='Klugman cmdline tool')
    parser.add_argument('--version', metavar='version', type=int,
                        default=latest, help='Which api version to use.')
    parser.add_argument('url', metavar='url',
                        help='The API endpoint url')
    parser.add_argument('--debug', action='store_true',
                        default=False, help='Enable debugging.')
    return parser


def main():
    parser = _get_base_parser()
    parser.add_argument('args', nargs=argparse.REMAINDER)
    arguments = parser.parse_args()

    version = arguments.version
    impl = versions[version]

    url = "%s/v%d" % (arguments.url, version)

    # Ok, we got past the basics. Add the subparsers and try again ...
    parser = _get_base_parser()
    api = impl(url, parser)
    arguments = parser.parse_args()

    api.dispatch(arguments)


if __name__ == '__main__':
    main()

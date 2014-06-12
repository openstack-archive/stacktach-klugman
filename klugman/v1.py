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
    klugman.py events [-irse]
    klugman.py events (-h | --help)

  options:
  -i <id>              filter by event <id>
  -r <request_id>      filter by <request_id>
  -s <start_datetime>  starting datetime range
  -e <end_datetime>    ending datetime range

"""



from docopt import docopt


class V1(object):

    def __init__(self, base_url, base_args, cmdline):
        arguments = docopt(__doc__, argv=cmdline)
        print arguments

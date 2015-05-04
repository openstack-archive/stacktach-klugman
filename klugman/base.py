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

import jsonutil

import prettytable
import requests


def remove_empty(kv):
    """Remove kv pairs from dictionary where value is empty."""
    return dict([(k, v) for k, v in kv.iteritems() if v])


def dump_response(keys, rows):
    for row in rows:
        x = prettytable.PrettyTable(["Property", "Value"])
        for key in keys:
            if key in row:
                x.add_row([key, row[key]])
        print(x)


def get(url, cmd, params, debug=False):
    final = "%s/%s" % (url, cmd)
    if debug:
        print('URL: %s' % final)
        for item in params.items():
            print("   : %s='%s'" % item)
    ret = requests.get(final, params=params)
    ret.raise_for_status()
    return ret.json(object_hook=jsonutil.object_hook)

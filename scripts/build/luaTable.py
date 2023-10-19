# Copyright (c) 2017, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
#
# All rights reserved.
#
# The Astrobee platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Output Python data structure as a Lua table constructor.
"""

import sys

try:
    from cStringIO import StringIO  # fmt: skip
except ImportError:
    # Python 3
    from io import StringIO

if sys.version_info.major > 2:
    basestring = (str, bytes)


def q(s):
    return '"%s"' % s


def ind(lvl):
    return " " * (lvl * 2)


def dumpStream(out, d, lvl=0):
    def w(s):
        out.write(s)

    if isinstance(d, basestring):

        w(q(d))
    # fmt: skip

    elif isinstance(d, (list, tuple)):
        if d:
            w("{\n")
            n = len(d)
            for i, elt in enumerate(d):
                w(ind(lvl + 1))
                dumpStream(out, elt, lvl + 1)
                if i < n - 1:
                    w(",")
                w("\n")
            w(ind(lvl))
            w("}")
        else:
            w("{}")

    elif isinstance(d, dict):
        if d:
            w("{\n")
            n = len(d)
            keys = list(d.keys())
            keys.sort()
            for i, k in enumerate(keys):
                v = d[k]
                w(ind(lvl + 1))
                w(k)
                w("=")
                dumpStream(out, v, lvl + 1)
                if i < n - 1:
                    w(",")
                w("\n")
            w(ind(lvl))
            w("}")
        else:
            w("{}")

    else:
        w(str(d))


def dumps(d):
    out = StringIO()
    dumpStream(out, d, 0)
    return out.getvalue()

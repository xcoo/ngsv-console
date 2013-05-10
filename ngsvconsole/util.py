# -*- coding: utf-8 -*-

#
#   ngsv-console
#   http://github.com/xcoo/ngsv-console
#   Copyright (C) 2012-2013, Xcoo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import

import os


def get_pretty_size(path):
    size = os.path.getsize(path)
    if size < 1000:
        return '%dB' % size
    elif size < 1000 ** 2:
        return '%f.1KB' % (size / 1000.0)
    elif size < 1000 ** 3:
        return '%.1fMB' % (size / (1000.0 ** 2))
    elif size < 1000 ** 4:
        return '%.1fGB' % (size / (1000.0 ** 3))
    elif size < 1000 ** 5:
        return '%.1fTB' % (size / (1000.0 ** 4))
    else:
        return '%.1fPB' % (size / (1000.0 ** 5))

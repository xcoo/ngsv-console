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

__author__ = 'Toshiki Takeuchi'
__copyright__ = 'Copyright (C) 2012-2013, Xcoo, Inc.'
__license__ = 'Apache License 2.0'
__maintainer__ = 'Toshiki Takeuchi'
__email__ = 'developer@xcoo.jp'

from flask import redirect, request, url_for

from ngsvconsole import app


@app.route('/api/search', methods=['POST'])
def api_search():
    req_query = ''
    if 'query' in request.form:
        req_query = request.form['query']

    req_type = 'all'
    if 'type' in request.form:
        req_type = request.form['type']

    req_filename = 'false'
    if 'filename' in request.form:
        req_filename = 'true'

    req_tag = 'false'
    if 'tag' in request.form:
        req_tag = 'true'

    return redirect(url_for('search',
                            q=req_query,
                            t=req_type,
                            fn=req_filename,
                            tag=req_tag))

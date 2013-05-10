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
from __future__ import print_function
from __future__ import unicode_literals

import os
import os.path
import sys


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import SharedDataMiddleware
from celery.result import BaseAsyncResult
from celery.task.control import inspect

from ngsvconsole.config import Config

app = Flask(__name__)

try:
    ini = os.environ['NGSV_CONSOLE_CONFIG']
except KeyError:
    sys.exit('Not found "ngsv.ini"')

conf = Config(ini)

app.debug = conf.debug
app.testing = conf.testing

app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {'/': os.path.join(os.path.dirname(__file__), 'static')})

tasks_info = []
ws_viewer_sockets = {}


def list_active_task():
    i = inspect()
    active = i.active()
    if active is not None:
        for v in active.values():
            for t in v:
                r = BaseAsyncResult(t['id'])
                r.task_name = t['name']
                tasks_info.append({'result': r})

list_active_task()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s?charset=utf8' \
                                        % (conf.db_user,
                                           conf.db_password,
                                           conf.db_host,
                                           conf.db_name)
db = SQLAlchemy(app)

# Page and requests
import ngsvconsole.views
import ngsvconsole.api.upload
import ngsvconsole.api.tag
import ngsvconsole.api.viewer
import ngsvconsole.api.search

#!/usr/bin/env python
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

from celery import Celery
import ngsvconsole.taskserver.celeryconfig as celeryconfig

celery = Celery('ngsvconsole.taskserver.celery',
                include=['ngsvconsole.taskserver.tasks'])

celery.config_from_object(celeryconfig)

if __name__ == '__main__':
    celery.start()

# -*- coding: utf-8 -*-

#
#   ngsv-console
#   http://github.com/xcoo/ngsv-console
#   Copyright (C) 2013, Xcoo, Inc.
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

from sql import get_time, escape


class Cnv:

    def __init__(self, db):
        self.db = db

    def append(self, filename):
        SQL_TEMPLATE = u"INSERT INTO cnv (file_name, created_date) " \
            u"VALUES ('%s', %d)"

        sql = SQL_TEMPLATE % (filename, get_time())

        self.db.execute(sql)

    def get_by_filename(self, filename):
        sql = u"SELECT cnv_id, file_name, created_date FROM cnv " \
            u"WHERE file_name = '%s'" % escape(filename)

        result = self.db.execute(sql)

        if len(result) > 0:
            return {'id': result[0][0],
                    'name': result[0][1],
                    'created': result[0][2]}
        else:
            return None

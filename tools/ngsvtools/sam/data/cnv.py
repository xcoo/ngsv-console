# -*- coding: utf-8 -*-

#
#   ngsv
#   http://github.com/xcoo/ngsv
#   Copyright (C) 2012, Xcoo, Inc.
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

class Cnv:

    def __init__(self, db):
        self.db = db

    def append(self, filename, chr_id, chr_start, chr_end, lengths, state,
               copy_number, num_snp, snp_start, snp_end):

        SQL_TEMPLATE = u"INSERT INTO cnv " \
                       u"(file_name, chr_id, chr_start, chr_end, lengths, state, copy_number, num_snp, snp_start, snp_end) " \
                       u"VALUES ('%s', %d, %d, %d, '%s', '%s', %d, %d, '%s','%s')"

        sql = SQL_TEMPLATE % (filename,
                              chr_id,
                              chr_start,
                              chr_end,
                              lengths,
                              state,
                              copy_number,
                              num_snp,
                              snp_start,
                              snp_end)
        print sql

        self.db.execute(sql)

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


class CnvFragment:

    def __init__(self, db):
        self.db = db

    def append(self, cnv_id, chr_id, chr_start, chr_end, lengths, state,
               copy_number, num_snp, snp_start, snp_end):
        SQL_TEMPLATE = u"INSERT INTO cnv_fragment (cnv_id, chr_id, " \
            u"chr_start, chr_end, lengths, state, copy_number, num_snp, " \
            u"snp_start, snp_end) VALUES " \
            u"(%d, %d, %d, %d, '%s', '%s', %d, %d, '%s', '%s')"

        sql = SQL_TEMPLATE % (cnv_id,
                              chr_id,
                              chr_start,
                              chr_end,
                              lengths,
                              state,
                              copy_number,
                              num_snp,
                              snp_start,
                              snp_end)

        self.db.execute(sql)

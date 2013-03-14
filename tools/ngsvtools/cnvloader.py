#!/usr/bin/env python
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

import logging
import os.path
import re

from ngsvtools.sam.data.cnv import Cnv
from ngsvtools.sam.data.cnvfragment import CnvFragment
from ngsvtools.sam.data.chromosome import Chromosome
from ngsvtools.sam.util import trim_chromosome_name
from ngsvtools.exception import AlreadyLoadedError


def load(filepath, db):
    filename = os.path.basename(filepath)

    cnv_data = Cnv(db)
    cnv_fragment_data = CnvFragment(db)
    chromosome_data = Chromosome(db)

    if cnv_data.get_by_filename(filename) is not None:
        raise AlreadyLoadedError('WARNING: Already loaded "%s"' % filename)

    logging.info('begin to load rpkm data from %s' % filepath)

    cnv_data.append(filename)
    cnv = cnv_data.get_by_filename(filename)

    line_count = 0
    cnt = 0
    for l in open(filepath, 'r').readlines():
        row = l[:-1].split()

        if row[0][0] == '#':
            logging.info('%s', row)
        else:
            r = re.compile('[c|C]hr(\w+):([0-9]+)-([0-9]+)')
            m = r.search(row[0])
            chr_num = m.group(1)

            chr_name = trim_chromosome_name(chr_num)
            c = chromosome_data.get_by_name(chr_name)
            if c is None:
                chromosome_data.append(chr_name)
                c = chromosome_data.get_by_name(chr_name)
            chr_id = c['id']

            chr_start = long(m.group(2))
            chr_end = long(m.group(3))

            r = re.compile('numsnp=(\w+)')
            m = r.search(row[1])
            numsnp = long(m.group(1))

            r = re.compile('length=(\w+)')
            m = r.search(row[2])
            length = m.group(1)
#            length = long(length.replace(',', ''))

            r = re.compile('state(\w+),cn=(\w+)')
            m = r.search(row[3])
            state = m.group(1)
            copy_number = long(m.group(2))

            r = re.compile('startsnp=(\w+)')
            m = r.search(row[5])
            startsnp = m.group(1)

            r = re.compile('endsnp=(\w+)')
            m = r.search(row[6])
            endsnp = m.group(1)

            cnv_fragment_data.append(cnv['id'], chr_id, chr_start, chr_end,
                                     length, state, copy_number, numsnp,
                                     startsnp, endsnp)
            cnt += 1

        line_count += 1

    logging.info('read lines: %d' % line_count)
    logging.info('loaded cnv: %d' % cnt)

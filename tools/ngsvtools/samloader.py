#!/usr/bin/env python
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

import sys
import os.path
import re

import pysam

from sam.data.sql import SQLDB
from sam.data.sam import Sam
from sam.data.chromosome import Chromosome
from sam.util import trim_chromosome_name
from config import SQLDB_HOST, SQLDB_USER, SQLDB_PASSWD, SAM_DB_NAME
from exception import AlreadyLoadedError, UnsupportedFileError

def load(filepath, db):
    
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filepath)
    if not re.match('^\.(sam|bam)', ext):
        raise UnsupportedFileError('ERROR: Not supported file format')

    sam_data = Sam(db)
    chr_data = Chromosome(db)

    if sam_data.get_by_filename(filename) is not None:
        raise AlreadyLoadedError('WARNING: Already loaded "%s"' % filename)

    print 'begin to load', filename

    # Convert sam to bam
    if ext == '.sam':
        insam = pysam.Samfile(filepath, 'r')
        filepath = base + '.bam'
        outbam = pysam.Samfile(filepath, 'wb', template=insam)
        for s in insam:
            outbam.write(s)
    
    # Create index if not exist
    bai = filepath + '.bai'
    if not os.path.isfile(bai):
        print 'Create index "%s"' % os.path.basename(bai)
        pysam.index(filepath)
    
    # load sam
    samfile = pysam.Samfile(filepath)
    sam_data.append(filename,
                    samfile.header, samfile.lengths,
                    samfile.mapped,
                    samfile.nreferences, samfile.references)

    # load chromosome
    for ref in samfile.references:
        chr_data.append(trim_chromosome_name(ref))

    return

def main():

    if len(sys.argv) < 2:
        print("No input files")
        sys.exit()

    files = sys.argv[1:]

    db = SQLDB(SAM_DB_NAME, SQLDB_HOST, SQLDB_USER, SQLDB_PASSWD)

    for f in files:
        load(f, db)

if __name__ == '__main__':
    main()
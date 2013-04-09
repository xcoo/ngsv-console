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
__copyright__ = 'Copyright (C) 2012, Xcoo, Inc.'
__license__ = 'Apache License 2.0'
__maintainer__ = 'Toshiki Takeuchi'
__email__ = 'developer@xcoo.jp'

import datetime

from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String, Text, Date

from ngsvconsole import db


class Bed(db.Model):

    __tablename__ = 'bed'

    bed_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(1024), nullable=False)
    created_date = Column(BigInteger, nullable=False)
    track_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    visibility = Column(Integer, nullable=False)
    item_rgb = Column(Integer, nullable=False)

    def __init__(self, file_name, created_data, track_name, description,
                 visibility, item_rgb):
        self.file_name = file_name
        self.created_data = created_data
        self.track_name = track_name
        self.description = description
        self.visibility = visibility
        self.item_rgb = item_rgb

    def __repr__(self):
        if self.bed_id is None:
            return "<bed('%s')>" % (self.file_name)
        else:
            return "<bed('%d', '%s')>" % (self.bed_id, self.file_name)


class Chromosome(db.Model):

    __tablename__ = 'chromosome'

    chr_id = Column(Integer, primary_key=True, autoincrement=True)
    chromosome = Column(String(45), nullable=False, unique=True)

    def __init__(self, chromosome):
        self.chromosome = chromosome

    def __repr__(self):
        if self.chr_id is None:
            return '<chromosome("%s")>' % self.chromosome
        else:
            return '<chromosome("%d", "%s")>' % (self.chr_id, self.chromosome)


class Cytoband(db.Model):

    __tablename__ = 'cytoband'

    cytoband_id = Column(BigInteger, primary_key=True, autoincrement=True)
    chr_id = Column(BigInteger, nullable=False)
    chr_start = Column(BigInteger, nullable=False)
    chr_end = Column(BigInteger, nullable=False)
    name = Column(Text, nullable=False)
    gie_stain = Column(String(255), nullable=False)

    def __init__(self, chr_id, chr_start, chr_end, name, gie_stain):
        self.chr_id = chr_id
        self.chr_start = chr_start
        self.chr_end = chr_end
        self.name = name
        self.gie_stain = gie_stain

    def __repr__(self):
        if self.id is None:
            return '<cytoband("%d", "%d", "%d", "%s", "%s")>' % (
                self.chr_id, self.chr_start, self.chr_end, self.name,
                self.gie_stain)
        else:
            return '<cytoband("%d", "%d", "%d", "%d", "%s", "%s")>' % (
                self.cytoband_id, self.chr_id, self.chr_start, self.chr_end,
                self.name, self.gie_stain)


class Sam(db.Model):

    __tablename__ = 'sam'

    sam_id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(1024), nullable=False)
    created_date = Column(BigInteger, nullable=False)
    header = Column(Text, nullable=False)
    lengths = Column(Text, nullable=False)
    mapped = Column(Integer, nullable=False)
    number_of_chromosomes = Column(Integer, nullable=False)
    chromosomes = Column(Text, nullable=False)

    def __init__(self, file_name, created_data, header, lengths, mapped,
                 number_of_chromosomes, chromosomes):
        self.file_name = file_name
        self.created_data = created_data
        self.header = header
        self.lengths = lengths
        self.mapped = mapped
        self.number_of_chromosomes = number_of_chromosomes
        self.chromosomes = chromosomes

    def __repr__(self):
        if self.sam_id is None:
            return "<sam('%s')>" % (self.file_name)
        else:
            return "<sam('%d', '%s')>" % (self.sam_id, self.file_name)


class Tag(db.Model):

    __tablename__ = 'tag'

    tag_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(Date, nullable=False,
                        default=datetime.datetime.utcnow())
    updated_at = Column(Date, nullable=False,
                        default=datetime.datetime.utcnow())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.tag_id is None:
            return "<tag(name='%s', created_at='%s', updated_at='%s')>" \
                % (self.name, self.created_at, self.updated_at)
        else:
            return "<tag(tag_id=%d, name='%s', created_at='%s', " \
                "updated_at='%s')>" \
                % (self.tag_id, self.name, self.created_at, self.updated_at)


class SamTag(db.Model):

    __tablename__ = 'sam_tag'

    tag_id = Column(BigInteger, primary_key=True, nullable=False)
    sam_id = Column(BigInteger, primary_key=True, nullable=False)

    def __init__(self, tag_id, sam_id):
        self.tag_id = tag_id
        self.sam_id = sam_id

    def __repr__(self):
        return "<tag_ref(tag_id=%d, sam_id=%d)>" % (self.tag_id, self.sam_id)


class BedTag(db.Model):

    __tablename__ = 'bed_tag'

    tag_id = Column(BigInteger, primary_key=True, nullable=False)
    bed_id = Column(BigInteger, primary_key=True, nullable=False)

    def __init__(self, tag_id, bed_id):
        self.tag_id = tag_id
        self.bed_id = bed_id

    def __repr__(self):
        return "<tag_ref(tag_id=%d, bed_id=%d)>" % (self.tag_id, self.bed_id)

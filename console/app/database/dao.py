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

__author__ = 'Toshiki Takeuchi'
__copyright__ = 'Copyright (C) 2012, Xcoo, Inc.'
__license__ = 'Apache License 2.0'
__maintainer__ = 'Toshiki Takeuchi'
__email__ = 'developer@xcoo.jp'

import datetime

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.database.models import Sam
from app.database.models import Bed
from app.database.models import Chromosome
from app.database.models import Cytoband
from app.database.models import Tag, SamTag, BedTag


class SamDao():

    def __init__(self):
        pass

    def all(self):
        query = db.session.query(Sam)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_by_id(self, sam_id):
        query = db.session.query(Sam).filter_by(sam_id=sam_id)
        try:
            return query.first()
        except NoResultFound:
            return None

    def get_by_filename(self, filename):
        query = db.session.query(Sam).filter_by(file_name=filename)
        try:
            return query.first()
        except NoResultFound:
            return None

    def get_by_tag(self, tag):
        query = db.session.query(Sam) \
            .join(SamTag, SamTag.tag_id == tag.tag_id) \
            .filter(Sam.sam_id == SamTag.sam_id)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_by_tag_id(self, tag_id):
        query = db.session.query(Sam) \
            .join(SamTag, SamTag.tag_id == tag_id) \
            .filter(Sam.sam_id == SamTag.sam_id)
        try:
            return query.all()
        except NoResultFound:
            return None


class BedDao():

    def __init__(self):
        pass

    def all(self):
        query = db.session.query(Bed)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_by_id(self, bed_id):
        query = db.session.query(Bed).filter_by(bed_id=bed_id)
        try:
            return query.first()
        except NoResultFound:
            return None

    def get_by_filename(self, filename):
        query = db.session.query(Bed).filter_by(file_name=filename)
        try:
            return query.first()
        except NoResultFound:
            return None

    def get_by_tag(self, tag):
        query = db.session.query(Bed) \
                          .join(BedTag, BedTag.tag_id == tag.tag_id) \
                          .filter(Bed.bed_id == BedTag.bed_id)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_by_tag_id(self, tag_id):
        query = db.session.query(Bed) \
                          .join(BedTag, BedTag.tag_id == tag_id) \
                          .filter(Bed.bed_id == BedTag.bed_id)
        try:
            return query.all()
        except NoResultFound:
            return None


class ChromosomeDao():

    def __init__(self):
        pass

    def all(self):
        query = db.session.query(Chromosome)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_by_id(self, chr_id):
        query = db.session.query(Chromosome) \
                          .filter(Chromosome.chr_id == chr_id)
        try:
            return query.one()
        except NoResultFound:
            return None


class CytobandDao():

    def __init__(self):
        pass

    def all(self):
        query = db.session.query(Cytoband)
        try:
            return query.all()
        except NoResultFound:
            return None

    def get_end_by_chr_id(self, chr_id):
        query = db.session.query(Cytoband) \
                          .filter(Cytoband.chr_id == chr_id) \
                          .order_by(Cytoband.chr_end.desc())
        try:
            return query.first()
        except NoResultFound:
            return None

    def all_chr_id(self):
        query = db.session.query(Cytoband).group_by(Cytoband.chr_id)
        try:
            return [c.chr_id for c in query.all()]
        except NoResultFound:
            return None


class TagDao():

    def __init__(self):
        pass

    def all(self):
        query = db.session.query(Tag)
        try:
            return query.all()
        except NoResultFound:
            return None

    def _add_tag(self, name):
        tag = Tag(name)
        db.session.add(tag)
        db.session.commit()

    def add_tag_with_sam(self, name, sam):
        tag = self.get_by_name(name)
        if tag is None:
            self._add_tag(name)
            tag = self.get_by_name(name)

        sam_tag_dao = SamTagDao()
        sam_tag = sam_tag_dao.get_by_tag_sam(tag.tag_id, sam.sam_id)
        print tag.tag_id, sam.sam_id
        print 'sam: ', sam_tag
        if sam_tag is None:
            sam_tag = SamTag(tag.tag_id, sam.sam_id)
            db.session.add(sam_tag)

        try:
            db.session.commit()
        except IntegrityError:
            pass

    def add_tag_with_bed(self, name, bed):
        tag = self.get_by_name(name)
        if tag is None:
            self._add_tag(name)
            tag = self.get_by_name(name)

        bed_tag_dao = BedTagDao()
        bed_tag = bed_tag_dao.get_by_tag_bed(tag.tag_id, bed.bed_id)
        print 'bed:', bed_tag
        if bed_tag is None:
            bed_tag = BedTag(tag.tag_id, bed.bed_id)
            db.session.add(bed_tag)

        try:
            db.session.commit()
        except IntegrityError:
            pass

    def update_tag_date(self, tag_id):
        try:
            tag = Tag.query.filter_by(tag_id=tag_id).first()
            tag.updated_at = datetime.datetime.utcnow()
            db.session.commit()
        except NoResultFound:
            pass

    def get_by_id(self, tag_id):
        try:
            return Tag.query.filter_by(tag_id=tag_id).first()
        except NoResultFound:
            return None

    def get_by_name(self, name):
        query = db.session.query(Tag).filter_by(name=name)
        try:
            return query.first()
        except NoResultFound:
            return None

    def get_by_samid(self, sam_id):
        query = db.session.query(Tag) \
            .join(SamTag, SamTag.sam_id == sam_id) \
            .filter(Tag.tag_id == SamTag.tag_id)
        try:
            return [{'id': tag.tag_id,
                     'name': tag.name} for tag in query.all()]
        except NoResultFound:
            return None

    def get_by_bedid(self, bed_id):
        query = db.session.query(Tag) \
            .join(BedTag, BedTag.bed_id == bed_id) \
            .filter(Tag.tag_id == BedTag.tag_id)
        try:
            return [{'id': tag.tag_id,
                     'name': tag.name} for tag in query.all()]
        except NoResultFound:
            return None

    def remove_by_id(self, tag_id):
        db.session.query(SamTag).filter_by(tag_id=tag_id).delete()
        db.session.query(BedTag).filter_by(tag_id=tag_id).delete()
        db.session.query(Tag).filter_by(tag_id=tag_id).delete()

    def remove_sam(self, sam, tag):
        query = db.session.query(SamTag).filter(
            and_(SamTag.tag_id == tag.tag_id, SamTag.sam_id == sam.sam_id))
        query.delete()

    def remove_sam_by_tag_id(self, sam, tag_id):
        query = db.session.query(SamTag).filter(
            and_(SamTag.tag_id == tag_id, SamTag.sam_id == sam.sam_id))
        query.delete()

    def remove_bed(self, bed, tag):
        query = db.session.query(BedTag).filter(
            and_(BedTag.tag_id == tag.tag_id, BedTag.bed_id == bed.bed_id))
        query.delete()

    def remove_bed_by_tag_id(self, bed, tag_id):
        query = db.session.query(BedTag).filter(
            and_(BedTag.tag_id == tag_id, BedTag.bed_id == bed.bed_id))
        query.delete()


class SamTagDao():

    def __init__(self):
        pass

    def get_by_tag_sam(self, tag_id, sam_id):
        try:
            return SamTag.query.filter(
                and_(SamTag.tag_id == tag_id, SamTag.sam_id == sam_id)).first()
        except NoResultFound:
            return None


class BedTagDao():

    def __init__(self):
        pass

    def get_by_tag_bed(self, tag_id, bed_id):
        try:
            return BedTag.query.filter(
                and_(BedTag.tag_id == tag_id, BedTag.bed_id == bed_id)).first()
        except NoResultFound:
            return None

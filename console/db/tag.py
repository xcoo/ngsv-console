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

import datetime

from sqlalchemy import Column
from sqlalchemy import BigInteger, String, Date
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Tag(Base):

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


class SamTag(Base):

    __tablename__ = 'sam_tag'

    tag_id = Column(BigInteger, primary_key=True, nullable=False)
    sam_id = Column(BigInteger, primary_key=True, nullable=False)

    def __init__(self, tag_id, sam_id):
        self.tag_id = tag_id
        self.sam_id = sam_id

    def __repr__(self):
        return "<tag_ref(tag_id=%d, sam_id=%d)>" % (self.tag_id, self.sam_id)


class BedTag(Base):

    __tablename__ = 'bed_tag'

    tag_id = Column(BigInteger, primary_key=True, nullable=False)
    bed_id = Column(BigInteger, primary_key=True, nullable=False)

    def __init__(self, tag_id, bed_id):
        self.tag_id = tag_id
        self.bed_id = bed_id

    def __repr__(self):
        return "<tag_ref(tag_id=%d, bed_id=%d)>" % (self.tag_id, self.bed_id)


class TagDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Tag)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def _add_tag(self, name):
        session = scoped_session(sessionmaker(bind=self._engine))
        tag = Tag(name)
        session.add(tag)
        session.commit()
        session.close()

    def add_tag_with_sam(self, name, sam):
        session = scoped_session(sessionmaker(bind=self._engine))

        tag = self.get_by_name(name)
        if tag is None:
            self._add_tag(name)
            tag = self.get_by_name(name)

        sam_tag = SamTag(tag.tag_id, sam.sam_id)
        session.add(sam_tag)
        try:
            session.commit()
        except IntegrityError:
            pass  # Ignore duplicate entry error
        finally:
            session.close()

    def add_tag_with_bed(self, name, bed):
        session = scoped_session(sessionmaker(bind=self._engine))

        tag = self.get_by_name(name)
        if tag is None:
            self._add_tag(name)
            tag = self.get_by_name(name)

        bed_tag = BedTag(tag.tag_id, bed.bed_id)
        session.add(bed_tag)
        try:
            session.commit()
        except IntegrityError:
            pass  # Ignore duplicate entry error
        finally:
            session.close()

    def update_tag_date(self, tag_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        try:
            tag = session.query(Tag).filter_by(tag_id=tag_id).first()
            tag.updated_at = datetime.datetime.utcnow()
            session.add(tag)
            session.commit()
        except NoResultFound:
            pass
        finally:
            session.close()

    def get_by_id(self, tag_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Tag).filter_by(tag_id=tag_id)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_name(self, name):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Tag).filter_by(name=name)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

    def remove_by_id(self, tag_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        try:
            session.query(SamTag).filter_by(tag_id=tag_id).delete()
            session.query(BedTag).filter_by(tag_id=tag_id).delete()
            session.query(Tag).filter_by(tag_id=tag_id).delete()
        finally:
            session.close()

    def remove_sam(self, sam, tag):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(SamTag).filter(
            and_(SamTag.tag_id == tag.tag_id, SamTag.sam_id == sam.sam_id))
        try:
            query.delete()
        finally:
            session.close()

    def remove_bed(self, bed, tag):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(BedTag).filter(
            and_(BedTag.tag_id == tag.tag_id, BedTag.bed_id == bed.bed_id))
        try:
            query.delete()
        finally:
            session.close()

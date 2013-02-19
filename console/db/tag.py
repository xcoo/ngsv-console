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

from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Tag(Base):

    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.tag_id is None:
            return "<tag(name='%s')>" % self.name
        else:
            return "<tag(tag_id=%d, name='%s')>" % (self.tag_id, self.name)


class TagRef(Base):

    __tablename__ = 'tag_ref'

    tag_ref_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, nullable=False)
    sam_id = Column(BigInteger)
    bed_id = Column(BigInteger)

    def __init__(self, tag_id, sam_id=None, bed_id=None):
        self.tag_id = tag_id
        self.sam_id = sam_id
        self.bed_id = bed_id

    def __repr__(self):
        if self.tag_ref_id is None:
            return "<tag_ref(tag_id=%d, sam_id=%d, bed_id=%d)>"\
                % (self.tag_id, self.sam_id, self.bed_id)
        else:
            return "<tag_ref(tag_ref_id=%d, tag_id=%d, sam_id=%d, bed_id=%d)>"\
                % (self.tag_ref_id, self.tag_id, self.sam_id, self.bed_id)


class TagDao():

    def __init__(self, engine):
        self._engine = engine

    def _add_tag(self, name):
        session = scoped_session(sessionmaker(bind=self._engine))
        tag = Tag(name)
        session.add(tag)
        session.commit()
        session.close()

    def add_tag_with_sam(self, name, sam):
        session = scoped_session(sessionmaker(bind=self._engine))
        self._add_tag(name)
        tag = self.get_by_name(name)
        tag_ref = TagRef(tag.tag_id, sam_id=sam.sam_id)
        session.add(tag_ref)
        session.commit()
        session.close()

    def add_tag_with_bed(self, name, bed):
        session = scoped_session(sessionmaker(bind=self._engine))
        self._add_tag(name)
        tag = self.get_by_name(name)
        tag_ref = TagRef(tag.tag_id, bed_id=bed.bed_id)
        session.add(tag_ref)
        session.commit()
        session.close()

    def get_by_name(self, name):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Tag).filter(Tag.name==name)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

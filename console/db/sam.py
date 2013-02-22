# -*- coding: utf-8 -*-

#
#   ngsv-console
#   http://github.com/xcoo/ngsv-console
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

from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from db.tag import TagRef

Base = declarative_base()


class Sam(Base):

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


class SamDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Sam)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_filename(self, filename):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Sam).filter_by(file_name=filename)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_tag(self, tag):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Sam)\
            .join(TagRef, TagRef.tag_id == tag.tag_id)\
            .filter(Sam.sam_id == TagRef.sam_id)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

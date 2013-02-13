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
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Chromosome(Base):

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


class ChromosomeDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Chromosome)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_id(self, chr_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Chromosome).filter(Chromosome.chr_id==chr_id)
        try:
            return query.one()
        except NoResultFound:
            return None
        finally:
            session.close()

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

from sqlalchemy import Column
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

class Cytoband(Base):

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
        if self.id == None:
            return '<cytoband("%d", "%d", "%d", "%s", "%s")>' % (self.chr_id,
                                                                 self.chr_start,
                                                                 self.chr_end,
                                                                 self.name,
                                                                 self.gie_stain)
        else:
            return '<cytoband("%d", "%d", "%d", "%d", "%s", "%s")>' % (self.cytoband_id,
                                                                       self.chr_id,
                                                                       self.chr_start,
                                                                       self.chr_end,
                                                                       self.name,
                                                                       self.gie_stain)

class CytobandDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Cytoband)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_end_by_chr_id(self, chr_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Cytoband).filter(Cytoband.chr_id==chr_id).order_by(Cytoband.chr_end.desc())
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

    def all_chr_id(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Cytoband).group_by(Cytoband.chr_id)
        try:
            return [c.chr_id for c in query.all()]
        except NoResultFound:
            return None
        finally:
            session.close()

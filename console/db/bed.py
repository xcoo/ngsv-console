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

Base = declarative_base()


class Bed(Base):

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

    def __repr__(self):  # TODO
        if self.bed_id is None:
            return "<thumb('%s', '%s', '%s')>" % (self.original,
                                                  self.created_at,
                                                  self.updated_at)
        else:
            return "<thumb('%d', '%s', '%s', '%s')>" % (self.bed_id,
                                                        self.original,
                                                        self.created_at,
                                                        self.updated_at)


class BedDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Bed)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

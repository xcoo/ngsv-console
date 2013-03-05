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

__author__ = 'Toshiki Takeuchi'
__copyright__ = 'Copyright (C) 2012, Xcoo, Inc.'
__license__ = 'Apache License 2.0'
__maintainer__ = 'Toshiki Takeuchi'
__email__ = 'developer@xcoo.jp'

from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from db.tag import BedTag

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

    def __repr__(self):
        if self.bed_id is None:
            return "<bed('%s')>" % (self.file_name)
        else:
            return "<bed('%d', '%s')>" % (self.bed_id, self.file_name)


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

    def get_by_filename(self, filename):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Bed).filter_by(file_name=filename)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_tag(self, tag):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Bed) \
            .join(BedTag, BedTag.tag_id == tag.tag_id) \
            .filter(Bed.bed_id == BedTag.bed_id)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_tag_id(self, tag_id):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Bed) \
            .join(BedTag, BedTag.tag_id == tag_id) \
            .filter(Bed.bed_id == BedTag.bed_id)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

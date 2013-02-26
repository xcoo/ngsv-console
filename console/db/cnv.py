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
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Cnv(Base):

    __tablename__ = 'cnv'

    cnv_id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(1024), nullable=False)
    chr_id = Column(BigInteger, nullable=False)
    chr_start = Column(BigInteger, nullable=False)
    chr_end = Column(BigInteger, nullable=False)
    lengths = Column(Text, nullable=False)
    state = Column(String(45), nullable=False)
    copy_number = Column(BigInteger, nullable=False)
    num_snp = Column(BigInteger, nullable=False)
    snp_start = Column(String(45), nullable=False)
    snp_end = Column(String(45), nullable=False)

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


class CnvDao():

    def __init__(self, engine):
        self._engine = engine

    def all(self):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Cnv)
        try:
            return query.all()
        except NoResultFound:
            return None
        finally:
            session.close()

    def get_by_filename(self, filename):
        session = scoped_session(sessionmaker(bind=self._engine))
        query = session.query(Cnv).filter_by(file_name=filename)
        try:
            return query.first()
        except NoResultFound:
            return None
        finally:
            session.close()

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

import datetime

from flask import request, redirect

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ngsvconsole.app import app, db
from ngsvconsole.models import Sam, Bed, Tag, SamTag, BedTag


@app.route('/api/tag/new', methods=['POST'])
def tag_new():
    tag_name = request.form['tag-name']
    if not tag_name:
        return redirect('/manager')

    try:
        sam_filenames = request.form.getlist('sam')
        for sam_filename in sam_filenames:
            sam = Sam.query.filter(Sam.file_name == sam_filename).first()
            add_tag_with_sam(tag_name, sam)
    except KeyError:
        pass

    try:
        bed_filenames = request.form.getlist('bed')
        for bed_filename in bed_filenames:
            bed = Bed.query.filter(Bed.file_name == bed_filename).first()
            add_tag_with_bed(tag_name, bed)
    except KeyError:
        pass

    return redirect('/manager')


def add_tag_with_sam(name, sam):
    tag = Tag.query.filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name)
        db.session.add(tag)
        db.session.commit()
        tag = Tag.query.filter(Tag.name == name).first()

    sam_tag = SamTag.query.filter(
        and_(SamTag.tag_id == tag.tag_id,
             SamTag.sam_id == sam.sam_id)).first()
    if sam_tag is None:
        sam_tag = SamTag(tag.tag_id, sam.sam_id)
        db.session.add(sam_tag)

    try:
        db.session.commit()
    except IntegrityError:
        pass


def add_tag_with_bed(name, bed):
    tag = Tag.query.filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name)
        db.session.add(tag)
        db.session.commit()
        tag = Tag.query.filter(Tag.name == name).first()

    bed_tag = BedTag.query.filter(
        and_(BedTag.tag_id == tag.tag_id,
             BedTag.bed_id == bed.bed_id)).first()
    if bed_tag is None:
        bed_tag = BedTag(tag.tag_id, bed.bed_id)
        db.session.add(bed_tag)

    try:
        db.session.commit()
    except IntegrityError:
        pass


def update_tag_date(tag_id):
    try:
        tag = Tag.query.filter_by(tag_id=tag_id).first()
        tag.updated_at = datetime.datetime.utcnow()
        db.session.commit()
    except NoResultFound:
        pass


@app.route('/api/tag/update', methods=['POST'])
def tag_update():
    tag_id = request.form['tag-id']
    if not tag_id:
        return redirect('/manager')

    tag = Tag.query.get(tag_id)

    try:
        req_filenames = request.form.getlist('sam')
        sams = Sam.query.join(SamTag, SamTag.tag_id == tag_id) \
                        .filter(Sam.sam_id == SamTag.sam_id)
        for sam in sams:
            if not sam.file_name in req_filenames:
                SamTag.query.filter(
                    and_(SamTag.tag_id == tag_id,
                         SamTag.sam_id == sam.sam_id)).delete()

        for filename in req_filenames:
            sam = Sam.query.filter(Sam.file_name == filename).first()
            add_tag_with_sam(tag.name, sam)
        update_tag_date(tag_id)
    except KeyError:
        pass

    try:
        req_filenames = request.form.getlist('bed')
        beds = Bed.query.join(BedTag, BedTag.tag_id == tag_id) \
                        .filter(Bed.bed_id == BedTag.bed_id)
        for bed in beds:
            if not bed.file_name in req_filenames:
                BedTag.query.filter(
                    and_(BedTag.tag_id == tag_id,
                         BedTag.bed_id == bed.bed_id)).delete()

        for filename in req_filenames:
            bed = Bed.query.filter(Bed.file_name == filename).first()
            add_tag_with_bed(tag.name, bed)
        update_tag_date(tag_id)
    except KeyError:
        pass

    return redirect('/manager')


@app.route('/api/tag/update-by-file', methods=['POST'])
def tag_update_by_file():
    filetype = request.form['type']
    fileid = request.form['id']
    tagids = [int(tag_id) for tag_id in request.form.getlist('tags')]
    if not filetype or not fileid or not tagids:
        return redirect('/')

    tags = []
    if filetype == 'sam':
        sam = Sam.query.get(fileid)
        tags = Tag.query.join(SamTag, SamTag.sam_id == sam.sam_id) \
                        .filter(Tag.tag_id == SamTag.tag_id).all()
        for tag in tags:
            if not tag.tag_id in tagids:
                SamTag.query.filter(
                    and_(SamTag.tag_id == tag.tag_id,
                         SamTag.sam_id == sam.sam_id)).delete()
                update_tag_date(tag.tag_id)
        for tag_id in tagids:
            tag = Tag.query.get(tag_id)
            try:
                add_tag_with_sam(tag.name, sam)
                update_tag_date(tag_id)
            except IntegrityError:
                pass
    elif filetype == 'bed':
        bed = Bed.query.get(fileid)
        tags = Tag.query.join(BedTag, BedTag.bed_id == bed.bed_id) \
                        .filter(Tag.tag_id == BedTag.tag_id).all()
        for tag in tags:
            if not tag.tag_id in tagids:
                BedTag.query.filter(
                    and_(BedTag.tag_id == tag.tag_id,
                         BedTag.bed_id == bed.bed_id)).delete()
                update_tag_date(tag.tag_id)
        for tag_id in tagids:
            tag = Tag.query.get(tag_id)
            try:
                add_tag_with_bed(tag.name, bed)
                update_tag_date(tag_id)
            except IntegrityError:
                pass

    return redirect('/')


@app.route('/api/tag/remove', methods=['POST'])
def tag_remove():
    tag_id = request.form['tag-id']
    if not tag_id:
        return redirect('/manager')

    SamTag.query.filter_by(tag_id=tag_id).delete()
    BedTag.query.filter_by(tag_id=tag_id).delete()
    Tag.query.filter_by(tag_id=tag_id).delete()

    return redirect('/manager')

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
from urlparse import urljoin

from flask import render_template, request

from ngsvconsole import app, conf, tasks_info, ws_viewer_sockets
from ngsvconsole.models import Sam, Bed, Cytoband, Chromosome
from ngsvconsole.models import Tag, SamTag, BedTag
import ngsvconsole.util as util


@app.route('/')
def root():
    samfiles = []
    for sam in Sam.query.all():
        samfile = {
            'type': 'sam',
            'filename': sam.file_name,
            'id': sam.sam_id,
            'created_date': sam.created_date,
            'url': urljoin(conf.upload_dir_url, sam.file_name),
            'size': util.get_pretty_size(urljoin(conf.upload_dir,
                                                 sam.file_name))}
        samfile['tags'] = Tag.query.join(SamTag, SamTag.sam_id == sam.sam_id) \
                                   .filter(Tag.tag_id == SamTag.tag_id).all()
        samfiles.append(samfile)

    bedfiles = []
    for bed in Bed.query.all():
        bedfile = {
            'type': 'bed',
            'filename': bed.file_name,
            'id': bed.bed_id,
            'created_date': bed.created_date,
            'url': urljoin(conf.upload_dir_url, sam.file_name),
            'size': util.get_pretty_size(urljoin(conf.upload_dir,
                                                 bed.file_name))}
        bedfile['tags'] = Tag.query.join(BedTag, BedTag.bed_id == bed.bed_id) \
                                   .filter(Tag.tag_id == BedTag.tag_id).all()
        bedfiles.append(bedfile)

    files = samfiles + bedfiles
    files.sort(key=lambda x: x['created_date'], reverse=True)
    for f in files:
        dt = datetime.datetime.fromtimestamp(f['created_date'])
        f['created_date'] = dt.strftime('%Y/%m/%d %H:%M')

    return render_template('main.html', files=files, tags=Tag.query.all())


@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    query = q
    return render_template('search.html', query=query)


@app.route('/nav')
def nav():
    return render_template('nav.html')


@app.route('/upload')
def upload():
    tasks = []

    for ti in reversed(tasks_info):
        r = ti['result']

        if r.task_name == 'tasks.load_sam':
            task = {
                'task_id': r.id,
                'task_name': r.task_name,
                'sam_load_progress': 0}

            if 'file' in ti and ti['file'] is not None:
                task['sam_file'] = ti['file']

            if r.status == 'PROGRESS':
                task['sam_load_progress'] = str(r.result['progress']) + '%'
            if r.status == 'SUCCESS':
                task['sam_load_progress'] = '100%'
                if r.result['state'] == 'SUCCESS_WITH_ALERT':
                    task['alert'] = r.result['alert']
            if r.status == 'FAILURE':
                task['sam_load_progress'] = '100%'
                task['alert'] = 'FAILURE'

            tasks.append(task)

        if r.task_name == 'tasks.load_bed':
            task = {
                'task_id': r.id,
                'task_name': r.task_name,
                'bed_load_progress': 0}

            if 'file' in ti and ti['file'] is not None:
                task['bed_file'] = ti['file']

            if r.status == 'PROGRESS':
                task['bed_load_progress'] = str(r.result['progress']) + '%'
            if r.status == 'SUCCESS':
                task['bed_load_progress'] = '100%'
                if r.result['state'] == 'SUCCESS_WITH_ALERT':
                    task['alert'] = r.result['alert']
            if r.status == 'FAILURE':
                task['bed_load_progress'] = '100%'
                task['alert'] = 'FAILURE'

            tasks.append(task)

    return render_template('upload.html', tasks=tasks)


@app.route('/viewer')
def viewer():
    chrs = []
    cytobands = Cytoband.query.group_by(Cytoband.chr_id)
    chr_ids = [c.chr_id for c in cytobands]
    for chr_id in chr_ids:
        end = Cytoband.query.filter(Cytoband.chr_id == chr_id) \
                            .order_by(Cytoband.chr_end.desc()).first()
        chr = Chromosome.query.get(chr_id)
        chrs.append({'name': chr.chromosome, 'end': end.chr_end})

    return render_template('viewer.html',
                           sams=Sam.query.all(),
                           beds=Bed.query.all(),
                           chrs=chrs,
                           hostname=conf.host,
                           viewer_enable=viewer_enable(request.remote_addr))


@app.route('/download')
def download():
    samfiles = []
    bedfiles = []

    for sam in Sam.query.all():
        f = {}
        f['name'] = sam.file_name
        f['url'] = urljoin(conf.upload_dir_url, sam.file_name)
        samfiles.append(f)

    for bed in Bed.query.all():
        f = {}
        f['name'] = bed.file_name
        f['url'] = urljoin(conf.upload_dir_url, bed.file_name)
        bedfiles.append(f)

    return render_template('download.html',
                           samfiles=samfiles,
                           bedfiles=bedfiles)


@app.route('/manager')
def manager():
    tagdata = []

    for tag in Tag.query.all():
        td = {'tag': tag}
        td['sams'] = Sam.query.join(SamTag, SamTag.tag_id == tag.tag_id) \
                              .filter(Sam.sam_id == SamTag.sam_id).all()
        td['beds'] = Bed.query.join(BedTag, BedTag.tag_id == tag.tag_id) \
                              .filter(Bed.bed_id == BedTag.bed_id).all()
        tagdata.append(td)

    return render_template('manager.html',
                           sams=Sam.query.all(),
                           beds=Bed.query.all(),
                           tags=tagdata)


@app.route('/help')
def help():
    return render_template('help.html')


def viewer_enable(ip):
    return ip in ws_viewer_sockets

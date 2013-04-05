#!/usr/bin/env python
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

import datetime
import os
import os.path
import sys
from urlparse import urljoin

from flask import Flask
from flask import render_template, redirect, request, url_for
from werkzeug import SharedDataMiddleware
from werkzeug import secure_filename
from gevent import pywsgi
from geventwebsocket import WebSocketHandler, WebSocketError
from celery.result import BaseAsyncResult
from celery.task.control import inspect
from sqlalchemy import create_engine

from db.sam import SamDao
from db.bed import BedDao
from db.chromosome import ChromosomeDao
from db.cytoband import CytobandDao
from db.tag import TagDao
from taskserver.tasks import load_sam, load_bed
from config import Config
import util

app = Flask(__name__)

try:
    ini = os.environ['NGSV_CONSOLE_CONFIG']
except KeyError:
    ini = os.path.join(os.path.dirname(__file__), '../config/ngsv.ini')

if not os.path.isfile(ini):
    sys.exit('Not found "ngsv.ini"')

conf = Config(ini)

app.debug = conf.debug
app.testing = conf.testing

app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {'/': os.path.join(os.path.dirname(__file__), 'static')})

tasks_info = []
ws_viewer_sockets = {}


def list_active_task():
    i = inspect()
    active = i.active()
    if active is not None:
        for v in active.values():
            for t in v:
                r = BaseAsyncResult(t['id'])
                r.task_name = t['name']
                tasks_info.append({'result': r})

list_active_task()

db_url = 'mysql://%s:%s@%s/%s?charset=utf8' % (conf.db_user,
                                               conf.db_password,
                                               conf.db_host,
                                               conf.db_name)
engine = create_engine(db_url, encoding='utf-8',
                       convert_unicode=True, pool_recycle=3600)


@app.route('/')
def root():
    tag_dao = TagDao(engine)
    sam_dao = SamDao(engine)
    samfiles = []
    for sam in sam_dao.all():
        samfiles.append({
            'type': 'sam',
            'filename': sam.file_name,
            'id': sam.sam_id,
            'created_date': sam.created_date,
            'tags': tag_dao.get_by_samid(sam.sam_id),
            'url': urljoin(conf.upload_dir_url, sam.file_name),
            'size': util.get_pretty_size(urljoin(conf.upload_dir,
                                                 sam.file_name))})
    bed_dao = BedDao(engine)
    bedfiles = []
    for bed in bed_dao.all():
        bedfiles.append({
            'type': 'bed',
            'filename': bed.file_name,
            'id': bed.bed_id,
            'created_date': bed.created_date,
            'tags': tag_dao.get_by_bedid(bed.bed_id),
            'url': urljoin(conf.upload_dir_url, sam.file_name),
            'size': util.get_pretty_size(urljoin(conf.upload_dir,
                                                 bed.file_name))})

    files = samfiles + bedfiles
    files.sort(key=lambda x: x['created_date'], reverse=True)
    for f in files:
        dt = datetime.datetime.fromtimestamp(f['created_date'])
        f['created_date'] = dt.strftime('%Y/%m/%d %H:%M')

    tags = [{'id': tag.tag_id,
             'name': tag.name} for tag in tag_dao.all()]

    return render_template('main.html', files=files, tags=tags)


@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')

    sam_dao = SamDao(engine)


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
    sam_dao = SamDao(engine)
    bed_dao = BedDao(engine)
    cytoband_dao = CytobandDao(engine)
    chromosome_dao = ChromosomeDao(engine)

    chrs = []
    for chr_id in cytoband_dao.all_chr_id():
        end = cytoband_dao.get_end_by_chr_id(chr_id)
        chr = chromosome_dao.get_by_id(chr_id)
        chrs.append({'name': chr.chromosome, 'end': end.chr_end})

    return render_template('viewer.html',
                           sams=sam_dao.all(),
                           beds=bed_dao.all(),
                           chrs=chrs,
                           hostname=conf.host,
                           viewer_enable=viewer_enable(request.remote_addr))


@app.route('/download')
def download():
    sam_dao = SamDao(engine)
    bed_dao = BedDao(engine)

    samfiles = []
    bedfiles = []

    for sam in sam_dao.all():
        f = {}
        f['name'] = sam.file_name
        f['url'] = urljoin(conf.upload_dir_url, sam.file_name)
        samfiles.append(f)

    for bed in bed_dao.all():
        f = {}
        f['name'] = bed.file_name
        f['url'] = urljoin(conf.upload_dir_url, bed.file_name)
        bedfiles.append(f)

    return render_template('download.html',
                           samfiles=samfiles,
                           bedfiles=bedfiles)


@app.route('/manager')
def manager():
    sam_dao = SamDao(engine)
    bed_dao = BedDao(engine)
    tag_dao = TagDao(engine)

    tags = []

    for tag in tag_dao.all():
        tags.append({'tag': tag,
                     'sams': sam_dao.get_by_tag(tag),
                     'beds': bed_dao.get_by_tag(tag)})

    return render_template('manager.html',
                           sams=sam_dao.all(), beds=bed_dao.all(),
                           tags=tags)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.form['query']
    return redirect(url_for('search', q=query))


@app.route('/api/upload-sam', methods=['POST'])
def upload_bam():
    f = request.files['file']
    if f and allowed_file(f.filename, ['sam', 'bam']):
        filename = secure_filename(f.filename)
        sam_file = os.path.join(conf.upload_dir, filename)
        f.save(sam_file)

        r = load_sam.delay(sam_file,
                           conf.db_name,
                           conf.db_host,
                           conf.db_user,
                           conf.db_password)
        tasks_info.append({'result': r, 'file': filename})

    return redirect('/upload')


@app.route('/api/upload-bed', methods=['POST'])
def upload_bed():
    f = request.files['file']
    if f and allowed_file(f.filename, ['bed']):
        filename = secure_filename(f.filename)
        bed_file = os.path.join(conf.upload_dir, filename)
        f.save(bed_file)

        r = load_bed.delay(bed_file,
                           conf.db_name,
                           conf.db_host,
                           conf.db_user,
                           conf.db_password)
        tasks_info.append({'result': r, 'file': filename})

    return redirect('/upload')


@app.route('/api/tag/new', methods=['POST'])
def tag_new():
    tag_name = request.form['tag-name']
    if not tag_name:
        return redirect('/manager')

    tag_dao = TagDao(engine)

    try:
        sam_filenames = request.form.getlist('sam')
        sam_dao = SamDao(engine)
        for sam_filename in sam_filenames:
            sam = sam_dao.get_by_filename(sam_filename)
            tag_dao.add_tag_with_sam(tag_name, sam)
    except KeyError:
        pass

    try:
        bed_filenames = request.form.getlist('bed')
        bed_dao = BedDao(engine)
        for bed_filename in bed_filenames:
            bed = bed_dao.get_by_filename(bed_filename)
            tag_dao.add_tag_with_bed(tag_name, bed)
    except KeyError:
        pass

    return redirect('/manager')


@app.route('/api/tag/update', methods=['POST'])
def tag_update():
    tag_id = request.form['tag-id']
    if not tag_id:
        return redirect('/manager')

    tag_dao = TagDao(engine)
    tag = tag_dao.get_by_id(tag_id)

    try:
        req_filenames = request.form.getlist('sam')
        sam_dao = SamDao(engine)
        for sam in sam_dao.get_by_tag_id(tag_id):
            if not sam.file_name in req_filenames:
                tag_dao.remove_sam(sam, tag)
        for filename in req_filenames:
            sam = sam_dao.get_by_filename(filename)
            tag_dao.add_tag_with_sam(tag.name, sam)
        tag_dao.update_tag_date(tag_id)
    except KeyError:
        pass

    try:
        req_filenames = request.form.getlist('bed')
        bed_dao = BedDao(engine)
        for bed in bed_dao.get_by_tag_id(tag_id):
            if not bed.file_name in req_filenames:
                tag_dao.remove_bed(bed, tag)
        for filename in req_filenames:
            bed = bed_dao.get_by_filename(filename)
            tag_dao.add_tag_with_bed(tag.name, bed)
        tag_dao.update_tag_date(tag_id)
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

    tag_dao = TagDao(engine)
    tags = []
    if filetype == 'sam':
        sam_dao = SamDao(engine)
        sam = sam_dao.get_by_id(fileid)
        tags = tag_dao.get_by_samid(sam.sam_id)
        for tag in tags:
            if not tag['id'] in tagids:
                tag_dao.remove_sam_by_tag_id(sam, tag['id'])
                tag_dao.update_tag_date(tag['id'])
        for tag_id in tagids:
            tag = tag_dao.get_by_id(tag_id)
            tag_dao.add_tag_with_sam(tag.name, sam)
            tag_dao.update_tag_date(tag_id)
    elif filetype == 'bed':
        bed_dao = BedDao(engine)
        bed = bed_dao.get_by_id(fileid)
        tags = tag_dao.get_by_bedid(bed.bed_id)
        for tag in tags:
            if not tag['id'] in tagids:
                tag_dao.remove_bed_by_tag_id(bed, tag['id'])
                tag_dao.update_tag_date(tag['id'])
        for tag_id in tagids:
            tag = tag_dao.get_by_id(tag_id)
            tag_dao.add_tag_with_bed(tag.name, bed)
            tag_dao.update_tag_date(tag_id)

    return redirect('/')


@app.route('/api/tag/remove', methods=['POST'])
def tag_remove():
    tag_id = request.form['tag-id']
    if not tag_id:
        return redirect('/manager')
    print 'remove tag'
    tag_dao = TagDao(engine)
    tag_dao.remove_by_id(tag_id)

    return redirect('/manager')


@app.route('/api/ws/connect')
def ws_connect():
    if request.environ.get('wsgi.websocket') is None:
        return redirect('/viewer')

    ip = request.remote_addr
    ws = request.environ['wsgi.websocket']
    ws_viewer_sockets[ip] = ws
    print 'Register: ', request.remote_addr

    while True:
        src = ws.receive()
        if src is None:
            break

    return redirect('/viewer')


@app.route('/api/ws/send-config')
def ws_send_config():
    if request.environ.get('wsgi.websocket') is None:
        return redirect('/viewer')

    ip = request.remote_addr
    ws = request.environ['wsgi.websocket']

    while True:
        src = ws.receive()
#        print src
        if src is None:
            break
        if ip in ws_viewer_sockets:
            try:
                ws_viewer_sockets[ip].send(src)
            except WebSocketError:
                del ws_viewer_sockets[ip]

    return redirect('/viewer')


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions


def viewer_enable(ip):
    return ip in ws_viewer_sockets


def run():
    if len(sys.argv) == 2 and sys.argv[1] == '--wsgi':
        print '''\
Debug: Disable
Testing: Disable
Websocket: Enable

Run "$ python app.py" if you want to use Debug/Testing mode
'''
        server = pywsgi.WSGIServer(('', 5000),
                                   app,
                                   handler_class=WebSocketHandler)
        server.serve_forever()
    else:
        print '''\
Debug: Enable
Testing: Enable
Websocket: Disable

Run "$ python app.py --wsgi" if you want to use websocket
'''
        app.run(host='0.0.0.0')

if __name__ == '__main__':
    run()

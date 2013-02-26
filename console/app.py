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

import os
import sys
from urlparse import urljoin

from flask import Flask
from flask import render_template, redirect, request
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
    return render_template('main.html')


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
                           hostname=conf.host)


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


@app.route('/api/newtag', methods=['POST'])
def newtag():
    tag_name = request.form['tag-name']
    if not tag_name:
        return redirect('/manager')

    tag_dao = TagDao(engine)

    try:
        sam_filename = request.form['sam']
        print sam_filename
        if sam_filename:
            sam_dao = SamDao(engine)
            sam = sam_dao.get_by_filename(sam_filename)
            tag_dao.add_tag_with_sam(tag_name, sam)
    except KeyError:
        pass

    try:
        bed_filename = request.form['bed']
        if bed_filename:
            bed_dao = BedDao(engine)
            bed = bed_dao.get_by_filename(bed_filename)
            tag_dao.add_tag_with_bed(tag_name, bed)
    except KeyError:
        pass

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
        print src
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

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

import os

from flask import redirect, request
from werkzeug import secure_filename

from ngsvconsole.app import app, conf, tasks_info
from ngsvconsole.taskserver.tasks import load_sam, load_bed, load_cnv


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


@app.route('/api/upload-cnv', methods=['POST'])
def upload_cnv():
    f = request.files['file']
    if f and allowed_file(f.filename, ['rawcnv', 'cnv']):
        filename = secure_filename(f.filename)
        cnv_file = os.path.join(conf.upload_dir, filename)
        f.save(cnv_file)

        r = load_cnv.delay(cnv_file,
                           conf.db_name,
                           conf.db_host,
                           conf.db_user,
                           conf.db_password)
        tasks_info.append({'result': r, 'file': filename})

    return redirect('/upload')


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions

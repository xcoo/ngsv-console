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

from celery import current_task

import ngsvtools.action
import ngsvtools.samloader
import ngsvtools.histogramloader
import ngsvtools.bedloader
import ngsvtools.cnvloader
from ngsvtools.sam.data.sql import SQLDB
from ngsvtools.exception import UnsupportedFileError, AlreadyLoadedError

from ngsvconsole.taskserver.celery import celery


class HistogramLoaderAction(ngsvtools.action.HistogramLoaderAction):

    def __call__(self, progress):
        current_task.update_state(state='PROGRESS',
                                  meta={'progress': 50 + progress / 2})


# Load a sam file and calculate histograms.
@celery.task(name='tasks.load_sam')
def load_sam(sam_file, db_name, db_host, db_user, db_password):
    current_task.update_state(state='STARTED')
    db = SQLDB(db_name, db_host, db_user, db_password)

    sam_already_loaded = False
    alert = ''

    try:
        ngsvtools.samloader.load(sam_file, db)
    except UnsupportedFileError, e:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': e.msg}
    except AlreadyLoadedError, e:
        sam_already_loaded = True
        alert = e.msg

    current_task.update_state(state='PROGRESS', meta={'progress': 50})

    ngsvtools.histogramloader.load(sam_file, db, action=HistogramLoaderAction)

    if sam_already_loaded:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': alert}

    return {'state': 'SUCCESS'}


class BedLoaderAction(ngsvtools.action.BedLoaderAction):

    def __call__(self, progress):
        current_task.update_state(state='PROGRESS',
                                  meta={'progress': progress})


# Load a bed file.
@celery.task(name='tasks.load_bed')
def load_bed(bed_file, db_name, db_host, db_user, db_password):
    current_task.update_state(state='STARTED')
    db = SQLDB(db_name, db_host, db_user, db_password)

    try:
        ngsvtools.bedloader.load(bed_file, db, action=BedLoaderAction)
    except UnsupportedFileError, e:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': e.msg}
    except AlreadyLoadedError, e:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': e.msg}

    return {'state': 'SUCCESS'}


# Load a cnv file.
@celery.task(name='tasks.load_cnv')
def load_cnv(cnv_file, db_name, db_host, db_user, db_password):
    current_task.update_state(state='STARTED')
    db = SQLDB(db_name, db_host, db_user, db_password)

    try:
        ngsvtools.cnvloader.load(cnv_file, db)
    except UnsupportedFileError, e:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': e.msg}
    except AlreadyLoadedError, e:
        return {'state': 'SUCCESS_WITH_ALERT', 'alert': e.msg}

    return {'state': 'SUCCESS'}

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

from setuptools import setup
from distutils.extension import Extension

# Require for setuptools_cython
import sys
if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__

setup(
    name='ngsv-tools',
    version='0.1.0',
    description='Tools for NGSV database',
    license='Apache License 2.0',
    author='Xcoo, Inc.',
    author_email='developer@xcoo.jp',
    url='http://github.com/xcoo/ngsv-console',
    setup_requires=['setuptools_cython'],
    install_requires=['pysam>=0.7', 'MySQL-python', 'celery'],
    ext_modules=[Extension('ngsvtools.cypileup', ['ngsvtools/cypileup.pyx'])],
    scripts=['scripts/ngsv'],
    packages=['ngsvtools', 'ngsvtools.sam', 'ngsvtools.sam.data'],
    package_data={'ngsvtools': ['data/ngsv.sql']})

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

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name='ngsv-tools',
    version='0.1.0',
    description='Tools for NGSV database',
    license='Apache License 2.0',
    author='Xcoo, Inc.',
    author_email='developer@xcoo.jp',
    url='http://github.com/xcoo/ngsv-console',
    requires=['pysam (>=0.7)'],
    ext_modules=[Extension('ngsvtools.cypileup', ['ngsvtools/cypileup.pyx'])],
    cmdclass={'build_ext': build_ext},
    scripts=['scripts/ngsv'],
    packages=['ngsvtools', 'ngsvtools.sam', 'ngsvtools.sam.data'])

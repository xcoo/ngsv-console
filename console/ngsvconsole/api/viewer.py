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

from geventwebsocket import WebSocketError
from flask import redirect, request

from ngsvconsole import app, ws_viewer_sockets


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

        if src is None:
            break
        if ip in ws_viewer_sockets:
            try:
                ws_viewer_sockets[ip].send(src)
            except WebSocketError:
                del ws_viewer_sockets[ip]

    return redirect('/viewer')

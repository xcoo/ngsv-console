# -*- coding: utf-8 -*-

import os
import sys
from gevent import pywsgi
from geventwebsocket import WebSocketHandler


def run():
    os.environ['NGSV_CONSOLE_CONFIG'] = os.path.join(os.path.dirname(__file__),
                                                     'config/ngsv.ini')

    from app import app

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

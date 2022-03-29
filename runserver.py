import asyncio
import tornado.autoreload
import os
import json

from application.settings import SettingsApplication
from tornado.escape import utf8
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options

from utils.util import ObjAwareEncoder

define('port', default=8888)
define('num_chunks', default=40)

async def client():
    async def body_producer(write):
        for i in range(options.num_chunks):
            chunk = ('chunk %02d ' % i) * 10000
            await write(utf8(chunk))

    response = await AsyncHTTPClient().fetch(
        'http://localhost:%d/proxy' % options.port,
        method='PUT',
        body_producer=body_producer)


def runserver():
    parse_command_line()
    app = SettingsApplication()
    http_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": os.path.join('C:/Users/hminhtuan/Downloads','tornado_ssl.crt'),
        "keyfile": os.path.join('C:/Users/hminhtuan/Downloads','tornado_ssl.key'),
    })
    http_server.listen(options.port)
    tornado.autoreload.start()
    IOLoop.instance().start()

if __name__ == '__main__':
    json._default_encoder = ObjAwareEncoder()  # Use custom encoder
    runserver()

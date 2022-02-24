import asyncio
from test_application import TestApplication
from tornado.escape import utf8
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options

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


def main():
    parse_command_line()
    app = TestApplication()
    app.listen(options.port)
    # IOLoop.instance().add_callback(client)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()

import asyncio
from handlers.base import BaseHandler
import HrpListener
import json
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.web import stream_request_body
from tornado.websocket import WebSocketHandler

class TestGetAPIHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie('collabos_user')

    def get(self, uid):
        self.set_secure_cookie('collabos_user', 'test-user-%s' % uid)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({ 'user_id': uid }))


class TestPostAPIHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie('collabos_user')

    def post(self):
        uid = self.get_body_argument('uid')
        self.set_secure_cookie('collabos_user', 'test-user-%s' % uid)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({ 'user_id': uid }))


@stream_request_body
class UploadHandler(BaseHandler):
    def prepare(self):
        self._chunk = []

    async def data_received(self, chunk):
        await self._on_data_received(chunk)

    async def _on_data_received(self, chunk):
        await gen.sleep(0.01)
        self._chunk.append(chunk)

    def put(self):
        self.set_header('Content-Type', 'application/json')
        self.write('{ "data": "%s" }' % ''.join(self._chunk))


@stream_request_body
class ProxyHandler(BaseHandler):
    def prepare(self):
        self._chunks = Queue()

    async def _body_producer(self, write):
        while True:
            chunk = await self._chunks.get()
            if chunk is None:
                return
            await write(chunk)

    async def data_received(self, chunk):
        await self._chunks.put(chunk)

    async def put(self):
        self._chunks.put(None)
        response = await self._async_request(
            url=self.reverse_url('upload'),
            method='PUT',
            body_producer=self._body_producer,
        )
        self.set_status(response.code)
        self.write(response.body)


class AmiWSHandler(WebSocketHandler, HrpListener.HrpListener):
    def check_origin(self, origin):
        print('Will allow origin %s' % origin)
        return True

    def open(self):
        self.hrp = self.application.hrp
        if not self.hrp:
            self.close(code=504, reason='can not initialise HRP connection')
            return
        self.hrp.setListener(self)
        self.write_message({
            'status': 'hs',
            'detail': 'hrp connection established'
        })

    async def on_message(self, message):
        msg_json = json.loads(message)
        data_chunk = msg_json['data'] if 'data' in msg_json else None
        if not data_chunk:
            self.write_message({
                'status': 'rejected',
                'detail': 'no chunk data in msg, wrong spec'
            })
            return
        data_chunk = bytearray(data_chunk)
        await IOLoop.current().run_in_executor(None,
                                               self.hrp.feedData,
                                               data_chunk, 0,
                                               len(data_chunk))

    def _extract_text(self, result):
        try:
            return json.loads(result)['text']
        except:
            return None

    def resultUpdated(self, result):
        text = self._extract_text(result)
        if text:
            self.write_message({
                'status': 'response',
                'finish': False,
                'text': text
            })

    def resultFinalized(self, result):
        text = self._extract_text(result)
        if text:
            self.write_message({
                'status': 'response',
                'finish': True,
                'text': text
            })

    def resultCreated(self, sessionId):
        self.write_message({
            'status': 'response',
            'finish': True,
            'text': sessionId
        })


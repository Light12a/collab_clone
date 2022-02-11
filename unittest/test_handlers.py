import asyncio, hashlib, datetime, uuid, query_sql, constant_value
from handlers.base_handlers import BaseHandler
import HrpListener
import json
import logging
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.web import stream_request_body
from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient
from tornado.websocket import WebSocketHandler

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.DEBUG,
    filename="debug.log")

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

class LogoutHandler(BaseHandler): 
    def post(self):
        request = json.loads(bytes.decode(self.request.body))
        check, params = self._check_token_exists(request['username'], request['tenant_id'])
        
        if check and params[0] == request['token']:
            self._clear_token(request['token'])
            self.write({
                "code":200
                })
            self.set_status(200)
        else:
            self.write({
                "code":401, 
                "message":"Token is wrong"
                })
            self.set_status(401)
            err = "Token of user: {} is wrong"
            logging.debug(err.format(request['username']))

    def _clear_token(self, token):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.CLEAR_TOKEN.format(token))
        self.application.conn.commit()
        sql.close()

    def _check_token_exists(self,username, tenant_id):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.CHECK_TOKEN_EXISTS_BEFORE_CLEAR.format(username, tenant_id))
        result = sql.fetchone()

        if result is None:
            return False, result
        else:
            return True, result

class GetUserHandler(BaseHandler):
    def post(self):
        request = json.loads(bytes.decode(self.request.body))
        inf = "token: {}, search: {}, from: {}, to: {}"
        logging.info(request['token'], request['search'], request['from'], request['to'])
        #check token valid and then select user
        #block get state 
        if self._find_token(request):
            user = self._get_user(request)
            if user:
                self.write({
                    "user": user
                })
                inf = "return some users info search by keyword: {} from:{} to:{}"
                logging.info(inf.format(request['search'], request['from'], request['to']))
            else:
                self.write({"code":405, "message":"Search keyword not found"})
                            
    def _find_token(self, request):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.FIND_TOKEN.format(request['token']))
        result = sql.fetchone()
        if result:
            inf = "token existed"
            logging.info(inf)
            if self._check_valid_token(result[1].strftime("%Y-%m-%d %H:%M:%S"), result[0]):
                inf = "Token is in of date"
                logging.info(inf)
                return True
            else:
                err = "Token is out of date"
                logging.error(err)
                self.write({
                        "code": 402,
                        "message": "Token is expiried"
                        })
        else:
            err = "Token not existed"
            self.write({"code":401, "message":"token is wrong"})
            return False
            
    def _get_user(self, request):
        sql = self.application.conn.cursor()
        if request['to'] == -1:
            sql.execute(query_sql.GET_USER.format(request['search'], request['search'],request['from'], 10000000))
            results = sql.fetchall()
        else:
            sql.execute(query_sql.GET_USER.format(request['search'], request['search'],request['from'], request['to']))
            results = sql.fetchall()
        sql.close()
        if results:
            user =[{
                "user_id": result[0],
                "username": result[1],
                "state":100,
                "ext_number": result[2]
                } for result in results]
        else:
            err = "Not found search keyword: {}"
            logging.error(err.format(request['search']))
            return False
        return user

    
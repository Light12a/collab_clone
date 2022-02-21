import asyncio
from handlers.base_handlers import BaseHandler
import HrpListener
import json
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.web import stream_request_body
from tornado.websocket import WebSocketHandler
import logging
import query_sql
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


class UserConfigHandler(BaseHandler):
    def post(self):
        request = json.loads(bytes.decode(self.request.body))
        check, params = self._check_token_exists(request['username'], request['tenant_id'])
        if check and params[0] == request['token_id']:
            if self._check_valid_token(params[2].strftime("%Y-%m-%d %H:%M:%S"), params[1]):
                params = self._get_user_config(request)
                self.write({
                    "code":200,
                    "user_id": params[0],
                    "username":params[1],
                    "ext_number": params[5],
                    "tenant":params[2],
                    "role": 1,
                    "state": "offline",
                    "domain": "https://13.113.23.145:8088/",
                    "domain_ws": "wss://13.113.23.145:8088/ws",
                    "pbx_domain": "http://18.180.191.58:8888/",
                    "pbx_ws": "wss://18.180.191.58:8888/ws"
                })
                logging.info({
                    "code":200,
                    "user_id": params[0],
                    "username":params[1],
                    "ext_number": params[5],
                    "tenant":params[2],
                    "role": 1,
                    "state": "offline",
                    "domain":"http://18.180.191.58:8888/",
                    "domain_ws": "wss://18.180.191.58:8888/ws",
                    "pbx_domain": "https://13.113.23.145:8088/",
                    "pbx_ws": "wss://13.113.23.145:8088/ws"
                })
            else:
                self.write("Token is wrong")
        else:
                self.write("Token does not exist")

                
                
    def _get_user_config(self, request):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.GET_USER_CONFIG.format(request['username'], request['tenant_id']))
        result = sql.fetchone()
        sql.close()
        return result


    def _check_token_exists(self,username, tenant_id):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.CHECK_TOKEN_EXISTS_BEFORE_CLEAR.format(username, tenant_id))
        result = sql.fetchone()

        if result is None:
            return False, result
        else:
            return True, result

class ApplyStateHandler(BaseHandler):
    def post(self):
        try:
            request = json.loads(bytes.decode(self.request.body))
            if ("token" and "username" and "state" and "sub_state") in request:
                check, params = self._check_token_exists(request["token"])
                if check and params[0] == request["token"]:
                    print(request["token"])
                    if self._check_valid_token(params[3].strftime("%Y-%m-%d %H:%M:%S"), params[2]):
                        if self._check_username_correct(request["username"]):
                            if request["state"] not in [100, 101, 102, 103, 104]:
                                self.write({
                                    "code" : 407,
                                    "errorMessage" : "invalid state"
                                })
                            elif request["state"] == 103 and request["sub_state"] not in [1, 2, 3]: #fix list id
                                self.write({    
                                    "code" : 408,
                                    "errorMessage" : "invalid sub_state"
                                })
                            elif request["state"] in [100, 102, 104] and request["sub_state"] != 0:
                                self.write({    
                                    "code" : 408,
                                    "errorMessage" : "invalid sub_state"
                                })
                            else:
                                self._apply_state(request["state"], request["sub_state"], request["token"])
                                params = self._get_user_after_state(request["token"])
                                print("test None")
                                print(params[4])
                                self.write({
                                    "code": 200,
                                    "username": params[0], 
                                    "displayname": params[1],
                                    "groupId": params[2],
                                    "state": params[3],
                                    "sub_state": params[4],
                                })
                                logging.info({
                                    "code": 200,
                                    "username": params[0], 
                                    "displayname": params[1],
                                    "groupId": params[2],
                                    "state": params[3],
                                    "sub_state": params[4],
                                })
                        else:
                            self.write({"code": 402, "errorMessage": "username not found"})
                    else:
                        self.write({"code": 402, "errorMessage": "Token is expired"})
                else:
                    self.write({"code": 401, "errorMessage": "Token is wrong"})
            else:
                raise ValueError
        except ValueError:
            err = "Json request is not correct"
            logging.error(err)
            self.write({"code": 201, "errorMessage": "Bad request"})

    def _check_token_exists(self, token_id):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.CHECK_TOKEN_EXIST.format(token_id))
            result = sql.fetchone()

            if result is None:
                return False, result
            else:
                return True, result
    def _check_username_correct(self, username):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.CHECK_USERNAME_IS_NULL.format(username))
            result = sql.fetchone()

            if result is None:
                return False
            else:
                return True     
    def _apply_state(self, state, substate, token):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.APPLY_STATE.format(state, substate, token))
            result = sql.fetchone()
    
    def _get_user_after_state(self, token):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.GET_USER_AFTER_APPLY_STATE.format(token))
            result = sql.fetchone()
            return result
        #self.write({"code":201, "message": "Bad request", "detail": "resource not found"})
    
        #self.write({"code":201, "message": "Bad request", "detail": "resource not found"})


class GetUserStateHandler(BaseHandler):
    def post(self):
        try:
            request = json.loads(bytes.decode(self.request.body))
            if ("token" and "username") in request: 
                check, params = self._check_token_exists(request["token"])
                if check and params[0] == request["token"]:
                    if self._check_valid_token(params[3].strftime("%Y-%m-%d %H:%M:%S"), params[2]):
                        if self._check_username_correct(request["username"]):
                            print("test in")
                            print(request["token"])
                            params = self._get_user_state(request["token"])
                            print("test in")
                            print(params)
                            self.write({
                                "code" : 200,
                                "username": params[0], 
                                "displayname": params[1],
                                "groupId": params[2],
                                "state": params[3],
                                "sub_state": params[4],
                                "note": params[5],
                            })
                            logging.info({
                                "code" : 200,
                                "username": params[0], 
                                "displayname": params[1],
                                "groupId": params[2],
                                "state": params[3],
                                "sub_state": params[4],
                                "note": params[5],                                
                            })
                        else:
                            self.write({"code": 402, "errorMessage": "username not found"})
                    else:
                        self.write({"code": 402, "errorMessage": "Token is expired"})
                else:
                    self.write({"code": 401, "errorMessage": "Token is wrong"})
            else:
                raise ValueError
        except ValueError:
            err = "Json request is not correct"
            logging.error(err)
            self.write({"code": 201, "errorMessage": "Bad request"})

    def _check_token_exists(self, token_id):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.CHECK_TOKEN_EXIST.format(token_id))
            result = sql.fetchone()
            if result is None:
                return False, result
            else:
                return True, result


    def _get_user_state(self, token):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.GET_USER_AFTER_APPLY_STATE_WITHIN_CODE.format(token))
            result = sql.fetchone()
            return result

    def _check_username_correct(self, username):
            sql = self.application.conn.cursor()
            sql.execute(query_sql.CHECK_USERNAME_IS_NULL.format(username))
            result = sql.fetchone()

            if result is None:
                return False
            else:
                return True 


import asyncio, hashlib, datetime, uuid, query_sql, constant_value, MySQLdb
from handlers.base_handlers import BaseHandler
import HrpListener
import json
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.web import stream_request_body
from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient
from tornado.websocket import WebSocketHandler
import util_log

log = util_log.get(__name__)

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

class LoginHandler(BaseHandler):
    def post(self):
        request = json.loads(bytes.decode(self.request.body))
        
        check = self._check_format_json(request)
        if check: 
            self._check_token_valid(request)
        else:
            credential = self._user_credential_read(tenant_id=request['tenant_id'], username= request['username'])
            if not credential:
                self.write({
                    "code":403,
                    "message":"username or tenant_id is wrong"
                    })
                self.set_status(403)
                err = "{} or tenant_id: {} is wrong in json request for login at {}"
                log.debug(err.format(request['username'], request['tenant_id'], datetime.datetime.utcnow()))
            else:
                password_valid = self._validate_user_password(credential, password=request['password'])
                if not password_valid:
                    self.write({
                        "code":400, 
                        "message":"Password is wrong"
                        })
                    self.set_status(400)
                    err = "Password of user: {} is wrong"
                    log.debug(err.format(request['username']))
                else:
                    codes, token = self._create_token(credential)
                    self.write({
                        "code":codes, 
                        "token": token['token_id']
                        })
                    self.set_status(200)
                    inf = "Login of user: {} successfully"
                    log.info(inf.format(request['username']))

    def _user_credential_read(self, tenant_id, username): 
        sql = self.application.conn.cursor()
        sql.execute(query_sql.SELECT_USER.format(tenant_id, username))
        result = sql.fetchone()
        sql.close()
        
        if result is None:
            return False
        else:
            return result[0]
        
    def _validate_user_password(self, user_id, password):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.SELECT_PASSWORD.format(user_id))
        result = sql.fetchone() 
        sql.close()
        
        if result[0] == password:
            return True 
    
    def _remove_expired_token(self, user_id):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.REMOVE_EXPIRED_TOKEN.format(user_id))
        self.application.conn.commit()
        sql.close()

    def _create_token(self, user_id):
        params = dict(
            token_id = str(uuid.uuid4()),
            user_id = user_id,
            expiration_time = constant_value.ONE_WEEK_TOKEN_IN_SECONDS,
            create_time = str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        )
        
        sql = self.application.conn.cursor()
        self._remove_expired_token(user_id=user_id)
        sql.execute(query_sql.ACCESS_TOKEN_CREATE.format(
            params['token_id'],params['user_id'],
            params['expiration_time'],params['create_time']
            ))
        log.info({
            "token": params['token_id'],
            "user_id": params['user_id'],
            "expiration_time": params['expiration_time'],
            "create_time": params['create_time']
        })
        self.application.conn.commit()
        sql.close()

        return 200, params

    def _check_format_json(self, json):
        try:
            token = json['token']
            inf = "json request for relogin of user: {}"
            log.info(inf.format(json['username']))
        except KeyError:
            err = "json request for new login of {}"
            log.info(err.format(json['username']))
            return False
        return True

    def _check_token_valid(self, request):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.SELECT_TOKEN_TO_CHECK_SAME.format(request['tenant_id'], request['username']))
        result = sql.fetchone()
        try:
            if result[0] == request['token']:
                inf = "Find out token_id is the same with token_id of user: {} in json request"
                log.info(inf.format(request['username']))
                check = self._check_valid_token(result[2].strftime("%Y-%m-%d %H:%M:%S"), result[1])
                if check:
                    self.write({
                        "code":200
                        })
                    self.set_status(200)
                else:
                    self.write({
                        "code": 402,
                        "message": "Token is expiried"
                        })
                    self.set_status(402)
            else:
                self.write({
                    "code":405, 
                    "message": "Token is wrong"
                    })
                self.set_status(405)
        except TypeError:
            self.write({
                "code":406, 
                "message":"username or tenant_id is not existed"
                })
            self.set_status(406)
            err = "Username: {} or tenant_id: {} attached in json request is not existed in db"
            log.exception(err.format(request['username'], request['tenant_id']))
        

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
            log.debug(err.format(request['username']))

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
        try:
            request = json.loads(bytes.decode(self.request.body))
            if self._find_token(request):
                user = self._get_user(request)
                if user:
                    self.write({
                        "users": user
                    })
                    inf = "return some users info search by keyword: {} from:{} to:{}"
                    log.info(inf.format(request['search'], request['from'], request['to']))
                else:
                    self.write({"code":405, "message":"Search keyword not found"})
        except ValueError:
            err = "Json request is not correct"
            log.error(err)
            self.write({"code":201, "message":"Bad request"})
        
        #check token valid and then select user
        #block get state 
                    
    def _find_token(self, request):
        sql = self.application.conn.cursor()
        sql.execute(query_sql.FIND_TOKEN.format(request['token']))
        result = sql.fetchone()
        if result:
            inf = "token existed"
            log.info(inf)
            if self._check_valid_token(result[1].strftime("%Y-%m-%d %H:%M:%S"), result[0]):
                inf = "Token is in of date"
                log.info(inf)
                return True
            else:
                err = "Token is out of date"
                log.error(err)
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
            try:
                sql.execute(query_sql.GET_USER.format(request['search'], request['search'],request['from'], 10000000))
                results = sql.fetchall()
            except MySQLdb._exceptions.OperationalError and KeyError:
                self.write({"code":201, "message": "Bad request"})
        else:
            try:
                sql.execute(query_sql.GET_USER.format(request['search'], request['search'],request['from'], request['to']))
                results = sql.fetchall()
            except MySQLdb._exceptions.OperationalError and KeyError:
                self.write({"code":201, "message": "Bad request"})
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
            log.error(err.format(request['search']))
            return False
        return user

    
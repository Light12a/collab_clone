import datetime
import jwt
import json
import ssl
import re
import websockets
from ..base import BaseHandler
from .models import User, Token, Tenant
from handlers.groups.models import Group
from handlers.operation_logs.models import OperationLog
from http import HTTPStatus
from utils.config import config
from tornado import gen
from hashlib import md5
from tornado.websocket import WebSocketHandler
from services.logging import logger as log
from .token import JwtTokenTransfrom
from .decorators import token_required
from .schema import LOGIN_SCHEMA, LOGOUT_SCHEMA, \
    REFRESH_SCHEMA, PROFILE_SCHEMA, PASSWORD_CHANGE_SCHEMA

log = log.get(__name__)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


class LoginHandler(BaseHandler):
   """
      This class is created to build Login API.
      Params of request are domain, username and password.
      The other side, this API can use for re-login with request's format is token.
      User who logged in failure 3 times in row will be locked.
   """
   SCHEMA = LOGIN_SCHEMA

   @gen.coroutine
   def post(self):
      company_id = self.validated_data.get('company_id')
      username = self.validated_data.get('username')
      password = self.validated_data.get('password')
      token = self.validated_data.get('token')

      if token is None:
         credential = yield self._user_credential_read(company_id, username)
         yield self._check_lock(username)
         yield self._validate_user_password(credential, password, username)
      else:
         self._check_token_valid(token)

   @gen.coroutine
   def _user_credential_read(self, company_id, username):
      """
         This function use domain and username to find out user_id of user 
            who has just logged in.
         Params: domain, username
      """
      result = self.db.query(User.user_id).join(Tenant, User.tenant_id == Tenant.tenant_id).filter(
          Tenant.domain == company_id, User.user_name == username).distinct().all()

      try:
         raise gen.Return(result[0][0])
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Company_id: {} and Username: {} not found".
                    format(company_id, username)})
         raise gen.Return(self.write_response("0000",
                                              code=HTTPStatus.UNAUTHORIZED,
                                              message="Invalid Username or company_id"))

   @gen.coroutine
   def _validate_user_password(self, user_id, password, username):
      """
         Function take user_id to find out password and compare with 
            inputed password in order to verify password.
         @Params: user_id, password.
      """
      result = self.db.query(User).filter(User.user_id == user_id).all()

      try:
         user_pass = self.to_json(result[0])
         if user_pass['password'] == password:
            token = yield self._create_token(user_id)
            yield self._send_json(username, token['token_id'])
            log.info("Username: {} login successfully".format(username))
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.OK, response_data={
                    "token": token['token_id'],
                    "token_expired": token['expiration_time']
                }))
         else:
            self.db.query(User).filter(User.user_id == user_id).update(
                {User.login_ng_cnt: User.login_ng_cnt + 1},
                synchronize_session=False)
            yield self._check_cnt_to_lock(username)
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.UNAUTHORIZED,
                message="Invalid password"))
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Invalid Password of user: {}".format(user_id)})

   @gen.coroutine
   def _remove_expired_token(self, user_id):
      """
         Remove user's token if existed in database before provide new token.
         @Params: user_id.
      """
      self.db.query(Token).filter(Token.user_id == user_id).delete()
      self.db.commit()

   @gen.coroutine
   def _create_token(self, user_id):
      """
         Create new token and save it in database.
         @Params: user_id.
      """
      query = self.db.query(User).filter(User.user_id == user_id)
      id = self.to_json(query[0])
      token = JwtTokenTransfrom(user_id=user_id)._transform_token()
      params = dict(
          token_id=str(token),
          user_id=id['id'],
          expiration_time=int(int(datetime.datetime.strptime(str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) + int(config.getint('token', 'login_expiry')*1000)),
          create_time=str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
      )

      self._remove_expired_token(user_id=id['id'])
      self.db.query(User).filter(User.user_id == user_id).update(
          {User.login_ng_cnt: 0}, synchronize_session=False)
      new_token = Token(user_id=params['user_id'], token_id=params['token_id'],
                        expired_date=params['expiration_time'], create_date=params['create_time'])
      self.db.add(new_token)
      self.db.commit()
      raise gen.Return(params)

   @gen.coroutine
   def _send_json(self, username, token):
      ws = yield websockets.connect("wss://localhost:8888/collabos?token={}".format(token), ssl=ssl_context)
      yield ws.send(json.dumps({
          "api_name": "presense_state",
          "username": username,
          "state": 101,
          "substate": 0,
          "note": "",
          "only": 1
      }))

   def _check_token_valid(self, request):
      """
         Check token which user has just sent to server is newest.
         @Params: Token field in json request.
      """
      result = self.db.query(Token.user_id).filter(
          Token.token_id == request)

      try:
         if result[0][0]:
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.OK, response_data={"code": 200}))
      except IndexError:
         raise gen.Return(self.write_response(
             "0000", code=HTTPStatus.UNAUTHORIZED, message="Invalid Token"))

   @gen.coroutine
   def _check_cnt_to_lock(self, username):
      """
         Check number of login failure in row of user.
         @params: username.
      """
      cnt = self.db.query(User.login_ng_cnt).filter(
          User.user_id == username).all()

      if cnt[0][0] >= 3:
         self.db.query(User).filter(User.user_id == username).update(
             {
                 User.locked: 1,
                 User.locked_date: str(
                     datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
             }, synchronize_session=False)
         self.db.commit()
         raise gen.Return(True)

   @gen.coroutine
   def _check_lock(self, username):
      """
         Check user is locked to login or not.
         @params: username.
      """
      lock = self.db.query(User).filter(User.user_name == username).all()
      locked = self.to_json(lock[0])

      try:
         if locked['locked'] == 1:
            log.error("User: {} is locked".format(username))
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.UNAUTHORIZED, message="User locked"))
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Username: {} not found".format(username)})


class LogoutHandler(BaseHandler):
   """
      API is used for logging out of system.
      @params: Token
   """
   SCHEMA = LOGOUT_SCHEMA

   @gen.coroutine
   def post(self):
      """
         Check token which has just been sent to server is the newest and delete it.
      """
      token = self.validated_data.get('token')
      check = yield self._check_token_exists(token)

      if check:
         self._clear_token(token)
         log.info("User logged out successfully with token: {}".format(token))
         raise gen.Return(self.write_response(
             "0000", code=HTTPStatus.OK))
      else:
         raise gen.Return(self.write_response("0000",
                                              code=HTTPStatus.UNAUTHORIZED, message="Invalid Token"))

   @gen.coroutine
   def _check_token_exists(self, token):
      """
      Function take in token to verify this one is the newest.
      @params: Token.
      """
      result = self.db.query(Token.token_id).filter(
          Token.token_id == token).distinct().all()

      try:
         raise gen.Return(result[0][0])
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Invalid Token"})
         raise gen.Return(False)

   def _clear_token(self, token):
      """
      Function take in user's token whose has just called API logout to delete.
      @params: token.
      """
      self.db.query(Token).filter(Token.token_id == token).delete()
      self.db.commit()


class RefreshTokenHandler(BaseHandler):
   """
      Refresh expired token by checking token which has just been 
         sent to server is the newest and providing new one.
      @params: expired token.
   """
   SCHEMA = REFRESH_SCHEMA

   @gen.coroutine
   def post(self):
      token = self.validated_data.get('token')

      user_id = yield self._check_user_by_token(token)

      if user_id:
         token = yield self._update_token(user_id[0])
         self.write_response(
             "0000", code=HTTPStatus.OK, response_data={
                 "token": token['token_id'],
                 "token_expired": token['expiration_time']
             })
         log.info("Refresh token of User: {}".format(user_id))
      else:
         raise gen.Return(self.write_response(
             "0000", code=HTTPStatus.UNAUTHORIZED, message="Invalid Token"))

   @gen.coroutine
   def _check_user_by_token(self, token):
      """
         Find out user id of token before providing new token.
         @params: Token.
      """
      result = self.db.query(Token.user_id).filter(
          Token.token_id == token).all()

      try:
         raise gen.Return(result[0])
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Invalid Token"})
         raise gen.Return(False)

   @gen.coroutine
   def _update_token(self, user_id):
      """
         Update new token for user id of old token.
         @params: user id.
      """

      token = JwtTokenTransfrom(user_id=user_id)._transform_token()
      params = dict(
          token_id=str(token),
          user_id=user_id,
          expiration_time=int(
              int(
                  datetime.datetime.strptime(str(
                      datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000)
              + int(config.getint('token', 'login_expiry')*1000)),
          create_time=str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
      )

      self.db.query(Token).filter(Token.user_id == user_id).update({Token.token_id: params['token_id'],
                                                                    Token.expired_date: params['expiration_time'],
                                                                    Token.create_date: params['create_time']}, synchronize_session=False)
      self.db.commit()
      raise gen.Return(params)


class ReleaseLockHandlers(BaseHandler):

   @gen.coroutine
   def post(self):
      data = self.validated_data

      self.db.query(User).filter(User.user_name == data['username']).update(
          {User.locked: 0, User.login_ng_cnt: 0}, synchronize_session=False)
      self.db.commit()


class LoginCPMHandler(BaseHandler):
   @gen.coroutine
   def post(self):
      TenantId = self.validated_data.get('TenantId')
      UserId = self.validated_data.get('UserId')
      Password = self.validated_data.get('Password')
      Lang = self.validated_data.get('Lang')

      yield self._validate_user_credential(TenantId, UserId, Password)

   @gen.coroutine
   def _validate_user_credential(self, TenantId, UserId, Password):
      query = self.db.query(User).filter(
          User.tenant_id == TenantId, User.user_id == UserId).all()

      try:
         user = self.to_json(query[0])
         yield self._check_lock(UserId)
         yield self._validate_password(user['id'], Password, UserId, TenantId)
      except IndexError:
         log.error(
             "Invalid TenantId: {} or UserId: {}".format(TenantId, UserId)
         )
         raise gen.Return(self.not_found(
             result_code=HTTPStatus.NOT_FOUND, message="Invalid TenantId or UserId"))

   @gen.coroutine
   def _validate_password(self, Id, Password, UserId, TenantId):
      query = self.db.query(User, Group.group_name).join(Group, isouter=True).filter(
          User.id == Id)
      if (query.count() == 1):
         user = self.to_json(query[0][0])
         if user['password'] == Password:
            yield self._create_token(UserId)
            operation_logs = OperationLog(
                tenant_id=TenantId, user_id=UserId, operation=14)
            self.db.add(operation_logs)
            self.db.query(User).filter(User.user_id == UserId).update(
                {User.login_ng_cnt: 0}, synchronize_session=False)
            self.db.commit()
            log.info("UserId: {} login successfully".format(UserId))
            self.write_response("0000", code=HTTPStatus.OK, message=dict(
                UserId=user['user_id'],
                UserName=user['user_name'],
                Mail=user['mail'],
                GroupId=user['group_id'],
                GroupName=query[0][1],
                Device=user['device'],
                AutoinTime=user['autoin_time'],
                AuthId=user['auth_id'],
                Extension=user['extension'],
                InsertDate=user['insert_date'],
                UpdateDate=user['update_date']
            ))
         else:
            self.db.query(User).filter(User.user_id == UserId).update(
                {User.login_ng_cnt: User.login_ng_cnt + 1},
                synchronize_session=False
            )
            yield self._check_ng_to_lock(UserId)
            log.error("Invalid Password of User: {}".format(UserId))
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.UNAUTHORIZED, message="Invalid Password"
            ))
      else:
         log.error("User Invalid")
         raise gen.Return(self.not_found(
             result_code=HTTPStatus.NOT_FOUND, message="User not found"))

   @gen.coroutine
   def _check_lock(self, UserId):
      """
         Check user is locked to login or not.
         @params: username.
      """
      lock = self.db.query(User).filter(User.user_id == UserId).all()
      try:
         locked = self.to_json(lock[0])
         if locked['locked'] == 1:
            log.error("User: {} is locked".format(UserId))
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.UNAUTHORIZED, message="User locked"
            ))
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Username: {} not found".format(UserId)})

   @gen.coroutine
   def _check_ng_to_lock(self, UserId):
      """
         Check number of login failure in row of user.
         :params: username.
      """
      cnt = self.db.query(User.login_ng_cnt).filter(
          User.user_id == UserId).all()
      if cnt[0][0] >= 3:
         self.db.query(User).filter(User.user_id == UserId).update(
             {
                 User.locked: 1,
                 User.locked_date: str(
                     datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
             }, synchronize_session=False)
         self.db.commit()
         raise gen.Return(True)

   @gen.coroutine
   def _create_token(self, user_id):
      """
         Create new token and save it in database.
         @Params: user_id.
      """
      query = self.db.query(User).filter(User.user_id == user_id)
      id = self.to_json(query[0])
      token = JwtTokenTransfrom(user_id=user_id)._transform_token()
      params = dict(
          token_id=str(token),
          user_id=id['id'],
          expiration_time=int(int(datetime.datetime.strptime(str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) + int(config.getint('token', 'login_expiry')*1000)),
          create_time=str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
      )

      self._remove_expired_token(user_id=id['id'])
      self.db.query(User).filter(User.user_id == user_id).update(
          {User.login_ng_cnt: 0}, synchronize_session=False)
      new_token = Token(user_id=params['user_id'], token_id=params['token_id'],
                        expired_date=params['expiration_time'], create_date=params['create_time'])
      self.db.add(new_token)
      self.db.commit()
      self.set_secure_cookie('user', token)
      raise gen.Return(params)

   @gen.coroutine
   def _remove_expired_token(self, user_id):
      """
         Remove user's token if existed in database before provide new token.
         @Params: user_id.
      """
      self.db.query(Token).filter(Token.user_id == user_id).delete()
      self.db.commit()


class ProfileHandler(BaseHandler):
   SCHEMA = PROFILE_SCHEMA

   @gen.coroutine
   def post(self):
      pass


active_clients = dict()


class BroadcastHangdler(WebSocketHandler, BaseHandler):
   def check_origin(self, origin):
      return True

   def open(self):
      token = self.get_argument('token')
      query = self.db.query(User).filter(
          Token.user_id == User.id, Token.token_id == token)
      user = self.to_json(query[0])
      active_clients.update({self: user['user_name']})
      print(active_clients)

   def on_message(self, message):
      message = json.loads(message)

      try:
         if message['only'] == 1:
            for client in active_clients.items():
               if message['username'] == client[1]:
                  client[0].write_message(message)
      except Exception:
         for client in active_clients.keys():
            client.write_message(message)

   def on_close(self):
      print("Close Websocket")


class PasswordChangeHandler(BaseHandler):
   SCHEMA = PASSWORD_CHANGE_SCHEMA

   @gen.coroutine
   @token_required
   def post(self):
      TenantId = self.validated_data.get('TenantId')
      UserId = self.validated_data.get('UserId')
      OldPassword = self.validated_data.get('OldPassword')
      NewPassword = self.validated_data.get("NewPassword")
      ConfirmPassword = self.validated_data.get("ConfirmPassword")

      query = self.db.query(Security).filter(Security.TenantId == TenantId)
      security = self.to_json(query[0][0])

      query = self.db.query(User).filter(
          User.user_id == UserId, User.tenant_id == TenantId)
      user = self.to_json(query[0][0])

      if md5(OldPassword) == user['password']:
         if NewPassword == ConfirmPassword:
            if security['use_password_policy'] == 0:
               self.db.query(User).update({User.password: md5(ConfirmPassword)})
               self.db.commit()
               raise gen.Return(self.write_response(
                   "0000", code=HTTPStatus.OK, message="Password Change Successfully"))
            else:
               pattern = self._generate_rule(security)
               mat = re.search(re.compile(pattern), ConfirmPassword)
               if mat:
                  self.db.query(User).update({User.password: md5(ConfirmPassword)})
                  self.db.commit()
                  raise gen.Return(self.write_response(
                   "0000", code=HTTPStatus.OK, message="Password Change Successfully"))
               else:
                  raise gen.Return(self.write_response(
                   "0008", code=HTTPStatus.OK, message="Policy Illegal"))
         else:
            raise gen.Return(self.write_response(
                "0006", code=HTTPStatus.UNAUTHORIZED, message="Invalid ConfirmPassword"))
      else:
         raise gen.Return(self.write_response(
             "0007", code=HTTPStatus.UNAUTHORIZED, message="Invalid OldPassword"))

   @gen.coroutine
   def _generate_rule(self, security):
      RULE = dict(
            use_lower=[security['use_lower'], "(?=.*[a-z])", "a-z"],
            use_digit=[security['use_digit'], "(?=.*[0-9])", "\d"],
            use_upper=[security['use_upper'], "(?=.*[A-Z])", "A-Z"],
            use_sympol=[security['use_upper'],
                        "(?=.*[@$!%*#?&])", "@$!#%*?&"],
      )
      pattern = "^"
      patterns = "["
      for j in RULE.values():
         if j[0] == 1:
            pattern = pattern + j[1]
            patterns = patterns + j[2]
      pattern = pattern + patterns + "]" + \
         "{%s,}$" % security['password_lenght']
      return pattern

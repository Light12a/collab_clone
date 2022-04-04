import datetime
from ..base import BaseHandler
from .models import User, Token, Tenant
from handlers.groups.models import Group
from handlers.operation_logs.models import OperationLog
from http import HTTPStatus
from utils.config import config
from tornado import gen
from services.logging import logger as log
from .token import JwtTokenTransfrom
from .schema import LOGIN_SCHEMA, LOGOUT_SCHEMA, REFRESH_SCHEMA, PROFILE_SCHEMA

log = log.get(__name__)


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
         This function use domain and username to find out user_id of user who has just logged in.
         Params: domain, username
      """
      result = self.db.query(User.user_id).join(Tenant, User.tenant_id == Tenant.tenant_id).filter(
          Tenant.domain == company_id, User.user_name == username).distinct().all()

      try:
         raise gen.Return(result[0][0])
      except IndexError as e:
         log.error({'error_type': type(e).__name__,
                    'error': e,
                    "message": "Company_id: {} and Username: {} not found".format(company_id, username)})
         self.write_response(0000, code=HTTPStatus.UNAUTHORIZED,
                             message="Invalid Username or company_id")

   @gen.coroutine
   def _validate_user_password(self, user_id, password, username):
      """
         Function take user_id to find out password and compare with inputed password in order to verify password.
         @Params: user_id, password.
      """
      result = self.db.query(User).filter(User.user_id == user_id).all()
      user_pass = self.to_json(result[0])

      try:
         if user_pass['password'] == password:
            token = yield self._create_token(user_id)
            self.write_response(
                0000, code=HTTPStatus.OK, response_data={
                    "token": token['token_id'],
                    "token_expired": token['expiration_time']
                })
            log.info("Username: {} login successfully".format(username))
         else:
            self.db.query(User).filter(User.user_id == user_id).update(
                {User.login_ng_cnt: User.login_ng_cnt + 1}, synchronize_session=False)
            yield self._check_cnt_to_lock(username)
            self.write_response(
                0000, code=HTTPStatus.UNAUTHORIZED, message="Invalid password")

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
      token = JwtTokenTransfrom(user_id=user_id)._transform_token()
      params = dict(
          token_id=str(token),
          user_id=user_id,
          expiration_time=int(int(datetime.datetime.strptime(str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) + int(config.getint('token', 'login_expiry')*1000)),
          create_time=str(
              datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
      )

      self._remove_expired_token(user_id=user_id)
      self.db.query(User).filter(User.user_id == user_id).update(
          {User.login_ng_cnt: 0}, synchronize_session=False)
      new_token = Token(user_id=params['user_id'], token_id=params['token_id'],
                        expired_date=params['expiration_time'], create_date=params['create_time'])
      self.db.add(new_token)
      self.db.commit()

      raise gen.Return(params)

   @gen.coroutine
   def _check_format_json(self, json):
      """
         Catch format of json request for login or relogin.
         @Params: json request.
      """
      try:
         token = json['token']
      except Exception as e:
         log.info({'error_type': type(e).__name__,
                   'error': e,
                   "message": "json format for new login of User: {}".format(json['username'])})
         raise gen.Return(False)
      raise gen.Return(True)

   def _check_token_valid(self, request):
      """
         Check token which user has just sent to server is newest.
         @Params: Token field in json request.
      """
      result = self.db.query(Token.user_id).filter(
          Token.token_id == request)

      try:
         if result[0][0]:
            self.write_response(
                "0000", code=HTTPStatus.OK, response_data={"code": 200})
      except IndexError:
         resp = {
             "code": 401,
             "message": "Invalid Token"
         }
         self.write_response(
             "0000", code=HTTPStatus.UNAUTHORIZED, response_data=resp)

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
            self.write_response(
                0000, code=HTTPStatus.UNAUTHORIZED, message="User locked")
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
         self.write_response(
             0000, code=HTTPStatus.OK)
         log.info("User logged out successfully with token: {}".format(token))
      else:
         self.write_response(
             401, code=HTTPStatus.UNAUTHORIZED, message="Invalid Token")

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
             0000, code=HTTPStatus.OK, response_data={
                 "token": token['token_id'],
                 "token_expired": token['expiration_time']
             })
         log.info("Refresh token of User: {}".format(user_id))
      else:
         self.write_response(
             401, code=HTTPStatus.UNAUTHORIZED, message="Invalid Token")

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
      query = self.db.query(User, Group.group_name).filter(
         User.group_id == Group.group_id, User.id == Id)
      if (query.count() == 1):
         user = self.to_json(query[0][0])
         token = JwtTokenTransfrom(user_id=UserId)._transform_token()
         if user['password'] == Password:
            self.write_response(0000, code=HTTPStatus.OK, message=dict(
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
            operation_logs = OperationLog(
               tenant_id=TenantId, user_id=UserId, operation=14)
            self.db.add(operation_logs)
            self.db.query(User).filter(User.user_id == UserId).update(
               {User.login_ng_cnt: 0}, synchronize_session=False)
            self.db.commit()
            self.set_secure_cookie('user', token)
            log.info("UserId: {} login successfully".format(UserId))
         else:
            self.db.query(User).filter(User.user_id == UserId).update(
                {User.login_ng_cnt: User.login_ng_cnt + 1},
                synchronize_session=False
            )
            yield self._check_ng_to_lock(UserId)
            self.write_response(
                0000, code=HTTPStatus.UNAUTHORIZED, message="Invalid Password"
            )
            log.error("Invalid Password of User: {}".format(UserId))
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
            self.write_response(
                0000, code=HTTPStatus.UNAUTHORIZED, message="User locked"
            )
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

class ProfileHandler(BaseHandler):
   SCHEMA = PROFILE_SCHEMA

   @gen.coroutine
   def post(self):
      pass

import datetime
from ..base import BaseHandler
from .models import User, Token, Tenant
from http import HTTPStatus
from utils.config import config
from tornado import gen
from services.logging import logger as log
from .token import JwtTokenTransfrom

log = log.get(__name__)
class LoginHandler(BaseHandler):
    """
        This class is created to build Login API.
        Params of request are domain, username and password.
        The other side, this API can use for re-login with request's format is token.
        User who logged in failure 3 times in row will be locked.
    """

    @gen.coroutine
    def post(self):
        data = self.validated_data

        if data:
            if not (("company_id" in data and "username" in data and "password" in data) or ("token" in data)):
                log.error("Json request format is wrong")
                raise gen.Return(
                    self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))
            
            lock = yield self._check_lock(data['username'])
            
            if lock:
                log.error("User: {} is locked".format(data['username']))
                raise gen.Return(
                    self.error(code=HTTPStatus.UNAUTHORIZED, message="User is locked"))

            check = yield self._check_format_json(data)
            
            if check:
                self._check_token_valid(data)
            else:
                credential = yield self._user_credential_read(
                    domain=data['company_id'], username=data['username'])

                if not credential:
                    self.write_response(
                        401, code=HTTPStatus.UNAUTHORIZED,
                                            message="username or company_id is wrong")
                else:
                    password_valid = yield self._validate_user_password(
                        credential, password=data['password'])
                    if not password_valid:
                        self.db.query(User).filter(User.user_id==credential).update(
                            {User.login_ng_cnt : User.login_ng_cnt + 1}, synchronize_session = False)

                        yield self._check_cnt_to_lock(data['username'])
                        self.write_response(401,code=
                                HTTPStatus.UNAUTHORIZED, message="Password is wrong")
                    else:
                        token = yield self._create_token(credential)
                        resp = {
                            "token": token['token_id'],
                            "token_expired":token['expiration_time']
                        }
                        self.set_secure_cookie("user", token['token_id'])
                        self.write_response(
                            200, code=HTTPStatus.OK, response_data=resp)
                        log.info("Username: {} login successfully".format(data['username']))
        else:
            log.error("Json request format is wrong")
            raise gen.Return(
                self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))
 
    @gen.coroutine
    def _user_credential_read(self, domain, username):
        """
            This function use domain and username to find out user_id of user who has just logged in.
            Params: domain, username
        """
        result = self.db.query(User.user_id).join(Tenant, User.tenant_id == Tenant.tenant_id).filter(
            Tenant.domain == domain, User.user_name == username).distinct().all()
        
        try:
            
            raise gen.Return(result[0][0])
        except IndexError as e:
            log.error({'error_type': type(e).__name__,
                        'error': e, 
                        "message":"Domain: {} and username: {} not found".format(domain, username)})
            raise gen.Return(False)
          
    @gen.coroutine
    def _validate_user_password(self, user_id, password):
        """
            Function take user_id to find out password and compare with inputed password in order to verify password.
            @Params: user_id, password.
        """
        result = self.db.query(User).filter(User.user_id == user_id).all()

        user_pass = self.to_json(result[0])
        try:
            if user_pass['password'] == password:
                raise gen.Return(True)
        except IndexError as e:
            log.error({'error_type': type(e).__name__,
                        'error': e, 
                        "message":"Password of user: {} is wrong".format(user_id)})
            raise gen.Return(False)
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
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) +  int(config.getint('token','login_expiry')*1000)),
            create_time=str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))  
        )

        self._remove_expired_token(user_id=user_id)
        self.db.query(User).filter(User.user_id==user_id).update({User.login_ng_cnt:0},synchronize_session = False)
        new_token = Token(user_id = params['user_id'], token_id = params['token_id'],
                          expired_date = params['expiration_time'], create_date = params['create_time'])
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
                        "message":"json format for new login of User: {}".format(json['username'])})
            raise gen.Return(False)
        raise gen.Return(True)
    
    def _check_token_valid(self, request):
        """
            Check token which user has just sent to server is newest.
            @Params: Token field in json request.
        """
        result = self.db.query(Token.user_id).filter(
            Token.token_id == request['token'])
        
        try:
            if result[0][0]:
                self.write_response(
                    200,code=HTTPStatus.OK, response_data={"code":200})
        except IndexError:
            resp = {
                "code": 401,
                "message": "Token is wrong"
            }
            self.write_response(
                401,code=HTTPStatus.UNAUTHORIZED, response_data=resp)

    @gen.coroutine
    def _check_cnt_to_lock(self, username):
        """
            Check number of login failure in row of user.
            @params: username.
        """
        cnt = self.db.query(User.login_ng_cnt).filter(User.user_id==username).all()
                 
        if cnt[0][0] >= 3:
            self.db.query(User).filter(User.user_id==username).update(
                {
                    User.locked : 1, 
                    User.locked_date : str(
                        datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
            }, synchronize_session = False)
            self.db.commit()
            raise gen.Return(True)

    @gen.coroutine
    def _check_lock(self, username):
        """
            Check user is locked to login or not.
            @params: username.
        """
        lock = self.db.query(User).filter(User.user_name==username).all()
        locked = self.to_json(lock[0])

        try:
            if locked['locked'] == 1:
                return gen.Return(True)
        except IndexError as e:
            log.error({'error_type': type(e).__name__,
                        'error': e, 
                        "message":"Username: {} not found".format(username)})
            return gen.Return(False)

class LogoutHandler(BaseHandler):
    """
        API is used for logging out of system.
        @params: Token
    """
    @gen.coroutine
    def post(self):
        """
            Check token which has just been sent to server is the newest and delete it.
        """
        data = self.validated_data

        if data:
            if not "token" in data:
                log.error("Request json is wrong")
                raise gen.Return(
                    self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))

            check = yield self._check_token_exists(data['token'])
                
            if check:
                self._clear_token(data['token'])
                self.clear_cookie("user", data['token'])
                self.write_response(
                    200, code=HTTPStatus.OK)
                log.info("User logged out successfully with token: {}".format(data['token']))
            else:
                self.write_response(
                    401, code=HTTPStatus.UNAUTHORIZED, message="Token is wrong")
        else:
            log.error("Request json is wrong")
            raise gen.Return(
                self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))

    @gen.coroutine
    def _check_token_exists(self, token):
        """
        Function take in token to verify this one is the newest.
        @params: Token.
        """
        result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

        try:
            raise gen.Return(result[0][0])
        except IndexError as e:
            log.error({'error_type': type(e).__name__,
                        'error': e, 
                        "message":"Token is wrong"})
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
    @gen.coroutine
    def post(self):
        data = self.validated_data
        
        if data:
            if not ('token' in data):
                err = "Bad request with json request"
                log.info(err)
                raise gen.Return(
                    self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))
            
            user_id = yield self._check_user_by_token(data['token'])
            
            if user_id:
                token = yield self._update_token(user_id[0])
                resp = {
                    "token": token['token_id'],
                    "token_expired": token['expiration_time']
                }
                self.write_response(
                    200,code=HTTPStatus.OK.value, response_data=resp)
                log.info("Refresh token of User: {}".format(user_id))
            else:
                self.write_response(
                    401, code=HTTPStatus.UNAUTHORIZED, message="Token is wrong")
        else:
            log.info("Bad request with json request")
            raise gen.Return(
                self.error(code=HTTPStatus.BAD_REQUEST, message="Bad request"))

    @gen.coroutine
    def _check_user_by_token(self, token):
        """
            Find out user id of token before providing new token.
            @params: Token.
        """
        result = self.db.query(Token.user_id).filter(Token.token_id==token).all()
        
        try:
            raise gen.Return(result[0])
        except IndexError as e:
            log.error({'error_type': type(e).__name__,
                        'error': e, 
                        "message":"Token is wrong"})
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
            expiration_time=int(int(datetime.datetime.strptime(str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) +  int(config.getint('token','login_expiry')*1000)),
            create_time=str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))  
        )

        self.db.query(Token).filter(Token.user_id == user_id).update({Token.token_id : params['token_id'], 
                                    Token.expired_date : params['expiration_time'],
                                    Token.create_date : params['create_time']}, synchronize_session = False)
        self.db.commit()

        raise gen.Return(params)

class ReleaseLockHandlers(BaseHandler):

    @gen.coroutine
    def post(self):
        data = self.validated_data

        self.db.query(User).filter(User.user_name == data['username']).update({User.locked : 0}, synchronize_session = False)
        self.db.commit()

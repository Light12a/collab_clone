import imp
import datetime
from multiprocessing.sharedctypes import synchronized
from unittest import result
import uuid
import json
from ..base import BaseHandler
from .models import User, Token, Tenant
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log
from sqlalchemy import inspect

log = log.get(__name__)
class LoginHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build Login API.
    Params of request are domain, username and password.
    The other side, this API can use for re-login with request's format is token.
    """

    @gen.coroutine
    def post(self):
            
        data = self.data_received()

        if data:
            if not (("domain" in data and "username" in data and "password" in data) or ("token" in data)):
                inf = "Json request format is wrong"
                log.info(inf)
                self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            check = yield self._check_format_json(data)
            if check:
                self._check_token_valid(data)
            else:
                credential = yield self._user_credential_read(
                    domain=data['domain'], username=data['username'])
                if not credential:
                    self.write_response(401, code=HTTPStatus.UNAUTHORIZED.value,
                                            message="username or domain is wrong")
                    err = "Username: {} or domain: {} is wrong"
                    log.info(err.format(data['username'], data['domain']))
                else:
                    password_valid = yield self._validate_user_password(
                        credential, password=data['password'])
                    if not password_valid:
                        self.write_response(401,code=
                                HTTPStatus.UNAUTHORIZED.value, message="Password is wrong")
                        err = "Password: {} of username: {} is wrong"
                        log.info(err.format(data['password']), data['username'])
                    else:
                        token = yield self._create_token(credential)
                        resp = {
                            "token": token['token_id'],
                            "token_expired":token['expiration_time']
                        }
                        self.write_response(200, code=HTTPStatus.OK.value, response_data=resp)
                        inf = "Username: {} login successfully"
                        log.info(inf.format(data['username']))
        else:
            inf = "Json request format is wrong"
            log.info(inf)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
 
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
        except IndexError:
            raise gen.Return(False)
          
    @gen.coroutine
    def _validate_user_password(self, user_id, password):
        """
        Function take user_id to find out password and compare with inputed password in order to verify password.
        Params: user_id, password.
        """
        result = self.db.query(User.password).filter(User.user_id == user_id)
        try:
            if result[0][0] == password:
                raise gen.Return(True)
        except ValueError:
            raise gen.Return(False)
    @gen.coroutine
    def _remove_expired_token(self, user_id):
        """
        Remove user's token if existed in database before provide new token.
        Params: user_id.
        """
        self.db.query(Token).filter(Token.user_id == user_id).delete()
        self.db.commit()
    @gen.coroutine
    def _create_token(self, user_id):
        """
        Create new token and save it in database.
        Params: user_id.
        """
        params = dict(
            token_id=str(uuid.uuid4()),
            user_id=user_id,
            expiration_time=int(int(datetime.datetime.strptime(str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S').timestamp()*1000) +  int(config.getint('token','login_expiry')*1000)),
            create_time=str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))  
        )

        self._remove_expired_token(user_id=user_id)
        new_token = Token(user_id = params['user_id'], token_id = params['token_id'],
                          expired_date = params['expiration_time'], create_date = params['create_time'])
        self.db.add(new_token)
        self.db.commit()

        raise gen.Return(params) 
    @gen.coroutine
    def _check_format_json(self, json):
        """
        Catch format of json request for login or relogin.
        Params: json request.
        """
        try:
            token = json['token']
        except KeyError:
            raise gen.Return(False)
        raise gen.Return(True)
    
    def _check_token_valid(self, request):
        """
        Check token which user has just sent to server is newest.
        Params: Token field in json request.
        """
        result = self.db.query(Token.user_id).filter(
            Token.token_id == request['token'])
        
        try:
            if result[0][0]:
                self.write_response(200,code=HTTPStatus.OK.value, response_data={"code":200})
        except IndexError:
            resp = {
                "code": 401,
                "message": "Token is wrong"
            }
            self.write_response(401,code=HTTPStatus.UNAUTHORIZED.value, response_data=resp)

class LogoutHandler(ResponseMixin, BaseHandler):
    """
        API is used for logging out of system.
        @params: Token
    """
    @gen.coroutine
    def post(self):
        """
            Check token which has just been sent to server is the newest and delete it.
        """
        data = self.data_received()

        if data:
            if not "token" in data:
                err = "Request json is wrong"
                log.info(err)
                self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

            check = yield self._check_token_exists(data['token'])
                
            if check:
                self._clear_token(data['token'])
                self.write_response(200, code=HTTPStatus.OK.value)
                inf = "User logged out successfully with token: {}"
                log.info(inf.format(data['token']))
            else:
                self.write_response(401, code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
                inf = "Token: {} is wrong"
                log.info(inf.format(data['token']))
        else:
            err = "Request json is wrong"
            log.info(err)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

    @gen.coroutine
    def _check_token_exists(self, token):
        """
        Function take in token to verify this one is the newest.
        @params: Token.
        """
        result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

        try:
            raise gen.Return(result[0][0])
        except IndexError:
            raise gen.Return(False)

    def _clear_token(self, token):
        """
        Function take in user's token whose has just called API logout to delete.
        @params: token.
        """
        self.db.query(Token).filter(Token.token_id == token).delete()
        self.db.commit()

class RefreshTokenHandler(ResponseMixin, BaseHandler):
    """
        Refresh expired token by checking token which has just been 
            sent to server is the newest and providing new one.
        @params: expired token.
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if data:
            if not ('token' in data):
                err = "Bad request with json request"
                log.info(err)
                self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            user_id = yield self._check_user_by_token(data['token'])

            if user_id:
                token = yield self._update_token(user_id)
                resp = {
                    "token": token['token_id'],
                    "token_expired": token['expiration_time']
                }
                self.write_response(200,code=HTTPStatus.OK.value, response_data=resp)
                inf = "Refresh token of User: {}"
                log.info(inf.format(user_id))
            else:
                self.write_response(401, code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
                inf = "Token: {} is wrong"
                log.info(inf.format(data['token']))
        else:
            err = "Bad request with json request"
            log.info(err)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

    @gen.coroutine
    def _check_user_by_token(self, token):
        """
            Find out user id of token before providing new token.
            @params: Token.
        """
        result = self.db.query(Token.user_id).filter(Token.token_id==token).all()
        
        try:
            raise gen.Return(result[0])
        except IndexError:
            raise gen.Return(False)

    @gen.coroutine
    def _update_token(self, user_id):
        """
            Update new token for user id of old token.
            @params: user id.
        """
        params = dict(
            token_id=str(uuid.uuid4()),
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

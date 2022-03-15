import imp
import datetime
from telnetlib import Telnet
import uuid
import json
from ..base import BaseHandler
from .models import User, Token, Tenant
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log

log = log.get(__name__)
class LoginHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build Login API.
    Params of request are domain, username and password.
    The other side, this API can use for re-login with request's format is token.
    """
    @property
    def db(self):
        return self.application.session

    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(bytes.decode(self.request.body))

    @gen.coroutine
    def post(self):
        try:
            data = self.data_received()
            if not (("domain" in data and "username" in data and "password" in data) or ("token" in data)):
                raise ValueError
            check = yield self._check_format_json(data)
            if check:
                yield self._check_token_valid(data)
            else:
                credential = yield self._user_credential_read(
                    domain=data['domain'], username=data['username'])
                if not credential:
                    self.write_response(status="Failure", code=HTTPStatus.UNAUTHORIZED.value,
                                        message="username or domain is wrong")
                    err = "Username: {} or domain: {} is wrong"
                    log.error(err.format(data['username'], data['domain']))
                else:
                    password_valid = yield self._validate_user_password(
                        credential, password=data['password'])
                    if not password_valid:
                        self.write_response("Failure",code=
                            HTTPStatus.UNAUTHORIZED.value, message="Password is wrong")
                        err = "Password: {} of username: {} is wrong"
                        log.error(err.format(data['password']), data['username'])
                    else:
                        token = yield self._create_token(credential)
                        resp = {
                            "token": token['token_id'],
                            "token_expired":token['expiration_time']
                        }
                        self.write_response("success", code=HTTPStatus.OK.value, response_data=resp)
                        inf = "Username: {} login successfully"
                        log.info(inf.format(data['username']))
        except ValueError:
            print("day la loi")
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Username: {}, Domain: {}, Password: {} in wrong format"
            log.debug(err.format(data['username'], data['domain'], data['password']))
    @gen.coroutine
    def _user_credential_read(self, domain, username):
        """
        This function use domain and username to find out user_id of user who has just logged in.
        Params: domain, username
        """
        result = self.db.query(User.user_id).join(Tenant, User.tenant_id == Tenant.tenant_id).filter(
            Tenant.domain == domain, User.user_name == username).distinct()
        
        if result is None:
            return False
        else:
            return result[0][0]
    @gen.coroutine
    def _validate_user_password(self, user_id, password):
        """
        Function take user_id to find out password and compare with inputed password in order to verify password.
        Params: user_id, password.
        """
        result = self.db.query(User.password).filter(User.user_id == user_id)
        try:
            if result[0][0] == password:
                return True
        except ValueError:
            return False
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

        return params
    @gen.coroutine
    def _check_format_json(self, json):
        """
        Catch format of json request for login or relogin.
        Params: json request.
        """
        try:
            token = json['token']
        except KeyError:
            return False
        return True
    
    @gen.coroutine
    def _check_token_valid(self, request):
        """
        Check token which user has just sent to server is newest.
        Params: Token field in json request.
        """
        result = self.db.query(Token.token_id).filter(
            Token.token_id == request['token'])

        if result.token_id:
            self.write_response("Success",code=HTTPStatus.OK.value, response_data={"code":200})
        else:
            resp = {
                "code": 401,
                "message": "Token is wrong"
            }
            self.write_response("Failure",code=HTTPStatus.NOT_FOUND.value, result=resp)

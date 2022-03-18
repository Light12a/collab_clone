from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import code
from dataclasses import dataclass
import imp
import datetime
from multiprocessing.sharedctypes import synchronized
from unittest import result
from urllib import request
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
import requests
from . import state_value
log = log.get(__name__)


# class LoginHandler(ResponseMixin, BaseHandler):
#     def get(self):
#         results = self.db.query(User).all()
#         for result in results:
#             print(result.user_name)
class LoginHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build Login API.
    Params of request are domain, username and password.
    The other side, this API can use for re-login with request's format is token.
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        print("data", data)
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
        print("start issue")
        result = self.db.query(User.user_id).join(Tenant, User.tenant_id == Tenant.tenant_id).filter(
            Tenant.domain == domain, User.user_name == username).distinct().all()
        print("issue")
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

class ApplyStateHandler(ResponseMixin, BaseHandler):
    """
    This class will apply a state & a sub_state to user
    The acceptable cases is described on COLLABOS API - sheet Presence State Code
    @params: token, state, sub_state
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if ("token" and "state" and "sub_state") in data:
            check, token = yield self._check_token_exists(data['token'])
            if check: 
                self._apply_state(data)
            else:
                self.write_response("Success", code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")   
        else:
            err = "Bad request with json request"
            log.error(err)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
            Output: False  or
                    True and token
        """
        result = self.db.query(Token.token_id).filter(Token.token_id == token)
        if result == None:
            raise gen.Return(False)
        else:
            raise gen.Return(True, token)
    
    @gen.coroutine
    def _get_current_state(self, token):    
        username = self.db.query(User.user_name).join(Token, User.user_name == Token.token_id).filter(Token.token_id == token)
        result =  yield requests.get("http://35.75.95.117:8088/ari/deviceStates/PJSIP%2F{}".\
                    format(username), auth=("asterisk","asterisk")).json()['state']
        return state_value.STATES[result]

    @gen.coroutine
    def _apply_state(self, data):
        away_code_id_maximum = 15
        current_state = yield self._get_current_state(data["token"])
        if  (data["state"] not in [100, 101, 102]) or \
            (data["state"] in [101, 102] and data["sub_state"] != 0) or \
            (data["state"] == 100 and data["sub_state"] not in list(range(1, away_code_id_maximum+1))) or \
            (current_state == 104):
            params = yield self._get_user_state(data["token"])
            respo = {
                "code": 200,
                "username": params[0], 
                "displayname": params[1],
                "groupId": params[2],
                "state": -1,
                "sub_state": -1,
            }
            self.write_response("Success", HTTPStatus.OK.value, response_data=respo)
            info = "State & substate does not have update because invalid input"
            log.info(info)
        else:
            self._apply_state(data['state'], data['sub_state'], data['token'])
            params = self._get_user_state(data['token'])
            respo = {
                "code": 200,
                "username": params[0], 
                "displayname": params[1],
                "groupId": params[2],
                "state": 100, #temp
                "sub_state": 100, #temp
            }
            self.write_response("Success", HTTPStatus.OK.value, response_data=respo)
            info = "Update state: {}, sub_state: {} to username: {} is success"
            log.info(info.format(params[3], params[4], params[0]))
    
    @gen.coroutine
    def _get_user_state(self, token):
        """
        SELECT u.username, concat(u.firstname,' ', u.middlename,' ', u.lastname), u.group_id,
        u.user_state_id, u.substate, t.token_id from backend.user as u join backend.token as t
        on t.user_id = u.user_id where token_id = '{}';
        """
        try:
            results = self.db.query(User.username, User.firstname + User.middlename + User.lastname, \
                    User.group_id).join(Token, Token.user_id == User.user_id).filter(Token.token_id == token).first()
            raise gen.Return(results)
        except:
            log.error("Issue in _get_user_state")
            raise gen.Return(False)


class GetUserStateHandler(ResponseMixin, BaseHandler):
    """
    ...
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if 'token' in data:
            check, token = self._check_token_exists(data['token'])
            if check:
                self._get_user_state(data)
            else:
                self.write_response("Failure", HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
        else:
            err = "Bad request with json request"
            log.info(err)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

    @gen.coroutine
    def _get_user_state(self, data):
        params = self._get_state(data['token'])       
        state, substate = self._get_state_and_substate(data['token'])
        note = self._get_away_code(params[3], params[4])
        if state == 100:
            respo= {
                "code" : 200, 
                "username": params[0], 
                "displayname": params[1],
                "groupId": params[2],
                "state":   params[3],
                "sub_state": params[4],  
                "note": note,
            }
            self.write_response("Success", HTTPStatus.OK.value, response_data=respo)
        else:
            respo= {"code" : 200, 
                    "username": params[0], 
                    "displayname": params[1],
                    "groupId": params[2],
                    "state":   state,
                    "sub_state": substate,  
                    "note": note,
                    }
            self._apply_state(state, substate, data['token'])
            self.write_response("Success", HTTPStatus.OK.value, response_data=respo)
    @gen.coroutine
    def _get_state(self, token):
        """
        "SELECT u.username, concat(u.firstname,' ', u.middlename,' ', u.lastname), 
        u.group_id, u.user_state_id, u.substate, t.token_id from backend.user as u 
        join backend.token as t on t.user_id = u.user_id where token_id = '{}';
        """
    @gen.coroutine
    def _get_state_and_substate(self, data):
        """
        ...
        """
    @gen.coroutine
    def _get_away_code(self, data):
        """
        ...
        """
    @gen.coroutine
    def _apply_state(self, data):
        """
        ...
        """
    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
            Output: False  or
                    True and token
        """
        result = self.db.query(Token.token_id).filter(Token.token_id == token)
        if result == None:
            raise gen.Return(False)
        else:
            raise gen.Return(True, token)
            
class GetUserConfigHandler(BaseHandler, ResponseMixin):
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if 'token' in data:
            check, token = self._check_token_exists(data['token'])
            if check:
                yield self._get_user_config(data)
            else:
                self.write_response("Success", HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
        else:
            err = "Bad request with json request"
            log.info(err)
            self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
    @gen.coroutine
    def _get_user_config(self, data):
            """
            select u.user_id, u.username,concat(u.firstname,' ', u.middlename,' ', u.lastname) 
            as displayname, u.group_id,  t.tenant_name, u.authority_id, u.user_state_id, 
            u.extension_number, u.user_classifier, u.user_state_id, t.prefix, u.allow_monitor,
             u.allow_coach from backend.user as u join backend.tenant as t on u.tenant_id = t.tenant_id 
            join backend.token as tok on tok.user_id = u.user_id where tok.token_id = '{}';
            """
            try:
                query = self.db.query(User, Token, Tenant).filter().first()
                respo = {}
                self.write_response("Success",)
            except:
                self.write_response("Failure", HTTPStatus.NOT_FOUND, message="error")
                err = "Issue in query statement"
                log.debug(err)

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
            Output: False  or
                    True and token
        """
        result = self.db.query(Token.token_id).filter(Token.token_id == token)
        if result == None:
            raise gen.Return(False)
        else:
            raise gen.Return(True, token)
     
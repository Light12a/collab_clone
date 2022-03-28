import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import User, Token, UserRecord
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
import requests
from . import state_value
from services.logging import logger as log
log = log.get(__name__)
class LoginHandler(BaseHandler):
    @property
    def db(self):
        return self.application.session

    @gen.coroutine
    def get(self):
        self.set_secure_cookie("user", "85a55880-a85b-4515-a89f-a263fd1c07ce")
        self.write("85a55880-a85b-4515-a89f-a263fd1c07ce")

        # self.set_secure_cookie("user", "092HK3399p@3")
        # self.write("092HK3399p@3")
class LogoutHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        self.clear_cookie("user")
        self.write("Logout")

class ApplyStateHandler(BaseHandler):
    """
    This class will apply a state & a sub_state to user
    The acceptable cases is described on COLLABOS API - sheet Presence State Code
    @params: token, state, sub_state
    """
    @gen.coroutine
    def post(self):
        """
        Post method is implemented.
        """
        data = self.data_received()
        if 'token' in data and 'state' in data and 'substate' in data:
            check = yield self._check_token_exists(data['token'])
            if check:
                self._apply_state(data)
            else:
                self.write_response("Failure", code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
                info = "Token: {} is wrong"
                log.info(info.format(data['token']))
        else:
            err = "request format is wrong"
            log.warning(err)
            self.error(message="Bad request with json request", code=HTTPStatus.BAD_REQUEST.value)

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
        """
        try:
            result = self.db.query(Token.token_id).filter(Token.token_id == token)
            if result[0][0] == token:
                return True
            else: return False
        except:
            return False
    
    @gen.coroutine
    def _get_deviceState(self, token):    
        """
        Meaning: Get deviceState by token. The Function use token to find username and 
                return state code in state_value.py
        Input : token
        Output : a tuple contains state and substate
        """
        try:
            username = self.db.query(User.user_name).join(Token, User.user_id == Token.user_id).filter(Token.token_id == token)
            result =  requests.get("http://35.75.95.117:8088/ari/deviceStates/PJSIP%2F{}".\
                        format(username[0][0]), auth=("asterisk","asterisk")).json()['state']
            return state_value.STATES[result], state_value.SUB_STATES[result]
        except:
            log.error("Issue in _get_deviceState")
            self.error(message="Internal Server Error")

    @gen.coroutine
    def _apply_state(self, data):
        """
        Meaning: apply state follows condition in Collabos API Sheet
        Input: request data
        """
        try:
            deviceState = (yield self._get_deviceState(data['token']))[0]
            if  (deviceState != 104) and\
                ((data['state'] in [100, 101, 102] and data['sub_state'] == 0) or\
                (data['state'] == 103 and data['sub_state'] in [0, 1, 2, 3])):
                self._apply(data)
                self._get_user_state(data["token"], 1)
            else:
                self._get_user_state(data['token'], 0)
        except:
            log.error("Issue in _apply_state")
            self.error(message="Internal Server Error")

    @gen.coroutine
    def _apply(self, data):
        """
        Meaning: update SQL for acd_status and sub_status in UserRecord table
        Input: data request
        """
        try:
            query = self.db.query(UserRecord).filter(User.user_id == Token.user_id, \
                    User.user_id == UserRecord.user_id, Token.token_id == data['token']).one()
            query.acd_status = data['state']
            query.sub_status = data['sub_state']
            self.db.commit()
            log.info("update SQL success")
        except: 
            log.error("Issue in _apply()")
            self.error(message="Internal Server Error")
            
    @gen.coroutine
    def _get_user_state(self, token, flag=0):
        """
        Meaning: flag = 0 => appy state fail => response: state=-1; sub_state=-1
                 flag = 1 => apply state success => response: updated state & updated substate
        Input:  token, flag
        Output: JSON reponses
        """
        try:
            results = self.db.query(User.user_name, (User.firstname + User.middlename\
                    + User.lastname), User.group_id, UserRecord.acd_status, UserRecord.sub_status)\
                    .join(UserRecord, UserRecord.user_id == User.user_id)\
                    .join(Token, Token.user_id == User.user_id)\
                    .filter(Token.token_id == token)
            if flag == 1:
                respo = {
                    "code": 200,
                    "username": results[0][0], 
                    "displayname": results[0][1],
                    "groupId": results[0][2],
                    "state": results[0][3], 
                    "sub_state": results[0][4], 
                }
            else:
                 respo = {
                    "code": 200,
                    "username": results[0][0], 
                    "displayname": results[0][1],
                    "groupId": results[0][2],
                    "state": -1, 
                    "sub_state": -1, 
                }
            self.write_response("Success", code=HTTPStatus.OK.value, response_data=respo)
            inf = "Response success with {}"
            log.info(inf.format(respo))
        except:
            log.error("Issue in _get_user_state")
            self.error(message="Internal Server Error")


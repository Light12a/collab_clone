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
            
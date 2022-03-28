from email.policy import HTTP
import imp
import datetime
import uuid
import json

from grpc import Call
from handlers.tenant_settings.models import CallRecord
from handlers.users.models import UserRecord, Token
from ..base import BaseHandler
from .models import CorrespondenceMemo, RespondingMemo, User
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log


log = log.get(__name__)

class GetCorrespondenceMemoListHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build API for get correspondence memo.
    Params of request is token.
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if 'token' in data:
            check = yield self._check_token_exists(data["token"])
            if check:
                self._get_correspondence_memo()
            else:
                self.write_response("Failure", code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
        else: 
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

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
    
    def _get_correspondence_memo(self):
        results = self.db.query(RespondingMemo.memo_id, RespondingMemo.memo_name).all()
        if results:
            memo =[{
                "id": result[0],
                "text": result[1]
                } for result in results]
            resp = {
                "code": 200,
                "memo": memo
            }
            self.write_response("Success", code = HTTPStatus.OK.value, response_data=resp)
        else:
            resp = {
            "code": 404,
            "errorMessage": "No data"
            }
            err = "Not found any correspondence memo"
            log.error(err)
            self.write_response("Failure", code=HTTPStatus.NOT_FOUND.value, response_data=resp)


class ApplyCorrespondenceMemoHandler(ResponseMixin, BaseHandler):
    """
    This class apply a correspondence memo to a call 
    @param: token, memo_id, memo_note, call_id
    """
    @gen.coroutine
    def post(self):
        data = self.data_received()
        if 'token' and 'memo_id' and 'memo_note' and 'call_id' in data:
            check = yield self._check_token_exists(data['token'])
            if check:
                self._apply_correspondence_memo(data)
            else:
                self.write_response("Failure", code = HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
        else:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {}, memo id {}, memo {}, call_id {} in wrong format"
            log.debug(err.format(data['token'], data['memo_id'], data['memo'], data['call_id'], ))

    @gen.coroutine
    def _apply_correspondence_memo(self, data):
        try:
            query = self.db.query(CallRecord).filter(CallRecord.call_record_id == data['call_id'], Token.user_id == User.user_id, Token.token_id == data['token']).one()
            query.memo_id = data['memo_id']
            self.db.commit()
            respo = {"code":200}
            self.write_response("Success", code=HTTPStatus.OK.value, response_data=respo)
        except:
            self.error("Failure", code=HTTPStatus.NOT_FOUND.value, message="Data not found")

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
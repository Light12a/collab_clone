import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import SoundFiles, User, Token
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log


log = log.get(__name__)

class GetCorrespondenceMemoHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build API for get correspondence memo.
    Params of request is token.
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
            if 'token' in data:
                check, token = self._check_token_exists(data["token"])
                if check:
                    pass
            else: raise ValueError
        except ValueError:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

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
    
    def _get_correspondence_memo(self):
        results = self.db.query.all()
        if results:
             memo =[{
                "id": result[0][0],
                "text": result[0][2]
                } for result in results]
        else:
            resp = {
            "code": 404,
            "errorMessage": "No data"
            }
            err = "Not found any correspondence memo"
            log.error(err)
            self.write_response("Failure",)
       
        self.write_response





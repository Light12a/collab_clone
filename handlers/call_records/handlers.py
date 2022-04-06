import imp
import datetime
import re
import uuid
import json
import MySQLdb
from pandas import concat
from sqlalchemy import func

from db import CallRecord

from ..base import BaseHandler

from users.models import User, Token, Tenant
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log

log = log.get(__name__)

class GetCallInfoHandlers(BaseHandler):
    """
    This API is used to get all call information by callId.
    Params: token, ext_number
    """
    
    @gen.coroutine
    def post(self):
        try:
            data = self.validated_data
            if ("token" and "ext_number") in data:
                check = yield self._check_token_exists(data['token'])
                if check:
                    call_info = yield self._get_call_info(data)
            
                
        except ValueError:
            self.write({"code":400, "errorMessage":"Bad request"})
            self.set_status(400)

    @gen.coroutine
    def _get_call_info(self, data):
        result = self.db.query(CallRecord).filter(CallRecord.destination == data['ext_number']).all()
        
        try: 
            raise gen.Return(result[0].to_json())
        except IndexError:
            raise gen.Return(False)

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
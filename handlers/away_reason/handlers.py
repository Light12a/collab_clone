import imp
import datetime
import uuid
import json
import MySQLdb
from sqlalchemy import func
from ..base import BaseHandler
from ..users.models import Token, Tenant, User
from .models import AwayReason
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log

log = log.get(__name__)

class GetAwayReasonsHandler(BaseHandler):
    """
    This class is created to build Get Away Reasons API.
    Param of request is ID of token.
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
            request = self.data_received()
            if "token" in request:
                check = yield self._check_token_exists(request['token'])
                if check:
                    away_code = yield self._get_away_code(request['token'])
                    self.write({
                        "code": 200, 
                        "away_reasons": away_code
                    })
                    self.set_status(200)
                else:
                    self.write({"code":404, "errorMessage": "away reason not found"})
                    self.set_status(404)
            else:
                raise ValueError
        except ValueError:
            self.write({"code":400, "errorMessage":"Bad request"})
            self.set_status(400)

    @gen.coroutine
    def _get_away_code(self, token_id):
        results = self.db.query(AwayReason).filter(AwayReason.tenant_id == User.tenant_id, 
                                                  User.user_id == Token.user_id, 
                                                  Token.token_id == token_id).all()      
        if results:
            results_ = []
            for element in results:
                results_.append(element.to_json())
            
            away_reasons = [{
                "id": element['id'],
                "text": element['away_reason']
            } for element in results_]
        else:
            err = "Not found any reason"
            raise gen.Return(False)
        raise gen.Return(away_reasons)
        
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
            self.write({"code":401, "errorMessage":"token is wrong"})
            self.set_status(401)
            raise gen.Return(False)

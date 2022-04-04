from handlers.base import BaseHandler
from http import HTTPStatus
from tornado import gen
import imp
import datetime
import uuid
import json
import MySQLdb
from sqlalchemy import func
from ..base import BaseHandler
from ..users.models import User, Token, Tenant
from .models import CallerId, CallerIdUser
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log

log = log.get(__name__)

# Create API for caller notification number

class CallerIdSearchHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to search caller notification number by conditions.
        :param TenantId
        :param UserId
        :param SearchWord
        :param Sort1
        :param Sort2
        :param Sort3
        :param Offset
        :param Limit
        """
        self.write_response()

class CallerIdGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to get a specified caller notification number detailed allocation is acquired. 
        :param TenantId
        :param UserId
        :param CallerNumId
        """
        self.write_response()


class CallerIdUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to update the caller notification number
        :param TenantId
        :param UserId
        :param UserList
            :subparam UserId
        :param GroupList
            :subparam GroupId
        """
        self.write_response()
    
class GetNotificationNumbersHandler(BaseHandler):
    
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
                    numbers = yield self._get_numbers(request['token'])
                    if numbers:
                        self.write({
                            "code": 200, 
                            "skill_groups": numbers
                        })
                        self.set_status(200)
                    else:
                        self.write({"code":404, "errorMessage": "numbers not found"})
                        self.set_status(404)
                else:
                    self.write({"code":401, "errorMessage":"token is wrong"})
                    self.set_status(401)
            else:
                raise ValueError
        except ValueError:
            self.set_status(400)
            self.write({"code":400, "errorMessage":"Bad request"})

    @gen.coroutine
    def _get_numbers(self, token_id):
        results = self.db.query(CallerId).filter(CallerId.caller_num_id == CallerIdUser.caller_num_id,
                                                 CallerIdUser.user_id == Token.user_id,
                                                 Token.token_id == token_id).all()
        if results:
            results_ = []
            for elemant in results:
                results_.append(elemant.to_json())
                
            numbers = [{
                "id": element['caller_num_id'],
                "value": element['caller_num'],
                "in_use": "false"
            } for element in results_]
        else:
            err = "Not found any number"
            raise gen.Return(False)
        raise gen.Return(numbers)

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

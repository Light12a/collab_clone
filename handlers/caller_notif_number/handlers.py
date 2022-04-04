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
    
class GetNotificationNumbersHandler(BaseHandler):
    """
    This class is created to build get_notification_numbers API.
    Param of request is token_id.
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
                    numbers = yield self._get_numbers(request['token'])
                    if numbers:
                        self.write({
                            "code": 200, 
                            "numbers": numbers
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
        """
        Find out the list of notification numbers.
        Param: token_id
        """
        results = self.db.query(CallerId).filter(CallerId.caller_num_id == CallerIdUser.caller_num_id,
                                                 CallerIdUser.user_id == Token.user_id,
                                                 Token.token_id == token_id).all()
        try:
            results_ = []
            for elemant in results:
                results_.append(elemant.to_json())
            numbers = [{
                "id": element['caller_num_id'],
                "value": element['caller_num'],
                "in_use": "true"
            } for element in results_]
            raise gen.Return(numbers)
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
                             
class ApplyNotificationNumberHandler(BaseHandler):
    """
    This class is created to build apply_notification_number API.
    Params of request are token_id and number_id.
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
            if "token" in request and "number_id" in request:
                check = yield self._check_token_exists(request['token'])
                if check:
                    apply = yield self._apply_notification_number(request)
                    print(apply)
                    if apply:
                        self.write({
                            "code": 200                        
                        })
                        self.set_status(200)
                    else:
                        self.write({"code":401, "errorMessage":"number_id not found"})
                        self.set_status(401)
                else:
                    self.write({"code":401, "errorMessage":"token is wrong"})
                    self.set_status(401)
            else:
                raise ValueError
            
        except ValueError:
            self.set_status(400)
            self.write({"code":400, "errorMessage":"Bad request"})
    
    @gen.coroutine
    def _apply_notification_number(self, request):
        """
        Apply notification number with a number_id for a user.
        Params: request['token'] and request['number_id]
        """    
        try:
            query = self.db.query(CallerIdUser).filter(Token.user_id == User.user_id,
                                                       CallerIdUser.tenant_id == User.tenant_id,
                                                       Token.token_id == request['token']).one()
            query.caller_num_id = request['number_id']
            self.db.commit()
            return True
        except:
            err = "Not found any number"
            return False
                                       
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

import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import Tenant
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen

class TenantRetrievalHandler(BaseHandler):
    """
    This class handles tenant retrieval.
    It accedes to term, the tenant is retrieved, and the result is returned.
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
            if (("TenantId" and "OperatorUserId" and "SearchWord") or ()
                ) in request:
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

    # @gen.coroutine
    # def _get_numbers(self, token_id):
    #     """
    #     Find out the list of notification numbers.
    #     Param: token_id
    #     """
    #     results = self.db.query(CallerId).filter(
    #         CallerId.caller_num_id == CallerIdUser.caller_num_id,
    #         CallerIdUser.user_id == Token.user_id,
    #         Token.token_id == token_id
    #     ).all()
    #     if results:
    #         results_ = []
    #         for elemant in results:
    #             results_.append(elemant.to_json())
                
    #         numbers = [{
    #             "id": element['caller_num_id'],
    #             "value": element['caller_num'],
    #             "in_use": "false"
    #         } for element in results_]
    #     else:
    #         err = "Not found any number"
    #         raise gen.Return(False)
    #     raise gen.Return(numbers)

    # @gen.coroutine
    # def _check_token_exists(self, token):
    #     """
    #     Function take in token to verify this one is the newest.
    #     @params: Token.
    #     """
    #     result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

    #     try:
    #         raise gen.Return(result[0][0])
    #     except IndexError:
    #         raise gen.Return(False)

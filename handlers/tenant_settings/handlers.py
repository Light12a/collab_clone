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
            if ("TenantId" and "OperatorUserId" and "SearchWord") in request:
                    tenants = yield self._get_tenants(request)
                    if tenants:
                        self.write({
                            "ResultCode": 200,
                            "Message": "Here is the result",
                            "DataList": tenants
                        })
                        self.set_status(200)
                    else:
                        self.write({"code":404, "errorMessage": "No matching results were found"})
                        self.set_status(404)
            else:
                raise ValueError
        except ValueError:
            self.set_status(400)
            self.write({"code":400, "errorMessage":"Bad request"})

    @gen.coroutine
    def _get_tenants(self, request):
        """
        Find out the list of notification numbers.
        Param: token_id
        """
        # results = self.db.query(Tenant).filter(Tenant.identifier == request['SearchWord']).all()
        SearchWord = request['SearchWord']
        results = self.db.query(Tenant).filter(Tenant.identifier.like(SearchWord))

        if results:
            results_ = []
            for elemant in results:
                results_.append(elemant.to_json())
                
            tenants = [{
                "TenantId": element['tenant_id'],
                "TenantName": element['tenant_name'],
                "Identifier": element['identifier'],
                "ChannelCnt": element['channel_cnt'],
                "UpdateDate": element['update_date']
            } for element in results_]
        else:
            err = "Not found any number"
            raise gen.Return(False)
        raise gen.Return(tenants)
